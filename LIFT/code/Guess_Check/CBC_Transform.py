import os
import re
import subprocess
import time
import shutil
from functools import reduce
import antlr4
from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl
import sys
sys.path.append(os.path.abspath('code'))

from BoogieAST.AST2SourceVisitor import AST2SourceVisitor #pylint: disable=import-error
from BoogieAST.ASTOperation import ASTOperation #pylint: disable=import-error
from BoogieAST.BoogieLexer import BoogieLexer #pylint: disable=import-error
from BoogieAST.BoogieParser import BoogieParser #pylint: disable=import-error

class CBChecker:
    
    def __init__(self, tmpDir, tempfile, itvar):
        self.tmpDir = os.path.abspath(tmpDir)
        self.tempfile = os.path.abspath(tempfile)
        self.fileName = None
        self.projectDir = '/'.join(os.getcwd().split('/'))
        self.boogieDir = self.projectDir + '/ice/popl16_artifact/Boogie/Binaries'
        self.boogieArgs = ['/noinfer', '/contractInfer',  '/liveVariableAnalysis:0', 
            '/printAssignment', '/trace', '/printModel:4']
        self.itvar = itvar
        self.start_time = 0
        self.end_time = 0
        self.time = 0

        fileName = self.tempfile.split('/')[-1]
        if not os.path.exists(self.tmpDir):
            os.makedirs(self.tmpDir)
        outFile = os.path.join(self.tmpDir, fileName)
        self.fileName = outFile
        self.CBCfileName = os.path.join(self.tmpDir, 'CBC_' + fileName)

    def ExecuteCBC(self, Bound, ret='default', timeout = None, timeoutMonitor = None, withloopbound = False, lexical = False):
        # withloopbound, lexical are for generating BMC bpl file
        self.GenerateConcreteBplFile(Bound, withloopbound, lexical)
        curDir = os.path.abspath('.')
        os.chdir(self.boogieDir)
        print('[Debug] Boogie Dir: {}'.format(self.boogieDir))
        # print('[Debug]', self.CBCfileName)
        print('[Debug] Boogie Cmd: {}'.format(reduce(lambda x,y: '{} {}'.format(x,y), ['mono', 'Boogie.exe'] + self.boogieArgs + [self.CBCfileName])))
        Timer = []
        if timeout != None:
            Timer = [timeoutMonitor, '--foreground', '--kill-after', '1', str(int(timeout) + 1)]
        self.start_time = time.perf_counter()
        process = subprocess.Popen(
            Timer + ['mono', 'Boogie.exe'] + self.boogieArgs + [self.CBCfileName],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        os.chdir(curDir)

        stdout, stderr = process.communicate()
        self.end_time = time.perf_counter()
        self.time = self.end_time - self.start_time

        # print(stdout.decode())
        stdoutLines = stdout.decode().split('\n')

        reMatcher = r'Boogie program verifier finished with (\d+) verified, (\d+) error(s)?'
        reResult = re.search(reMatcher, stdoutLines[-2])
        if reResult == None:
            print('[Info] Benchmark timeout!')
            #return {'Result': 'Timeout'}
            return 0

        verifiedNum = int(reResult.group(1))
        errorNum = int(reResult.group(2))
        if errorNum == 0:
            print('[info] CBC verified with bound {}'.format(Bound))
            #return {'Result': 'Verified', 'Invariant': None, 'ConstBoundChecker': Bound}
            return 1
        else: 
            if ret == 'default':
                print('[info] CBC failed ')
                #return {'Result': 'Failed-CBC'}
                return 0
            elif ret == 'trace':
                raise NotImplementedError()
            else:
                raise RuntimeError('Unsupported return type for CBC.')
    

    def GenerateConcreteBplFile(self, ConstBound, withloopbound = False, lexical = False):
        input_stream = antlr4.FileStream(self.fileName)
        lexer = BoogieLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = BoogieParser(stream)
        AST = parser.boogie_program()
        
        whileLoopPa = ASTOperation.FindNode(AST, Filter= lambda x: type(x) == BoogieParser.Structured_cmdContext and x.getChildCount() == 1 and type(x.getChild(0)) == BoogieParser.While_cmdContext)
        if len(whileLoopPa) != 1:
            raise RuntimeError('Find no or more than one while loop!')
        
        def contain(node, v):
            if type(node) == TerminalNodeImpl:
                return v == node.getSymbol().text
            for i in range(node.getChildCount()):
                if contain(node.getChild(i), v):
                    # import pdb; pdb.set_trace()
                    return True
            return False

        def toDel(node):
            if type(node) == BoogieParser.Func_declContext:
                return True
            if not type(node) == BoogieParser.Label_or_cmdContext:
                return False
            # import pdb; pdb.set_trace()
            return contain(node, self.itvar)
        if withloopbound and not lexical:
            Loop_bound = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assume_cmdContext and contain(x, self.itvar))
            Loop_bound = Loop_bound[0]
        ASTOperation.RemoveNode(AST, toDel)
        # while => assume
        whileLoop = whileLoopPa[0].getChild(0)
        whileLoopGuardExpr = whileLoop.guard().children[1]
        assumeCmd = ASTOperation.Assume_Cmd(parser, whileLoopGuardExpr)
        # break => assume false
        whileStmts = whileLoop.stmt_list()
        breaks = ASTOperation.FindNode(whileStmts, lambda x: type(x) == BoogieParser.Break_cmdContext)
        breaksInStmts = list(map(lambda x: x.parentCtx.parentCtx, breaks))
        for stId in range(len(breaksInStmts)):
            for childId in range(len(breaksInStmts[stId].children)):
                if breaksInStmts[stId].children[childId] == breaks[stId].parentCtx:
                    assumeFalseCmd = ASTOperation.Assume_Cmd(parser, ASTOperation.Terminal_False())
                    breaksInStmts[stId].children[childId] = assumeFalseCmd
                    # print('[Debug] MATCH!')
                    # print(breaksInStmts[stId].getText())

                # print(breaksInStmts[stId].getText())

        # print(whileStmts.getText())
        # import pdb; pdb.set_trace()
        # repeat C times
        if withloopbound and not lexical:
            statementList = [Loop_bound] + ([assumeCmd] + \
                whileLoop.stmt_list().children) * ConstBound + \
                [assumeCmd, ASTOperation.Assert_Cmd(parser, ASTOperation.Terminal_False())]

        else:
            statementList = ([assumeCmd] + \
                whileLoop.stmt_list().children) * ConstBound + \
                [assumeCmd, ASTOperation.Assert_Cmd(parser, ASTOperation.Terminal_False())]

        whilePos = ASTOperation.ParentChildID(whileLoop, whileLoopPa[0])
        ASTOperation.RemoveChild(whileLoopPa[0], whilePos)

        ASTOperation.AddChild(whileLoopPa[0], statementList, whilePos)

        visitor = AST2SourceVisitor()
        visitor.visit(AST)
        # print(self.CBCfileName)
        print('[info] Write to CBC file {}'.format(self.CBCfileName))
        with open(self.CBCfileName, 'w') as CBCWriter:
             CBCWriter.write(visitor.Output)
if __name__ == '__main__':
    test = CBChecker('/tmpfs/tmp', '/tmpfs/tmp/test.bpl', 'i')
    test.GenerateConcreteBplFile(3, True, True)
    #test.ExecuteCBC(3)