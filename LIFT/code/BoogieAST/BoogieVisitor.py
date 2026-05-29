# Generated from Boogie.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BoogieParser import BoogieParser
else:
    from BoogieParser import BoogieParser

# This class defines a complete generic visitor for a parse tree produced by BoogieParser.

class BoogieVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BoogieParser#boogie_program.
    def visitBoogie_program(self, ctx:BoogieParser.Boogie_programContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#axiom_decl.
    def visitAxiom_decl(self, ctx:BoogieParser.Axiom_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#const_decl.
    def visitConst_decl(self, ctx:BoogieParser.Const_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#func_decl.
    def visitFunc_decl(self, ctx:BoogieParser.Func_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#impl_decl.
    def visitImpl_decl(self, ctx:BoogieParser.Impl_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#proc_decl.
    def visitProc_decl(self, ctx:BoogieParser.Proc_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#type_decl.
    def visitType_decl(self, ctx:BoogieParser.Type_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#var_decl.
    def visitVar_decl(self, ctx:BoogieParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#order_spec.
    def visitOrder_spec(self, ctx:BoogieParser.Order_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#var_or_type.
    def visitVar_or_type(self, ctx:BoogieParser.Var_or_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#proc_sign.
    def visitProc_sign(self, ctx:BoogieParser.Proc_signContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#impl_body.
    def visitImpl_body(self, ctx:BoogieParser.Impl_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#stmt_list.
    def visitStmt_list(self, ctx:BoogieParser.Stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#local_vars.
    def visitLocal_vars(self, ctx:BoogieParser.Local_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#spec.
    def visitSpec(self, ctx:BoogieParser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#modifies_spec.
    def visitModifies_spec(self, ctx:BoogieParser.Modifies_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#requires_spec.
    def visitRequires_spec(self, ctx:BoogieParser.Requires_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#ensures_spec.
    def visitEnsures_spec(self, ctx:BoogieParser.Ensures_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#label_or_cmd.
    def visitLabel_or_cmd(self, ctx:BoogieParser.Label_or_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#transfer_cmd.
    def visitTransfer_cmd(self, ctx:BoogieParser.Transfer_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#structured_cmd.
    def visitStructured_cmd(self, ctx:BoogieParser.Structured_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#assert_cmd.
    def visitAssert_cmd(self, ctx:BoogieParser.Assert_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#assign_cmd.
    def visitAssign_cmd(self, ctx:BoogieParser.Assign_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#assignment_lhs.
    def visitAssignment_lhs(self, ctx:BoogieParser.Assignment_lhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#assignment_lhs_indexed.
    def visitAssignment_lhs_indexed(self, ctx:BoogieParser.Assignment_lhs_indexedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#assume_cmd.
    def visitAssume_cmd(self, ctx:BoogieParser.Assume_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#break_cmd.
    def visitBreak_cmd(self, ctx:BoogieParser.Break_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#call_cmd.
    def visitCall_cmd(self, ctx:BoogieParser.Call_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#goto_cmd.
    def visitGoto_cmd(self, ctx:BoogieParser.Goto_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#havoc_cmd.
    def visitHavoc_cmd(self, ctx:BoogieParser.Havoc_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#if_cmd.
    def visitIf_cmd(self, ctx:BoogieParser.If_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#label.
    def visitLabel(self, ctx:BoogieParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#par_call_cmd.
    def visitPar_call_cmd(self, ctx:BoogieParser.Par_call_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#return_cmd.
    def visitReturn_cmd(self, ctx:BoogieParser.Return_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#while_cmd.
    def visitWhile_cmd(self, ctx:BoogieParser.While_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#yield_cmd.
    def visitYield_cmd(self, ctx:BoogieParser.Yield_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#call_params.
    def visitCall_params(self, ctx:BoogieParser.Call_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#void_call_params_remain.
    def visitVoid_call_params_remain(self, ctx:BoogieParser.Void_call_params_remainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#ret_call_params_remain.
    def visitRet_call_params_remain(self, ctx:BoogieParser.Ret_call_params_remainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#guard.
    def visitGuard(self, ctx:BoogieParser.GuardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#r_type.
    def visitR_type(self, ctx:BoogieParser.R_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#type_args.
    def visitType_args(self, ctx:BoogieParser.Type_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#type_atom.
    def visitType_atom(self, ctx:BoogieParser.Type_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#map_type.
    def visitMap_type(self, ctx:BoogieParser.Map_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#exprs.
    def visitExprs(self, ctx:BoogieParser.ExprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#proposition.
    def visitProposition(self, ctx:BoogieParser.PropositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#expr.
    def visitExpr(self, ctx:BoogieParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#equiv_op.
    def visitEquiv_op(self, ctx:BoogieParser.Equiv_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#implies_expr.
    def visitImplies_expr(self, ctx:BoogieParser.Implies_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#implies_op.
    def visitImplies_op(self, ctx:BoogieParser.Implies_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#explies_op.
    def visitExplies_op(self, ctx:BoogieParser.Explies_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#logical_expr.
    def visitLogical_expr(self, ctx:BoogieParser.Logical_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#and_op.
    def visitAnd_op(self, ctx:BoogieParser.And_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#or_op.
    def visitOr_op(self, ctx:BoogieParser.Or_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#rel_expr.
    def visitRel_expr(self, ctx:BoogieParser.Rel_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#rel_op.
    def visitRel_op(self, ctx:BoogieParser.Rel_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#bv_term.
    def visitBv_term(self, ctx:BoogieParser.Bv_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#term.
    def visitTerm(self, ctx:BoogieParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#add_op.
    def visitAdd_op(self, ctx:BoogieParser.Add_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#factor.
    def visitFactor(self, ctx:BoogieParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#mul_op.
    def visitMul_op(self, ctx:BoogieParser.Mul_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#power.
    def visitPower(self, ctx:BoogieParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#unary_expr.
    def visitUnary_expr(self, ctx:BoogieParser.Unary_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#neg_op.
    def visitNeg_op(self, ctx:BoogieParser.Neg_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#coercion_expr.
    def visitCoercion_expr(self, ctx:BoogieParser.Coercion_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#array_expr.
    def visitArray_expr(self, ctx:BoogieParser.Array_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#indexed.
    def visitIndexed(self, ctx:BoogieParser.IndexedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#atom_expr.
    def visitAtom_expr(self, ctx:BoogieParser.Atom_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#bool_lit.
    def visitBool_lit(self, ctx:BoogieParser.Bool_litContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#nat.
    def visitNat(self, ctx:BoogieParser.NatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#dec.
    def visitDec(self, ctx:BoogieParser.DecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#decimal.
    def visitDecimal(self, ctx:BoogieParser.DecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#dec_float.
    def visitDec_float(self, ctx:BoogieParser.Dec_floatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#bv_lit.
    def visitBv_lit(self, ctx:BoogieParser.Bv_litContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#old_expr.
    def visitOld_expr(self, ctx:BoogieParser.Old_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#arith_coercion_expr.
    def visitArith_coercion_expr(self, ctx:BoogieParser.Arith_coercion_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#paren_expr.
    def visitParen_expr(self, ctx:BoogieParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#forall_expr.
    def visitForall_expr(self, ctx:BoogieParser.Forall_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#exists_expr.
    def visitExists_expr(self, ctx:BoogieParser.Exists_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#lambda_expr.
    def visitLambda_expr(self, ctx:BoogieParser.Lambda_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#forall.
    def visitForall(self, ctx:BoogieParser.ForallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#exists.
    def visitExists(self, ctx:BoogieParser.ExistsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#r_lambda.
    def visitR_lambda(self, ctx:BoogieParser.R_lambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#quant_body.
    def visitQuant_body(self, ctx:BoogieParser.Quant_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#bound_vars.
    def visitBound_vars(self, ctx:BoogieParser.Bound_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#qsep.
    def visitQsep(self, ctx:BoogieParser.QsepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#if_then_else_expr.
    def visitIf_then_else_expr(self, ctx:BoogieParser.If_then_else_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#code_expr.
    def visitCode_expr(self, ctx:BoogieParser.Code_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#spec_block.
    def visitSpec_block(self, ctx:BoogieParser.Spec_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#attr_typed_idents_wheres.
    def visitAttr_typed_idents_wheres(self, ctx:BoogieParser.Attr_typed_idents_wheresContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#attr_typed_idents_where.
    def visitAttr_typed_idents_where(self, ctx:BoogieParser.Attr_typed_idents_whereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#typed_idents_wheres.
    def visitTyped_idents_wheres(self, ctx:BoogieParser.Typed_idents_wheresContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#typed_idents_where.
    def visitTyped_idents_where(self, ctx:BoogieParser.Typed_idents_whereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#typed_idents.
    def visitTyped_idents(self, ctx:BoogieParser.Typed_identsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#idents.
    def visitIdents(self, ctx:BoogieParser.IdentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#type_params.
    def visitType_params(self, ctx:BoogieParser.Type_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#attr.
    def visitAttr(self, ctx:BoogieParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#attr_or_trigger.
    def visitAttr_or_trigger(self, ctx:BoogieParser.Attr_or_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BoogieParser#attr_param.
    def visitAttr_param(self, ctx:BoogieParser.Attr_paramContext):
        return self.visitChildren(ctx)



del BoogieParser