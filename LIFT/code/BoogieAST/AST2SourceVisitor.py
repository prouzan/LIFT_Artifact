import sys
from antlr4 import *
import os

from BoogieAST.BoogieLexer import BoogieLexer #pylint: disable=import-error
from BoogieAST.BoogieParser import BoogieParser #pylint: disable=import-error
from BoogieAST.BoogieListener import BoogieListener #pylint: disable=import-error
from BoogieAST.BoogieVisitor import BoogieVisitor #pylint: disable=import-error

import string
# import pdb


class AST2SourceVisitor(BoogieVisitor):

    def __init__(self, indentInc = 2):
        self.LastSymbol = None
        self.LastIsAttr = False
        self.Indent = 0
        self.IndentInc = indentInc
        self.HasNewline = False
        self.IsNewline = True
        self.Output = ''

    def doSpace(self, ctx):
        last = self.LastSymbol
        current = ctx.getText()
        if last == None:
            return False
        spacings = list(string.ascii_letters + string.digits + "_.$#'`~^\\?>=<&|+-*!")
        last = last[-1]
        if last in spacings and current == ':=':
            return True
        if last == ',':
            return True
        current = current[0]
        isAttr = 'Attr' in type(ctx.getParent()).__name__
        Lspaceing = spacings
        Rspaceing = list(spacings)
        if self.LastIsAttr or isAttr:
            Lspaceing.append('}')
            Rspaceing.append('{')
        self.LastIsAttr = isAttr
        
        return last in Lspaceing and current in Rspaceing

    def doNewlineAfter(self, ctx):
        current = ctx.getText()
        if current in ['{', '}'] and 'Attr' in type(ctx.getParent()).__name__:
            self.HasNewline = False
            self.IsNewline = False
            return False
        if current in [';' , '}']:
            self.HasNewline = True
            self.IsNewline = True
            return True
        if current == '{':
            self.Indent += self.IndentInc
            self.HasNewline = True
            self.IsNewline = True
            return True
        self.HasNewline = False
        self.IsNewline = False
        return False

    def doNewlineBefore(self, ctx):
        current = ctx.getText()
        if current in ['{', '}'] and 'Attr' in type(ctx.getParent()).__name__:
            return False
        if current in ['{', 'invariant']:
            self.IsNewline = True
            return not self.HasNewline
        if current == '}':
            self.Indent -= self.IndentInc
            self.IsNewline = True
            return not self.HasNewline
        return False
    
    def visitTerminal(self, ctx):
        currentSymbol = ctx.getText()
        if self.doSpace(ctx):
            self.Output += ' '
        elif self.doNewlineBefore(ctx):
            self.Output += '\n'
        if self.IsNewline:
            self.Output += ' ' * self.Indent
        self.Output += ctx.getText()
        if self.doNewlineAfter(ctx):
            self.Output += '\n'

        self.LastSymbol = currentSymbol
        


         
# Use example:
# input_stream = FileStream('lexic.bpl')
# lexer = BoogieLexer(input_stream)
# stream = CommonTokenStream(lexer)
# parser = BoogieParser(stream)
# tree = parser.boogie_program()

# visitor = AST2SourceVisitor()
# visitor.visit(tree)
# print(visitor.Output)
