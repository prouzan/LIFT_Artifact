from antlr4 import *
from BoogieAST.BoogieLexer import BoogieLexer #pylint: disable=import-error
from BoogieAST.BoogieParser import BoogieParser #pylint: disable=import-error
from BoogieAST.BoogieListener import BoogieListener #pylint: disable=import-error
from BoogieAST.BoogieVisitor import BoogieVisitor #pylint: disable=import-error
from BoogieAST.AST2SourceVisitor import AST2SourceVisitor #pylint: disable=import-error
import pdb

class ASTOperation:
    
    # def __init__(self, AST):
    #     self.AST = AST

    @staticmethod
    def FindNode(ASTNode, Filter = lambda x: True):
        RetList = []
        if Filter(ASTNode):
            RetList.append(ASTNode)
        if ASTNode is None:
            return RetList
        for i in range(ASTNode.getChildCount()):
            RetList += ASTOperation.FindNode(ASTNode.getChild(i), Filter)
        return RetList

    @staticmethod
    def GetChildByType(ASTNode, NodeType):
        for i in range(ASTNode.getChildCount()):
            if type(ASTNode.getChild(i)) == NodeType:
                return ASTNode.getChild(i)
        return None

    @staticmethod
    def RemoveNode(ASTNode, Rule = lambda x: False):
        if ASTNode.getChildCount() == 0:
            return
        newChildren = []
        for i in range(ASTNode.getChildCount()):
            if not Rule(ASTNode.getChild(i)):
                # import pdb; pdb.set_trace()
                newChildren.append(ASTNode.getChild(i))
            else:
                # import pdb; pdb.set_trace()
                ...
        ASTNode.children = newChildren
        for i in range(ASTNode.getChildCount()):
            ASTOperation.RemoveNode(ASTNode.getChild(i), Rule)

    @staticmethod
    def RemoveChild(ASTNode, position):
        ASTNode.children = ASTNode.children[:position] + ASTNode.children[position + 1:]

    @staticmethod
    def AddChild(ASTNode, newNode, position):
        if not type(newNode) == list:
            newNode = [newNode]
        ASTNode.children = ASTNode.children[:position] + newNode + ASTNode.children[position:]

    @staticmethod
    def ParentChildID(ASTNode, ASTPa):
        for i in range(ASTPa.getChildCount()):
            if ASTPa.getChild(i) == ASTNode:
                return i
        return -1

    @staticmethod
    def Terminal_CommonToken(text):
        from antlr4.Token import CommonToken
        from antlr4.tree.Tree import TerminalNodeImpl
        token = CommonToken()
        token.text = text
        return TerminalNodeImpl(token)

    @staticmethod
    def Assume_Cmd(parser, expr):
        assumeCmd = BoogieParser.Assume_cmdContext(parser)
        proposition = BoogieParser.PropositionContext(parser)
        proposition.children = [expr]
        assumeCmd.children = [
            ASTOperation.Terminal_CommonToken('assume'), 
            proposition, 
            ASTOperation.Terminal_CommonToken(';')]
        return assumeCmd

    @staticmethod
    def Assert_Cmd(parser, expr):
        assertCmd = BoogieParser.Assume_cmdContext(parser)
        proposition = BoogieParser.PropositionContext(parser)
        proposition.children = [expr]
        assertCmd.children = [
            ASTOperation.Terminal_CommonToken('assert'), 
            proposition, 
            ASTOperation.Terminal_CommonToken(';')]
        return assertCmd

    @staticmethod
    def Terminal_True():
        return ASTOperation.Terminal_CommonToken('true')

    @staticmethod
    def Terminal_False():
        return ASTOperation.Terminal_CommonToken('false')
    

# Test code
# input_stream = FileStream('lexic.bpl')
# lexer = BoogieLexer(input_stream)
# stream = CommonTokenStream(lexer)
# parser = BoogieParser(stream)
# tree = parser.boogie_program()

# ASTOperation.FindNode(tree, None)

# visitor = AST2SourceVisitor()
# visitor.visit(tree)
# print(visitor.Output)