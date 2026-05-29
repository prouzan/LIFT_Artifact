grammar Boogie;

boogie_program: (
		axiom_decl
		| const_decl
		| func_decl
		| impl_decl
		| proc_decl
		| type_decl
		| var_decl
	)*;
axiom_decl: 'axiom' attr* proposition ';';
const_decl:
	'const' attr* 'unique'? typed_idents order_spec? ';';
func_decl:
	'function' attr* Ident type_params? '(' (
		var_or_type ( ',' var_or_type)*
	)? ')' ('returns' '(' var_or_type ')' | ':' r_type) (
		'{' expr '}'
		| ';'
	);
impl_decl: 'implementation' proc_sign impl_body;
proc_decl: 'procedure' proc_sign ( ';' spec* | spec* impl_body);
type_decl:
	'type' attr* Ident Ident* ('=' r_type)? (
		',' Ident Ident* ( '=' r_type)?
	)* ';';
var_decl: 'var' attr* typed_idents_wheres ';';
order_spec:
	'extends' ('unique'? Ident ( ',' 'unique'? Ident)*)? 'complete'?;
var_or_type: attr* ( r_type | Ident ( ':' r_type)?);
proc_sign:
	attr* Ident type_params? '(' attr_typed_idents_wheres? ')' (
		'returns' '(' attr_typed_idents_wheres? ')'
	)?;
impl_body: '{' local_vars* stmt_list '}';
stmt_list: ( label_or_cmd | transfer_cmd | structured_cmd)*;
local_vars: 'var' attr* typed_idents_wheres ';';
spec: ( modifies_spec | requires_spec | ensures_spec);
modifies_spec: 'modifies' idents? ';';
requires_spec: 'free'? 'requires' attr* proposition ';';
ensures_spec: 'free'? 'ensures' attr* proposition ';';
label_or_cmd: (
		assert_cmd
		| assign_cmd
		| assume_cmd
		| call_cmd
		| havoc_cmd
		| label
		| par_call_cmd
		| yield_cmd
	);
transfer_cmd: ( goto_cmd | return_cmd);
structured_cmd: ( break_cmd | if_cmd | while_cmd);
assert_cmd: 'assert' attr* proposition ';';
assign_cmd: assignment_lhs (',' assignment_lhs)* ':=' exprs ';';
assignment_lhs: Ident assignment_lhs_indexed*;
assignment_lhs_indexed: '[' exprs? ']';
assume_cmd: 'assume' attr* proposition ';';
break_cmd: 'break' Ident? ';';
call_cmd: 'async'? 'free'? 'call' attr* call_params ';';
goto_cmd: 'goto' idents ';';
havoc_cmd: 'havoc' idents ';';
if_cmd:
	'if' guard '{' stmt_list '}' (
		'else' ( if_cmd | '{' stmt_list '}')
	)?;
label: Ident ':';
par_call_cmd: 'par' attr* call_params ( '|' call_params)* ';';
return_cmd: 'return' ';';
while_cmd:
	'while' guard ('free'? 'invariant' attr* expr ';')* '{' stmt_list '}';
yield_cmd: 'yield' ';';
call_params:
	Ident (
		void_call_params_remain
		| ret_call_params_remain
	);
void_call_params_remain: '(' exprs? ')';
ret_call_params_remain: ( ',' idents)? ':=' Ident '(' exprs? ')';
guard: '(' ( '*' | expr) ')';
r_type: ( type_atom | Ident type_args? | map_type);
type_args: ( type_atom type_args? | Ident type_args? | map_type);
type_atom: ( 'int' | 'real' | 'bool' | '(' r_type ')');
map_type: type_params? '[' ( r_type ( ',' r_type)*)? ']' r_type;
exprs: expr ( ',' expr)*;
proposition: expr;
expr: implies_expr ( equiv_op implies_expr)*;
equiv_op: ( '<==>' | '⇔');
implies_expr:
	logical_expr (
		implies_op implies_expr
		| explies_op logical_expr (explies_op logical_expr)*
	)?;
implies_op: ( '==>' | '⇒');
explies_op: ( '<==' | '⇐');
logical_expr:
	rel_expr (
		and_op rel_expr ( and_op rel_expr)*
		| or_op rel_expr ( or_op rel_expr)*
	)?;
and_op: ( '&&' | '∧');
or_op: ( '||' | '∨');
rel_expr: bv_term ( rel_op bv_term)?;
rel_op: (
		'=='
		| '<'
		| '>'
		| '<='
		| '>='
		| '!='
		| '<:'
		| '≠'
		| '≤'
		| '≥'
	);
bv_term: term ( '++' term)*;
term: factor ( add_op factor)*;
add_op: ( '+' | '-');
factor: power ( mul_op power)*;
mul_op: ( '*' | 'div' | 'mod' | '/');
power: unary_expr ( '**' power)?;
unary_expr: ('-' unary_expr | neg_op unary_expr | coercion_expr);
neg_op: ( '!' | '¬');
coercion_expr: array_expr ( ':' ( r_type | nat))*;
array_expr: atom_expr indexed*;
indexed: '[' ( exprs ( ':=' expr)? | ':=' expr)? ']';
atom_expr: (
		bool_lit
		| nat
		| dec
		| dec_float
		| bv_lit
		| Ident ( '(' ( exprs |) ')')?
		| old_expr
		| arith_coercion_expr
		| paren_expr
		| forall_expr
		| exists_expr
		| lambda_expr
		| if_then_else_expr
		| code_expr
	);
bool_lit: ('false' | 'true');
nat: Digits;
dec: ( decimal | dec_float);
decimal: Digits 'e' '-'? Digits;
dec_float: Digits '.' Digits ( 'e' '-'? Digits)?;
bv_lit: Digits 'bv' Digits;
old_expr: 'old' '(' expr ')';
arith_coercion_expr: ( 'int' '(' expr ')' | 'real' '(' expr ')');
paren_expr: '(' expr ')';
forall_expr: '(' forall quant_body ')';
exists_expr: '(' exists quant_body ')';
lambda_expr: '(' r_lambda quant_body ')';
forall: ( 'forall' | '∀');
exists: ( 'exists' | '∃');
r_lambda: ( 'lambda' | 'λ');
quant_body: (type_params bound_vars? | bound_vars) qsep attr_or_trigger* expr;
bound_vars: attr_typed_idents_wheres;
qsep: ( '::' | '•');
if_then_else_expr: 'if' expr 'then' expr 'else' expr;
code_expr: '|{' local_vars* spec_block spec_block* '}|';
spec_block:
	Ident ':' label_or_cmd* ('goto' idents | 'return' expr) ';';
attr_typed_idents_wheres:
	attr_typed_idents_where (',' attr_typed_idents_where)*;
attr_typed_idents_where: attr* typed_idents_where;
typed_idents_wheres:
	typed_idents_where (',' typed_idents_where)*;
typed_idents_where: typed_idents ( 'where' expr)?;
typed_idents: idents ':' r_type;
idents: Ident ( ',' Ident)*;
type_params: '<' idents '>';
attr: attr_or_trigger;
attr_or_trigger:
	'{' (':' Ident ( attr_param ( ',' attr_param)*)? | exprs) '}';
attr_param: ( String | expr);

String: '"' (String_char | '\\"')* '"';
Digits: Digit Digit*;
Ident: '\\'? Non_digit (Non_digit | Digit)*;

fragment Digit: [0-9];
fragment Non_digit: [A-Za-z'~#$^_.?`];
fragment String_char: ~["\r\n];

WS: [ \t\r\n]+ -> skip;
BlockComment: '/*' .*? '*/' -> skip;
LineComment: '//' ~[\r\n]* -> skip;