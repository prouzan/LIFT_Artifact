# Generated from Boogie.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BoogieParser import BoogieParser
else:
    from BoogieParser import BoogieParser

# This class defines a complete listener for a parse tree produced by BoogieParser.
class BoogieListener(ParseTreeListener):

    # Enter a parse tree produced by BoogieParser#boogie_program.
    def enterBoogie_program(self, ctx:BoogieParser.Boogie_programContext):
        pass

    # Exit a parse tree produced by BoogieParser#boogie_program.
    def exitBoogie_program(self, ctx:BoogieParser.Boogie_programContext):
        pass


    # Enter a parse tree produced by BoogieParser#axiom_decl.
    def enterAxiom_decl(self, ctx:BoogieParser.Axiom_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#axiom_decl.
    def exitAxiom_decl(self, ctx:BoogieParser.Axiom_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#const_decl.
    def enterConst_decl(self, ctx:BoogieParser.Const_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#const_decl.
    def exitConst_decl(self, ctx:BoogieParser.Const_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#func_decl.
    def enterFunc_decl(self, ctx:BoogieParser.Func_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#func_decl.
    def exitFunc_decl(self, ctx:BoogieParser.Func_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#impl_decl.
    def enterImpl_decl(self, ctx:BoogieParser.Impl_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#impl_decl.
    def exitImpl_decl(self, ctx:BoogieParser.Impl_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#proc_decl.
    def enterProc_decl(self, ctx:BoogieParser.Proc_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#proc_decl.
    def exitProc_decl(self, ctx:BoogieParser.Proc_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#type_decl.
    def enterType_decl(self, ctx:BoogieParser.Type_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#type_decl.
    def exitType_decl(self, ctx:BoogieParser.Type_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#var_decl.
    def enterVar_decl(self, ctx:BoogieParser.Var_declContext):
        pass

    # Exit a parse tree produced by BoogieParser#var_decl.
    def exitVar_decl(self, ctx:BoogieParser.Var_declContext):
        pass


    # Enter a parse tree produced by BoogieParser#order_spec.
    def enterOrder_spec(self, ctx:BoogieParser.Order_specContext):
        pass

    # Exit a parse tree produced by BoogieParser#order_spec.
    def exitOrder_spec(self, ctx:BoogieParser.Order_specContext):
        pass


    # Enter a parse tree produced by BoogieParser#var_or_type.
    def enterVar_or_type(self, ctx:BoogieParser.Var_or_typeContext):
        pass

    # Exit a parse tree produced by BoogieParser#var_or_type.
    def exitVar_or_type(self, ctx:BoogieParser.Var_or_typeContext):
        pass


    # Enter a parse tree produced by BoogieParser#proc_sign.
    def enterProc_sign(self, ctx:BoogieParser.Proc_signContext):
        pass

    # Exit a parse tree produced by BoogieParser#proc_sign.
    def exitProc_sign(self, ctx:BoogieParser.Proc_signContext):
        pass


    # Enter a parse tree produced by BoogieParser#impl_body.
    def enterImpl_body(self, ctx:BoogieParser.Impl_bodyContext):
        pass

    # Exit a parse tree produced by BoogieParser#impl_body.
    def exitImpl_body(self, ctx:BoogieParser.Impl_bodyContext):
        pass


    # Enter a parse tree produced by BoogieParser#stmt_list.
    def enterStmt_list(self, ctx:BoogieParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by BoogieParser#stmt_list.
    def exitStmt_list(self, ctx:BoogieParser.Stmt_listContext):
        pass


    # Enter a parse tree produced by BoogieParser#local_vars.
    def enterLocal_vars(self, ctx:BoogieParser.Local_varsContext):
        pass

    # Exit a parse tree produced by BoogieParser#local_vars.
    def exitLocal_vars(self, ctx:BoogieParser.Local_varsContext):
        pass


    # Enter a parse tree produced by BoogieParser#spec.
    def enterSpec(self, ctx:BoogieParser.SpecContext):
        pass

    # Exit a parse tree produced by BoogieParser#spec.
    def exitSpec(self, ctx:BoogieParser.SpecContext):
        pass


    # Enter a parse tree produced by BoogieParser#modifies_spec.
    def enterModifies_spec(self, ctx:BoogieParser.Modifies_specContext):
        pass

    # Exit a parse tree produced by BoogieParser#modifies_spec.
    def exitModifies_spec(self, ctx:BoogieParser.Modifies_specContext):
        pass


    # Enter a parse tree produced by BoogieParser#requires_spec.
    def enterRequires_spec(self, ctx:BoogieParser.Requires_specContext):
        pass

    # Exit a parse tree produced by BoogieParser#requires_spec.
    def exitRequires_spec(self, ctx:BoogieParser.Requires_specContext):
        pass


    # Enter a parse tree produced by BoogieParser#ensures_spec.
    def enterEnsures_spec(self, ctx:BoogieParser.Ensures_specContext):
        pass

    # Exit a parse tree produced by BoogieParser#ensures_spec.
    def exitEnsures_spec(self, ctx:BoogieParser.Ensures_specContext):
        pass


    # Enter a parse tree produced by BoogieParser#label_or_cmd.
    def enterLabel_or_cmd(self, ctx:BoogieParser.Label_or_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#label_or_cmd.
    def exitLabel_or_cmd(self, ctx:BoogieParser.Label_or_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#transfer_cmd.
    def enterTransfer_cmd(self, ctx:BoogieParser.Transfer_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#transfer_cmd.
    def exitTransfer_cmd(self, ctx:BoogieParser.Transfer_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#structured_cmd.
    def enterStructured_cmd(self, ctx:BoogieParser.Structured_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#structured_cmd.
    def exitStructured_cmd(self, ctx:BoogieParser.Structured_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#assert_cmd.
    def enterAssert_cmd(self, ctx:BoogieParser.Assert_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#assert_cmd.
    def exitAssert_cmd(self, ctx:BoogieParser.Assert_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#assign_cmd.
    def enterAssign_cmd(self, ctx:BoogieParser.Assign_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#assign_cmd.
    def exitAssign_cmd(self, ctx:BoogieParser.Assign_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#assignment_lhs.
    def enterAssignment_lhs(self, ctx:BoogieParser.Assignment_lhsContext):
        pass

    # Exit a parse tree produced by BoogieParser#assignment_lhs.
    def exitAssignment_lhs(self, ctx:BoogieParser.Assignment_lhsContext):
        pass


    # Enter a parse tree produced by BoogieParser#assignment_lhs_indexed.
    def enterAssignment_lhs_indexed(self, ctx:BoogieParser.Assignment_lhs_indexedContext):
        pass

    # Exit a parse tree produced by BoogieParser#assignment_lhs_indexed.
    def exitAssignment_lhs_indexed(self, ctx:BoogieParser.Assignment_lhs_indexedContext):
        pass


    # Enter a parse tree produced by BoogieParser#assume_cmd.
    def enterAssume_cmd(self, ctx:BoogieParser.Assume_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#assume_cmd.
    def exitAssume_cmd(self, ctx:BoogieParser.Assume_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#break_cmd.
    def enterBreak_cmd(self, ctx:BoogieParser.Break_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#break_cmd.
    def exitBreak_cmd(self, ctx:BoogieParser.Break_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#call_cmd.
    def enterCall_cmd(self, ctx:BoogieParser.Call_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#call_cmd.
    def exitCall_cmd(self, ctx:BoogieParser.Call_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#goto_cmd.
    def enterGoto_cmd(self, ctx:BoogieParser.Goto_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#goto_cmd.
    def exitGoto_cmd(self, ctx:BoogieParser.Goto_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#havoc_cmd.
    def enterHavoc_cmd(self, ctx:BoogieParser.Havoc_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#havoc_cmd.
    def exitHavoc_cmd(self, ctx:BoogieParser.Havoc_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#if_cmd.
    def enterIf_cmd(self, ctx:BoogieParser.If_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#if_cmd.
    def exitIf_cmd(self, ctx:BoogieParser.If_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#label.
    def enterLabel(self, ctx:BoogieParser.LabelContext):
        pass

    # Exit a parse tree produced by BoogieParser#label.
    def exitLabel(self, ctx:BoogieParser.LabelContext):
        pass


    # Enter a parse tree produced by BoogieParser#par_call_cmd.
    def enterPar_call_cmd(self, ctx:BoogieParser.Par_call_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#par_call_cmd.
    def exitPar_call_cmd(self, ctx:BoogieParser.Par_call_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#return_cmd.
    def enterReturn_cmd(self, ctx:BoogieParser.Return_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#return_cmd.
    def exitReturn_cmd(self, ctx:BoogieParser.Return_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#while_cmd.
    def enterWhile_cmd(self, ctx:BoogieParser.While_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#while_cmd.
    def exitWhile_cmd(self, ctx:BoogieParser.While_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#yield_cmd.
    def enterYield_cmd(self, ctx:BoogieParser.Yield_cmdContext):
        pass

    # Exit a parse tree produced by BoogieParser#yield_cmd.
    def exitYield_cmd(self, ctx:BoogieParser.Yield_cmdContext):
        pass


    # Enter a parse tree produced by BoogieParser#call_params.
    def enterCall_params(self, ctx:BoogieParser.Call_paramsContext):
        pass

    # Exit a parse tree produced by BoogieParser#call_params.
    def exitCall_params(self, ctx:BoogieParser.Call_paramsContext):
        pass


    # Enter a parse tree produced by BoogieParser#void_call_params_remain.
    def enterVoid_call_params_remain(self, ctx:BoogieParser.Void_call_params_remainContext):
        pass

    # Exit a parse tree produced by BoogieParser#void_call_params_remain.
    def exitVoid_call_params_remain(self, ctx:BoogieParser.Void_call_params_remainContext):
        pass


    # Enter a parse tree produced by BoogieParser#ret_call_params_remain.
    def enterRet_call_params_remain(self, ctx:BoogieParser.Ret_call_params_remainContext):
        pass

    # Exit a parse tree produced by BoogieParser#ret_call_params_remain.
    def exitRet_call_params_remain(self, ctx:BoogieParser.Ret_call_params_remainContext):
        pass


    # Enter a parse tree produced by BoogieParser#guard.
    def enterGuard(self, ctx:BoogieParser.GuardContext):
        pass

    # Exit a parse tree produced by BoogieParser#guard.
    def exitGuard(self, ctx:BoogieParser.GuardContext):
        pass


    # Enter a parse tree produced by BoogieParser#r_type.
    def enterR_type(self, ctx:BoogieParser.R_typeContext):
        pass

    # Exit a parse tree produced by BoogieParser#r_type.
    def exitR_type(self, ctx:BoogieParser.R_typeContext):
        pass


    # Enter a parse tree produced by BoogieParser#type_args.
    def enterType_args(self, ctx:BoogieParser.Type_argsContext):
        pass

    # Exit a parse tree produced by BoogieParser#type_args.
    def exitType_args(self, ctx:BoogieParser.Type_argsContext):
        pass


    # Enter a parse tree produced by BoogieParser#type_atom.
    def enterType_atom(self, ctx:BoogieParser.Type_atomContext):
        pass

    # Exit a parse tree produced by BoogieParser#type_atom.
    def exitType_atom(self, ctx:BoogieParser.Type_atomContext):
        pass


    # Enter a parse tree produced by BoogieParser#map_type.
    def enterMap_type(self, ctx:BoogieParser.Map_typeContext):
        pass

    # Exit a parse tree produced by BoogieParser#map_type.
    def exitMap_type(self, ctx:BoogieParser.Map_typeContext):
        pass


    # Enter a parse tree produced by BoogieParser#exprs.
    def enterExprs(self, ctx:BoogieParser.ExprsContext):
        pass

    # Exit a parse tree produced by BoogieParser#exprs.
    def exitExprs(self, ctx:BoogieParser.ExprsContext):
        pass


    # Enter a parse tree produced by BoogieParser#proposition.
    def enterProposition(self, ctx:BoogieParser.PropositionContext):
        pass

    # Exit a parse tree produced by BoogieParser#proposition.
    def exitProposition(self, ctx:BoogieParser.PropositionContext):
        pass


    # Enter a parse tree produced by BoogieParser#expr.
    def enterExpr(self, ctx:BoogieParser.ExprContext):
        pass

    # Exit a parse tree produced by BoogieParser#expr.
    def exitExpr(self, ctx:BoogieParser.ExprContext):
        pass


    # Enter a parse tree produced by BoogieParser#equiv_op.
    def enterEquiv_op(self, ctx:BoogieParser.Equiv_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#equiv_op.
    def exitEquiv_op(self, ctx:BoogieParser.Equiv_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#implies_expr.
    def enterImplies_expr(self, ctx:BoogieParser.Implies_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#implies_expr.
    def exitImplies_expr(self, ctx:BoogieParser.Implies_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#implies_op.
    def enterImplies_op(self, ctx:BoogieParser.Implies_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#implies_op.
    def exitImplies_op(self, ctx:BoogieParser.Implies_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#explies_op.
    def enterExplies_op(self, ctx:BoogieParser.Explies_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#explies_op.
    def exitExplies_op(self, ctx:BoogieParser.Explies_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#logical_expr.
    def enterLogical_expr(self, ctx:BoogieParser.Logical_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#logical_expr.
    def exitLogical_expr(self, ctx:BoogieParser.Logical_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#and_op.
    def enterAnd_op(self, ctx:BoogieParser.And_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#and_op.
    def exitAnd_op(self, ctx:BoogieParser.And_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#or_op.
    def enterOr_op(self, ctx:BoogieParser.Or_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#or_op.
    def exitOr_op(self, ctx:BoogieParser.Or_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#rel_expr.
    def enterRel_expr(self, ctx:BoogieParser.Rel_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#rel_expr.
    def exitRel_expr(self, ctx:BoogieParser.Rel_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#rel_op.
    def enterRel_op(self, ctx:BoogieParser.Rel_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#rel_op.
    def exitRel_op(self, ctx:BoogieParser.Rel_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#bv_term.
    def enterBv_term(self, ctx:BoogieParser.Bv_termContext):
        pass

    # Exit a parse tree produced by BoogieParser#bv_term.
    def exitBv_term(self, ctx:BoogieParser.Bv_termContext):
        pass


    # Enter a parse tree produced by BoogieParser#term.
    def enterTerm(self, ctx:BoogieParser.TermContext):
        pass

    # Exit a parse tree produced by BoogieParser#term.
    def exitTerm(self, ctx:BoogieParser.TermContext):
        pass


    # Enter a parse tree produced by BoogieParser#add_op.
    def enterAdd_op(self, ctx:BoogieParser.Add_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#add_op.
    def exitAdd_op(self, ctx:BoogieParser.Add_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#factor.
    def enterFactor(self, ctx:BoogieParser.FactorContext):
        pass

    # Exit a parse tree produced by BoogieParser#factor.
    def exitFactor(self, ctx:BoogieParser.FactorContext):
        pass


    # Enter a parse tree produced by BoogieParser#mul_op.
    def enterMul_op(self, ctx:BoogieParser.Mul_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#mul_op.
    def exitMul_op(self, ctx:BoogieParser.Mul_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#power.
    def enterPower(self, ctx:BoogieParser.PowerContext):
        pass

    # Exit a parse tree produced by BoogieParser#power.
    def exitPower(self, ctx:BoogieParser.PowerContext):
        pass


    # Enter a parse tree produced by BoogieParser#unary_expr.
    def enterUnary_expr(self, ctx:BoogieParser.Unary_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#unary_expr.
    def exitUnary_expr(self, ctx:BoogieParser.Unary_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#neg_op.
    def enterNeg_op(self, ctx:BoogieParser.Neg_opContext):
        pass

    # Exit a parse tree produced by BoogieParser#neg_op.
    def exitNeg_op(self, ctx:BoogieParser.Neg_opContext):
        pass


    # Enter a parse tree produced by BoogieParser#coercion_expr.
    def enterCoercion_expr(self, ctx:BoogieParser.Coercion_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#coercion_expr.
    def exitCoercion_expr(self, ctx:BoogieParser.Coercion_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#array_expr.
    def enterArray_expr(self, ctx:BoogieParser.Array_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#array_expr.
    def exitArray_expr(self, ctx:BoogieParser.Array_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#indexed.
    def enterIndexed(self, ctx:BoogieParser.IndexedContext):
        pass

    # Exit a parse tree produced by BoogieParser#indexed.
    def exitIndexed(self, ctx:BoogieParser.IndexedContext):
        pass


    # Enter a parse tree produced by BoogieParser#atom_expr.
    def enterAtom_expr(self, ctx:BoogieParser.Atom_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#atom_expr.
    def exitAtom_expr(self, ctx:BoogieParser.Atom_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#bool_lit.
    def enterBool_lit(self, ctx:BoogieParser.Bool_litContext):
        pass

    # Exit a parse tree produced by BoogieParser#bool_lit.
    def exitBool_lit(self, ctx:BoogieParser.Bool_litContext):
        pass


    # Enter a parse tree produced by BoogieParser#nat.
    def enterNat(self, ctx:BoogieParser.NatContext):
        pass

    # Exit a parse tree produced by BoogieParser#nat.
    def exitNat(self, ctx:BoogieParser.NatContext):
        pass


    # Enter a parse tree produced by BoogieParser#dec.
    def enterDec(self, ctx:BoogieParser.DecContext):
        pass

    # Exit a parse tree produced by BoogieParser#dec.
    def exitDec(self, ctx:BoogieParser.DecContext):
        pass


    # Enter a parse tree produced by BoogieParser#decimal.
    def enterDecimal(self, ctx:BoogieParser.DecimalContext):
        pass

    # Exit a parse tree produced by BoogieParser#decimal.
    def exitDecimal(self, ctx:BoogieParser.DecimalContext):
        pass


    # Enter a parse tree produced by BoogieParser#dec_float.
    def enterDec_float(self, ctx:BoogieParser.Dec_floatContext):
        pass

    # Exit a parse tree produced by BoogieParser#dec_float.
    def exitDec_float(self, ctx:BoogieParser.Dec_floatContext):
        pass


    # Enter a parse tree produced by BoogieParser#bv_lit.
    def enterBv_lit(self, ctx:BoogieParser.Bv_litContext):
        pass

    # Exit a parse tree produced by BoogieParser#bv_lit.
    def exitBv_lit(self, ctx:BoogieParser.Bv_litContext):
        pass


    # Enter a parse tree produced by BoogieParser#old_expr.
    def enterOld_expr(self, ctx:BoogieParser.Old_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#old_expr.
    def exitOld_expr(self, ctx:BoogieParser.Old_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#arith_coercion_expr.
    def enterArith_coercion_expr(self, ctx:BoogieParser.Arith_coercion_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#arith_coercion_expr.
    def exitArith_coercion_expr(self, ctx:BoogieParser.Arith_coercion_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#paren_expr.
    def enterParen_expr(self, ctx:BoogieParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#paren_expr.
    def exitParen_expr(self, ctx:BoogieParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#forall_expr.
    def enterForall_expr(self, ctx:BoogieParser.Forall_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#forall_expr.
    def exitForall_expr(self, ctx:BoogieParser.Forall_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#exists_expr.
    def enterExists_expr(self, ctx:BoogieParser.Exists_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#exists_expr.
    def exitExists_expr(self, ctx:BoogieParser.Exists_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#lambda_expr.
    def enterLambda_expr(self, ctx:BoogieParser.Lambda_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#lambda_expr.
    def exitLambda_expr(self, ctx:BoogieParser.Lambda_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#forall.
    def enterForall(self, ctx:BoogieParser.ForallContext):
        pass

    # Exit a parse tree produced by BoogieParser#forall.
    def exitForall(self, ctx:BoogieParser.ForallContext):
        pass


    # Enter a parse tree produced by BoogieParser#exists.
    def enterExists(self, ctx:BoogieParser.ExistsContext):
        pass

    # Exit a parse tree produced by BoogieParser#exists.
    def exitExists(self, ctx:BoogieParser.ExistsContext):
        pass


    # Enter a parse tree produced by BoogieParser#r_lambda.
    def enterR_lambda(self, ctx:BoogieParser.R_lambdaContext):
        pass

    # Exit a parse tree produced by BoogieParser#r_lambda.
    def exitR_lambda(self, ctx:BoogieParser.R_lambdaContext):
        pass


    # Enter a parse tree produced by BoogieParser#quant_body.
    def enterQuant_body(self, ctx:BoogieParser.Quant_bodyContext):
        pass

    # Exit a parse tree produced by BoogieParser#quant_body.
    def exitQuant_body(self, ctx:BoogieParser.Quant_bodyContext):
        pass


    # Enter a parse tree produced by BoogieParser#bound_vars.
    def enterBound_vars(self, ctx:BoogieParser.Bound_varsContext):
        pass

    # Exit a parse tree produced by BoogieParser#bound_vars.
    def exitBound_vars(self, ctx:BoogieParser.Bound_varsContext):
        pass


    # Enter a parse tree produced by BoogieParser#qsep.
    def enterQsep(self, ctx:BoogieParser.QsepContext):
        pass

    # Exit a parse tree produced by BoogieParser#qsep.
    def exitQsep(self, ctx:BoogieParser.QsepContext):
        pass


    # Enter a parse tree produced by BoogieParser#if_then_else_expr.
    def enterIf_then_else_expr(self, ctx:BoogieParser.If_then_else_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#if_then_else_expr.
    def exitIf_then_else_expr(self, ctx:BoogieParser.If_then_else_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#code_expr.
    def enterCode_expr(self, ctx:BoogieParser.Code_exprContext):
        pass

    # Exit a parse tree produced by BoogieParser#code_expr.
    def exitCode_expr(self, ctx:BoogieParser.Code_exprContext):
        pass


    # Enter a parse tree produced by BoogieParser#spec_block.
    def enterSpec_block(self, ctx:BoogieParser.Spec_blockContext):
        pass

    # Exit a parse tree produced by BoogieParser#spec_block.
    def exitSpec_block(self, ctx:BoogieParser.Spec_blockContext):
        pass


    # Enter a parse tree produced by BoogieParser#attr_typed_idents_wheres.
    def enterAttr_typed_idents_wheres(self, ctx:BoogieParser.Attr_typed_idents_wheresContext):
        pass

    # Exit a parse tree produced by BoogieParser#attr_typed_idents_wheres.
    def exitAttr_typed_idents_wheres(self, ctx:BoogieParser.Attr_typed_idents_wheresContext):
        pass


    # Enter a parse tree produced by BoogieParser#attr_typed_idents_where.
    def enterAttr_typed_idents_where(self, ctx:BoogieParser.Attr_typed_idents_whereContext):
        pass

    # Exit a parse tree produced by BoogieParser#attr_typed_idents_where.
    def exitAttr_typed_idents_where(self, ctx:BoogieParser.Attr_typed_idents_whereContext):
        pass


    # Enter a parse tree produced by BoogieParser#typed_idents_wheres.
    def enterTyped_idents_wheres(self, ctx:BoogieParser.Typed_idents_wheresContext):
        pass

    # Exit a parse tree produced by BoogieParser#typed_idents_wheres.
    def exitTyped_idents_wheres(self, ctx:BoogieParser.Typed_idents_wheresContext):
        pass


    # Enter a parse tree produced by BoogieParser#typed_idents_where.
    def enterTyped_idents_where(self, ctx:BoogieParser.Typed_idents_whereContext):
        pass

    # Exit a parse tree produced by BoogieParser#typed_idents_where.
    def exitTyped_idents_where(self, ctx:BoogieParser.Typed_idents_whereContext):
        pass


    # Enter a parse tree produced by BoogieParser#typed_idents.
    def enterTyped_idents(self, ctx:BoogieParser.Typed_identsContext):
        pass

    # Exit a parse tree produced by BoogieParser#typed_idents.
    def exitTyped_idents(self, ctx:BoogieParser.Typed_identsContext):
        pass


    # Enter a parse tree produced by BoogieParser#idents.
    def enterIdents(self, ctx:BoogieParser.IdentsContext):
        pass

    # Exit a parse tree produced by BoogieParser#idents.
    def exitIdents(self, ctx:BoogieParser.IdentsContext):
        pass


    # Enter a parse tree produced by BoogieParser#type_params.
    def enterType_params(self, ctx:BoogieParser.Type_paramsContext):
        pass

    # Exit a parse tree produced by BoogieParser#type_params.
    def exitType_params(self, ctx:BoogieParser.Type_paramsContext):
        pass


    # Enter a parse tree produced by BoogieParser#attr.
    def enterAttr(self, ctx:BoogieParser.AttrContext):
        pass

    # Exit a parse tree produced by BoogieParser#attr.
    def exitAttr(self, ctx:BoogieParser.AttrContext):
        pass


    # Enter a parse tree produced by BoogieParser#attr_or_trigger.
    def enterAttr_or_trigger(self, ctx:BoogieParser.Attr_or_triggerContext):
        pass

    # Exit a parse tree produced by BoogieParser#attr_or_trigger.
    def exitAttr_or_trigger(self, ctx:BoogieParser.Attr_or_triggerContext):
        pass


    # Enter a parse tree produced by BoogieParser#attr_param.
    def enterAttr_param(self, ctx:BoogieParser.Attr_paramContext):
        pass

    # Exit a parse tree produced by BoogieParser#attr_param.
    def exitAttr_param(self, ctx:BoogieParser.Attr_paramContext):
        pass



del BoogieParser