import os
import re
import subprocess
import shutil
from functools import reduce
import antlr4
from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl
import sys
sys.path.append(os.path.abspath('code'))
from StateTrans import TraceStateTrans  #pylint: disable=import-error
from StateTrans.TraceStateTrans import * #pylint: disable=import-error

from BoogieAST.AST2SourceVisitor import AST2SourceVisitor #pylint: disable=import-error
from BoogieAST.ASTOperation import ASTOperation #pylint: disable=import-error
from BoogieAST.BoogieLexer import BoogieLexer #pylint: disable=import-error
from BoogieAST.BoogieParser import BoogieParser #pylint: disable=import-error

class K_Transformer:
    
    def __init__(self, tmpDir, tempfile, itvar):
        #self.Logger = logger
        self.tmpDir = os.path.abspath(tmpDir)
        self.tempfile = os.path.abspath(tempfile)
        self.fileName = None
        self.projectDir = '/'.join(os.getcwd().split('/'))
        self.boogieDir = self.projectDir + '/ice/popl16_artifact/Boogie/Binaries'
        self.boogieArgs = ['/noinfer', '/contractInfer', '/liveVariableAnalysis:0', 
            '/printAssignment', '/trace', '/printModel:4', 
            # '/proverLog:tst.smt'
            '/errorLimit:10'
            ]

        self.itvar = itvar
        '''
        if self.Logger.SMTFile != None:
            self.boogieArgs.append('/proverLog:{}'.format(self.Logger.SMTFile))
        '''
        fileName = self.tempfile.split('/')[-1]
        if not os.path.exists(self.tmpDir):
            os.makedirs(self.tmpDir)
        outFile = os.path.join(self.tmpDir, fileName)
        self.fileName = outFile
        #self.fileName = self.tempfile
        self.K_fileName = os.path.join(self.tmpDir, 'K_' + fileName)

    def GenerateConcreteBplFile(self, ConstBound, withinv = False):
        """
        Generate Boogie file in specified format, including pre-loop and in-loop unrolling, and remove/add assert and i decrement statements.
        """
        if ConstBound == 1:
            shutil.copy(self.fileName, self.K_fileName)
            return
        input_stream = antlr4.FileStream(self.fileName)
        lexer = BoogieLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = BoogieParser(stream)
        AST = parser.boogie_program()
        
        whileLoopPa = ASTOperation.FindNode(AST, Filter= lambda x: type(x) == BoogieParser.Structured_cmdContext and x.getChildCount() == 1 and type(x.getChild(0)) == BoogieParser.While_cmdContext)
        if len(whileLoopPa) != 1:
            raise RuntimeError('Find no or more than one while loop!')
        assertCtx = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assert_cmdContext)
        if len(assertCtx) != 1:
            raise RuntimeError('The number of assert is not 1.')
        assertCtx = assertCtx[0]

        def contain(node, v):
            if type(node) == TerminalNodeImpl:
                return v == node.getSymbol().text
            for i in range(node.getChildCount()):
                if contain(node.getChild(i), v):
                    # import pdb; pdb.set_trace()
                    return True
            return False

        def toDel(node):
            #if type(node) == BoogieParser.Func_declContext:
            #    return True
            if not type(node) == BoogieParser.Label_or_cmdContext:
                return False
            # import pdb; pdb.set_trace()
            return contain(node, self.itvar)
        Loop_bound = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assume_cmdContext and contain(x, self.itvar))
        Loop_bound = Loop_bound[0]
        Count_decl = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assign_cmdContext and contain(x, self.itvar) )
        Count_decl = Count_decl[0]
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

        base_statementList = ([assumeCmd] + \
            whileLoop.stmt_list().children) * ConstBound + \
            [Loop_bound]
            #[assumeCmd, ASTOperation.Assert_Cmd(parser, ASTOperation.Terminal_False())]
        inner_statementList = ([assumeCmd] + whileLoop.stmt_list().children) \
            * (ConstBound - 1) + [Count_decl] #+ [assertCtx]

        whilePos = ASTOperation.ParentChildID(whileLoop, whileLoopPa[0])
        #ASTOperation.RemoveChild(whileLoopPa[0], whilePos)
        ASTOperation.AddChild(whileLoopPa[0], base_statementList, whilePos) #ASTNode, newNode, position
        if withinv:
            ASTOperation.AddChild(whileLoop, [assertCtx], 6)
        else:
            ASTOperation.AddChild(whileLoop, [assertCtx], 3)
        ASTOperation.AddChild(whileLoop, inner_statementList, -1)
        visitor = AST2SourceVisitor()
        visitor.visit(AST)
        # print(self.CBCfileName)
        with open(self.K_fileName, 'w') as K_Writer:
             K_Writer.write(visitor.Output)


    def GenerateConcreteBplFileLexical(self, ConstBound, itvars, withinv = False):
        """
        Generate Boogie file in specified format, including pre-loop and in-loop unrolling, and remove/add assert and i decrement statements.
        """
        if ConstBound == 1:
            shutil.copy(self.fileName, self.K_fileName)
            return
        input_stream = antlr4.FileStream(self.fileName)
        lexer = BoogieLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = BoogieParser(stream)
        AST = parser.boogie_program()
        
        whileLoopPa = ASTOperation.FindNode(AST, Filter= lambda x: type(x) == BoogieParser.Structured_cmdContext and x.getChildCount() == 1 and type(x.getChild(0)) == BoogieParser.While_cmdContext)
        if len(whileLoopPa) != 1:
            raise RuntimeError('Find no or more than one while loop!')
        assertCtx = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assert_cmdContext)
        if len(assertCtx) != 1:
            raise RuntimeError('The number of assert is not 1.')
        assertCtx = assertCtx[0]

        def contain(node, v):
            if type(node) == TerminalNodeImpl:
                return v == node.getSymbol().text
            for i in range(node.getChildCount()):
                if contain(node.getChild(i), v):
                    # import pdb; pdb.set_trace()
                    return True
            return False

        def toDel(node):
            #if type(node) == BoogieParser.Func_declContext:
            #    return True
            if not (type(node) == BoogieParser.Label_or_cmdContext) and not (type(node) == BoogieParser.Structured_cmdContext and type(node.getChild(0)) == BoogieParser.If_cmdContext):
                return False
            # import pdb; pdb.set_trace()
            for itvar in itvars:
                if contain(node, itvar):
                    return True
        Loop_bound = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assume_cmdContext and contain(x, itvars[0]))
        Loop_bound = Loop_bound[0]
        if len(itvars) > 1:
            Count_decl = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Structured_cmdContext and type(x.getChild(0)) == BoogieParser.If_cmdContext and contain(x, itvars[0]) )
        else:
            Count_decl = ASTOperation.FindNode(AST, lambda x: type(x) == BoogieParser.Assign_cmdContext and contain(x, itvars[0]) )
        Count_decl = Count_decl[0]
        ASTOperation.RemoveNode(AST, toDel)
        # while => assume
        #whileLoopPa_new = ASTOperation.FindNode(AST, Filter= lambda x: type(x) == BoogieParser.Structured_cmdContext and x.getChildCount() == 1 and type(x.getChild(0)) == BoogieParser.While_cmdContext)
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

        base_statementList = ([assumeCmd] + \
            whileStmts.children) * ConstBound + \
            [Loop_bound]
            #[assumeCmd, ASTOperation.Assert_Cmd(parser, ASTOperation.Terminal_False())]
        inner_statementList = ([assumeCmd] + whileStmts.children) * (ConstBound - 1) + [Count_decl]

        whilePos = ASTOperation.ParentChildID(whileLoop, whileLoopPa[0])
        #ASTOperation.RemoveChild(whileLoopPa[0], whilePos)
        ASTOperation.AddChild(whileLoopPa[0], base_statementList, whilePos) #ASTNode, newNode, position
        if withinv:
            ASTOperation.AddChild(whileLoop, [assertCtx], 6)
        else:
            ASTOperation.AddChild(whileLoop, [assertCtx], 3)
        ASTOperation.AddChild(whileLoop, inner_statementList, -1)
        visitor = AST2SourceVisitor()
        visitor.visit(AST)
        # print(self.CBCfileName)
        with open(self.K_fileName, 'w') as K_Writer:
             K_Writer.write(visitor.Output)

if __name__ == '__main__':
    # 1. Read input parameters
    # Read input parameters including temp folder, temp file, variable list, iteration variable
    tmpDir = '/tmpfs/tmp'
    tempfile = '/tmpfs/tmp/k_test.bpl'
    #tempfile = '/root/LIFT/nonlin_mod_term_3.bpl'
    itvar = 'i'

    # 2. Instantiate K_Transformer
    # Instantiate K_Transformer with input parameters
    k_Transformer = K_Transformer(tmpDir, tempfile, itvar)
    # 3. Generate concrete BPL file
    # Generate concrete BPL file, unroll while loop specified number of times
    k_Transformer.GenerateConcreteBplFileLexical(2, ['i0', 'i1'])
    learner = 'dt_penalty'
    projectDir = '/'.join(os.getcwd().split('/'))
    boogieDir = projectDir + '/ice/popl16_artifact/Boogie/Binaries'
    boogieArgs = ['/noinfer', '/contractInfer', '/mlHoudini:{}'.format(learner), 
            '/printAssignment', '/trace']
    command = ['mono', 'Boogie.exe'] + boogieArgs + [k_Transformer.K_fileName]
    curDir = os.path.abspath('.')
    os.chdir(boogieDir)
    process = subprocess.Popen(command,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    os.chdir(curDir)
    stdoutLines = []
    nextIsInv = False
    invIt = 0
    while process.poll() == None:
        line = process.stdout.readline().decode().strip()
        if line.startswith('\n') or line == '':
            continue
        stdoutLines.append(line)
        if nextIsInv:
                print('[Info] Guess Inv #{}: {}'.format(invIt,line))
                invIt += 1
                nextIsInv = False
        if line.startswith('{'):
            nextIsInv = True
    resultLine = stdoutLines[-1]
    invLine = stdoutLines[-4]
    print(resultLine)
    reMatcher = r'Boogie program verifier finished with (\d+) verified, (\d+) error(s)?'
    reResult = re.search(reMatcher, resultLine)
    if reResult == None:
        reMatcher = r'Boogie program verifier exited with error detected at (.*):(.*)'
        reResult = re.search(reMatcher, resultLine)
        
        if reResult == None:
            print('ICE Error Info:')
            print('{}'.format(reduce(lambda x, y: '{}\n{}'.format(x, y), stdoutLines)))
            print('{}'.format(reduce(lambda x,y :'{}\n{}'.format(x, y), stdoutLines)))
            raise RuntimeError('ICE Runtime Error！')
        print('Result'+'Failed-Simp'+'Error')
        print(list(reResult.group(2).split(',')))
    verifiedNum = int(reResult.group(1))
    errorNum = int(reResult.group(2))
    if errorNum == 0:
        print('Result'+'Verified'+'Invariant')
        print(invLine)
    else: 
        print('Result'+'Failed')
