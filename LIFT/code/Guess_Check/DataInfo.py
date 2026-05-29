NLe_Dir = 'experiment/benchmarks-Instrumented'
Le_Dir = 'experiment/benchmarks-Instrumented-Lexicographic'
Tmp_Dir = 'experiment/tmp'
Test_Dir = 'experiment/test'
Fixed_Seed = 888

# All benchmark
Task_Info = [
        ('MenloPark_true-no-overflow_true-termination_true-valid-memsafety', ['x'], {'Test:Sp': lambda d: [d[0]* 99]}), # OK？ rand bug by z3?
        ('nonlin_mod_term_4', ['x', 'y']), # Result: ?
        ('c.07_true-termination_true-no-overflow', ['_i','j','k','tmp']),
        ('trex03_false-unreach-call_true-termination', ['x1', 'x2', 'x3']), # Result: ?
        ('trex03_false-unreach-call_true-termination-modif', ['x1', 'x2', 'x3', 'd1', 'd2', 'd3']), # Result: ?
        ('trex03_false-unreach-call_true-termination-simpl', ['x1','x2','x3']), # OK
        ('3pieces_Caterina_TACAS16_modif_3', ['x','y','N']), # OK
        ('4NestedWith2Variables_false-no-overflow', ['a','b']), # OK
        ('AliasDarteFeautrierGonnord-SAS2010-speedFails4_true-termination', ['x','n','b']), # OK
        ('AliasDarteFeautrierGonnord-SAS2010-wise_true-termination_true-no-overflow', ['x','y']), # OK
        ('aviad_true-termination_true-no-overflow', ['a']), # OK
        ('aviad_true-termination_true-no-overflow-version2', ['a']), # OK
        ('aviad_true-termination_true-no-overflow-version3', ['a']), # OK
        ('b.03-no-inv_assume_true-termination_true-no-overflow', ['x','y']), # OK
        ('b.10_true-termination_true-no-overflow', ['x','y']), # OK
        ('b.11_true-termination_true-no-overflow', ['x','y']), # OK
        ('b.11_true-termination_true-no-overflow-simpl', ['x','y']), # OK 
        ('BradleyMannaSipma-ICALP2005-Fig1_true-termination', ['x','y','N']), # OK
        ('c.07_true-termination_true-no-overflow-simpl', ['_i','j','k','tmp']),
        ('Cairo_true-no-overflow_true-termination_true-valid-memsafety', ['x']), # OK
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version3', ['x','y']), # OK
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.02_false-no-overflow', ['x']), # OK ？ rand bug by z3?
        ('ChenFlurMukhopadhyay-SAS2012-Ex2.13_true-termination', ['x','y']), # OK
        ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow-simpl', ['x','y','n']), # OK
        ('CookSeeZuleger-TACAS2013-Fig8a-modified_true-termination_true-no-overflow', ['K','x']), # OK
        ('Copenhagen_disj_true_version', ['x','y','z']), # OK
        ('Copenhagen_disj_true-termination_true-valid-memsafety', ['x','y']), # OK？ Rand Problem 
        ('Copenhagen_true-no-overflow_true-termination_true-valid-memsafety', ['x','y']), # OK
        ('determ_term_1', []), # determ 
        ('determ_term_2', []), # determ 
        ('determ_term_3', []), # determ 
        ('determ_term_4', []), # determ 
        ('determ_term_6', []), # determ 
        ('eca_bounded_core', ['limit']), # TO now
        ('ex1_false-no-overflow_true-termination', ['x','y']), # OK
        ('for_bounded_loop1_false-unreach-call_true-termination-simplified', ['n']), # OK
        ('Gothenburg_false-no-overflow', ['a','b','x','y'], {'Test:Eq': ['a','b']}), # OK？ Rand Problem 
        ('Gothenburg_v2_false-no-overflow', ['a','b','x','y'], {'Test:Sp': lambda d: [d[0], d[0] - 1] + d[-2:]}), # OK？ Rand Problem 
        ('Gothenburg_v3_false-no-overflow', ['a','b','x','y'], {'Test:Eq': ['a','b']}), # OK？ Rand Problem 
        ('Gothenburg_v4_false-no-overflow', ['a','b','x','y'], {'Test:Eq': ['a','b']}), # OK？ Rand Problem (Failed seed: 777)
        ('GulwaniJainKoskinen-PLDI2009-Fig1_true-termination', ['id','maxId']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig2_true-termination', ['y']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig2_true-termination-version', ['x','y']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig5_true-termination_true-no-overflow', ['x']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig5_true-termination_true-no-overflow-version', ['x']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig8_true-termination', ['x','y']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig8_true-termination-version', ['x','y']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig9_true-termination', ['x','y','z']), # OK
        ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig9_true-termination-version', ['x','y','z']), # OK
        ('java_AG313_true-termination_true-no-overflow', ['x','y']), # OK
        ('Lobnya-Boolean-Reordered_true-termination_true-valid-memsafety', ['x','b']), # OK
        ('min_rf-alloca_true-termination', ['x','y']), # OK
        ('Mysore_false-no-overflow', ['c','x']), # OK
        ('nonlin_div_term_1', ['x','y']), # OK
        ('nonlin_mod_term_1', ['x','y']), # OK
        ('nonlin_mod_term_2', ['x','y']), # OK
        ('nonlin_mult_term_1', ['y']), # OK CBC
        ('nonlin_mult_term_2', ['x','y']), # OK CBC
        ('nonlin_mult_term_3', ['x','y','z']), # OK CBC
        ('nonlin_mult_term_4', ['d','b']), # OK
        ('nonlin_mult_term_6', ['d','b']), # OK
        ('nonlin_mult_term_7', ['j','b']), # OK
        ('nonlin_mult_term_8', ['x','y','z']), # OK CBC
        ('nonlin_mult_term_9', ['j','b']), # OK
        ('Parallel_true-no-overflow_true-termination_true-valid-memsafety', ['x','y']), # OK
        ('Piecewise_true-no-overflow_true-termination_true-valid-memsafety', ['_i','j']), # OK
        ('PodelskiRybalchenko-LICS2004-Fig2_true-termination-modif1', ['x','y']), # OK 
        ('PodelskiRybalchenko-LICS2004-Fig2_true-termination-simpl', ['x','y']), # OK 
        ('PodelskiRybalchenko-VMCAI2004-Ex1_false-no-overflow', ['_i','j']), # OK
        ('PodelskiRybalchenko-VMCAI2004-Ex1_false-no-overflow-version', ['_i','j','_i1','j1']), # OK 
        ('Pure2Phase_true-termination_true-valid-memsafety', ['y','z']), # TO
        ('Singapore_false-no-overflow', ['x','y']), # OK
        ('Singapore_false-no-overflow-version', ['x','y']), # OK
        ('TelAviv-Amir-Minimum-alloca_true-termination', ['x','y']), # OK
        ('term_01', ['x','y']), # OK
        ('term_02', ['x','y','z']), # OK
        ('term_03', ['x','y','z']), # OK？ Rand Problem
        ('term_04', ['j','d']), # OK
        ('term_05', ['j','d']), # OK
        ('term_10', ['K','x','y']), # OK
        ('term_11', ['K','x','y']), # OK
        ('term_13', ['_i','j','k']), # OK
        ('term_14', ['_i','j','a','b']), # OK
        ('term_24', ['x','y','z']), # OK
        ('term_27', ['x','y']), # 
        ('term_28', ['x','y']), # OK
        ('Thun_false-no-overflow', ['x','y']), # OK
        ('3pieces_Caterina_TACAS16_modif_1', ['x','y']), # 
        ('3pieces_Caterina_TACAS16_modif_2', ['x','y']), # 
        ('3pieces_Caterina_TACAS16', ['x','y']), # OK
        ('4NestedWith3Variables_false-no-overflow', ['q','a','b']), # 
        ('aaron3_false-no-overflow-version', ['x','y','z','tx']), # 
        ('aaron3_false-no-overflow', ['x','y','z','tx']), # 
        ('aaron3_true-termination_true-valid-memsafety', ['x','y','z','tx']), # 
        ('AliasDarteFeautrierGonnord-SAS2010-speedpldi2_true-termination_true-no-overflow', ['n','m']), # 
        ('AliasDarteFeautrierGonnord-SAS2010-speedpldi3_true-termination_true-no-overflow', ['n','m']), # 
        ('aviad_true-termination_true-no-overflow-version1', ['a']), # OK
        ('Ben-Amram-2010LMCS-Ex2.3-alloca_true-termination-modified1', ['x','y','z']),
        ('determ_term_5', []), # determ 
        ('determ_term_7', []), # determ 
        ('determ_term_8', []), # determ 
        ('Et1_false-no-overflow_true-termination', ['a','b']),
        ('genady_true-termination_true-no-overflow', []),
        ('AliasDarteFeautrierGonnord-SAS2010-counterex1a_false-no-overflow', ['n', 'b', 'x', 'y']), # Result: ?
        ('AliasDarteFeautrierGonnord-SAS2010-cousot9_true-termination_true-no-overflow', ['j', 'N']), # Result: ?
        ('AliasDarteFeautrierGonnord-SAS2010-rsd_true-termination', ['_r']), # Result: ?
        ('Ben-Amram-2010LMCS-Ex2.3-alloca_true-termination', ['x', 'y', 'z']), # Result: ?
        ('Ben-Amram-2010LMCS-Ex2.3-alloca_true-termination-modified2', ['x', 'y', 'z']), # Result: ?
        ('ChawdharyCookGulwaniSagivYang-ESOP2008-aaron12_false-no-overflow', ['x', 'y', 'z']), # Result: ?
        ('ChawdharyCookGulwaniSagivYang-ESOP2008-aaron4_true-termination', ['_i', 'j', 'k', 'an', 'bn', 'tk']), # Result: ?
        ('ChawdharyCookGulwaniSagivYang-ESOP2008-aaron6_true-termination', ['x', 'tx', 'y', 'ty', 'n']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow', ['x']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version1', ['x']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version2', ['x']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version4', ['x', 'y']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version6', ['x', 'y']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex2.06_false-no-overflow', ['x', 'y']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow', ['x', 'y', 'z', 'n']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow-version1', ['x', 'y', 'z', 'n']), # Result: ?
        ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow-version2', ['x', 'y', 'z', 'n']), # Result: ?
        ('CookSeeZuleger-TACAS2013-Fig1_true-termination_true-no-overflow', ['x', 'y']), # Result: ?
        ('CookSeeZuleger-TACAS2013-Fig7a-true-termination_true-no-overflow', ['x', 'y', 'd']), # Result: ?
        ('CookSeeZuleger-TACAS2013-Fig7b-true-termination_true-no-overflow', ['x', 'y', 'z']), # Result: ?
        ('GulavaniGulwani-CAV2008-Fig1a_true-termination', ['x', 'y', 'z']), # Result: ?
        ('GulwaniJainKoskinen-PLDI2009-Fig1_true-termination-version1', ['id', 'maxId']), # Result: ?
        ('GulwaniJainKoskinen-PLDI2009-Fig1_true-termination-version2', ['id', 'maxId']), # Result: ?
        ('Masse-VMCAI2014-Fig1a_true-termination', ['a', 'b']), # Result: ?
        ('Masse-VMCAI2014-Fig1b_true-termination', ['x']), # Result: ?
        ('Masse-VMCAI2014-Fig1b_true-termination-version-1', ['x']), # Result: ?
        ('Masse-VMCAI2014-Fig1b_true-termination-version-2', ['x']), # Result: ?
        ('McCarthyIterative_true-termination_true-no-overflow', ['x']), # Result: ?
        ('MenloPark_true-no-overflow_true-termination_true-valid-memsafety-modif', ['x', 'y']), # Result: ?
        ('NoriSharma-2013FSE-Fig8-true-termination', ['x', 'y', 'z']), # Result: ?
        ('NoriSharma-2013FSE-Fig8-true-termination-modif', ['x', 'y', 'z']), # Result: ?
        ('Nyala-2lex_true-no-overflow_true-termination_true-valid-memsafety', ['x', 'y']), # Result: ?
        ('Nyala-2lex_true-no-overflow_true-termination_true-valid-memsafety-version', ['x', 'y']), # Result: ?
        ('PodelskiRybalchenko-LICS2004-Fig2_true-termination', ['x', 'y']), # Result: ?
        ('PodelskiRybalchenko-LICS2004-Fig2_true-termination-modif2', ['x', 'y']), # Result: ?
        ('PodelskiRybalchenko-TACAS2011-Fig4_true-termination_true-no-overflow', ['x', 'y']), # Result: ?
        ('PodelskiRybalchenko-simpl1', ['x', 'y']), # Result: ?
        ('PodelskiRybalchenko-simpl2', ['x', 'y']), # Result: ?
        ('PodelskiRybalchenko-simpl3', ['x', 'y']), # Result: ?
        ('Problem00_label00_true-unreach-call-toy', []), # Result: ?
        ('Pure2Phase_false-no-overflow', ['y', 'z']), # Result: ?
        ('Pure3Phase_false-no-overflow', ['x', 'y', 'z']), # Result: ?
        ('Toulouse-BranchesToLoop-alloca_true-termination', ['x', 'y', 'z']), # Result: ?
        ('UrbanMine-ESOP2014-Fig3_true-termination_true-no-overflow', ['x', 'y']), # Result: ?
        ('genady_true-termination_true-no-overflow-version', []), # Result: ?
        ('nonlin_div_term_2', ['x', 'y']), # Result: ?
        ('nonlin_jump_over_1_term', ['x', 'y']), # Result: ?
        ('nonlin_mod_term_3', ['x', 'y']), # Result: ?
        ('nonlin_mult_term_5', ['x', 'y']), # Result: ?
        ('term_06', []), # Result: ?
        ('term_07', ['x']), # Result: ?
        ('term_08', []), # Result: ?
        ('term_09', ['K', 'x', 'y']), # Result: ?
        ('term_12', []), # Result: ?
        ('term_15', ['x', 'y']), # Result: ?
        ('term_16', ['x', 'y']), # Result: ?
        ('term_17', []), # Result: ?
        ('term_18', []), # Result: ?
        ('term_19', ['x'], {'Test:Sp': lambda d: [d[0] * 10]}), # Result: ?
        ('term_20', []), # Result: ?
        ('term_21', ['z']), # Result: ?
        ('term_22', ['K', 'x', 'y']), # Result: ?
        ('term_23', ['x', 'y']), # Result: ?
        ('term_25', ['x', 'y', 'z']), # Result: ?
        ('term_26', ['x', 'y']), # Result: ?
        ('term_29', ['N']), # Result: ?
        ('transform_1', ['x', 'y']), # Result: ?
    ]

# No timeout for quick experiments
# Task_Info = [
#         ('3pieces_Caterina_TACAS16_modif_3', ['x','y','N']), # OK
#         ('4NestedWith2Variables_false-no-overflow', ['a','b']), # OK
#         ('AliasDarteFeautrierGonnord-SAS2010-speedFails4_true-termination', ['x','n','b']), # OK
#         ('AliasDarteFeautrierGonnord-SAS2010-wise_true-termination_true-no-overflow', ['x','y']), # OK
#         ('aviad_true-termination_true-no-overflow', ['a']), # OK
#         ('aviad_true-termination_true-no-overflow-version2', ['a']), # OK
#         ('aviad_true-termination_true-no-overflow-version3', ['a']), # OK
#         ('b.03-no-inv_assume_true-termination_true-no-overflow', ['x','y']), # OK
#         ('b.10_true-termination_true-no-overflow', ['x','y']), # OK
#         ('b.11_true-termination_true-no-overflow', ['x','y']), # OK
#         ('b.11_true-termination_true-no-overflow-simpl', ['x','y']), # OK 
#         ('BradleyMannaSipma-ICALP2005-Fig1_true-termination', ['x','y','N']), # OK
#         ('c.07_true-termination_true-no-overflow', ['_i','j','k','tmp']),
#         ('c.07_true-termination_true-no-overflow-simpl', ['_i','j','k','tmp']),
#         ('Cairo_true-no-overflow_true-termination_true-valid-memsafety', ['x']), # OK
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version3', ['x','y']), # OK
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.02_false-no-overflow', ['x']), # OK ？ rand bug by z3?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex2.13_true-termination', ['x','y']), # OK
#         ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow-simpl', ['x','y','n']), # OK
#         ('CookSeeZuleger-TACAS2013-Fig8a-modified_true-termination_true-no-overflow', ['K','x']), # OK
#         ('Copenhagen_disj_true_version', ['x','y','z']), # OK
#         ('Copenhagen_disj_true-termination_true-valid-memsafety', ['x','y']), # OK？ Rand Problem 
#         ('Copenhagen_true-no-overflow_true-termination_true-valid-memsafety', ['x','y']), # OK
#         ('determ_term_1', []), # determ 
#         ('determ_term_2', []), # determ 
#         ('determ_term_3', []), # determ 
#         ('determ_term_4', []), # determ 
#         ('determ_term_6', []), # determ 
#         # ('eca_bounded_core', ['limit']), # TO now
#         ('ex1_false-no-overflow_true-termination', ['x','y']), # OK
#         ('for_bounded_loop1_false-unreach-call_true-termination-simplified', ['n']), # OK
#         ('Gothenburg_false-no-overflow', ['a','b','x','y'], {'Test:Eq': ['a','b']}), # OK？ Rand Problem 
#         ('Gothenburg_v2_false-no-overflow', ['a','b','x','y'], {'Test:Sp': lambda d: [d[0], d[0] - 1] + d[-2:]}), # OK？ Rand Problem 
#         ('Gothenburg_v3_false-no-overflow', ['a','b','x','y'], {'Test:Eq': ['a','b']}), # OK？ Rand Problem 
#         ('Gothenburg_v4_false-no-overflow', ['a','b','x','y'], {'Test:Eq': ['a','b']}), # OK？ Rand Problem (Failed seed: 777)
#         # ('GulwaniJainKoskinen-PLDI2009-Fig1_true-termination', ['id','maxId']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig2_true-termination', ['y']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig2_true-termination-version', ['x','y']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig5_true-termination_true-no-overflow', ['x']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig5_true-termination_true-no-overflow-version', ['x']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig8_true-termination', ['x','y']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig8_true-termination-version', ['x','y']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig9_true-termination', ['x','y','z']), # OK
#         ('HeizmannHoenickeLeikePodelski-ATVA2013-Fig9_true-termination-version', ['x','y','z']), # OK
#         ('java_AG313_true-termination_true-no-overflow', ['x','y']), # OK
#         ('Lobnya-Boolean-Reordered_true-termination_true-valid-memsafety', ['x','b']), # OK
#         ('MenloPark_true-no-overflow_true-termination_true-valid-memsafety', ['x'], {'Test:Sp': lambda d: [d[0]* 99]}), # OK？ rand bug by z3?
#         ('min_rf-alloca_true-termination', ['x','y']), # OK
#         ('Mysore_false-no-overflow', ['c','x']), # OK
#         ('nonlin_div_term_1', ['x','y']), # OK
#         ('nonlin_mod_term_1', ['x','y']), # OK
#         ('nonlin_mod_term_2', ['x','y']), # OK
#         ('nonlin_mult_term_1', ['y']), # OK CBC
#         ('nonlin_mult_term_2', ['x','y']), # OK CBC
#         ('nonlin_mult_term_3', ['x','y','z']), # OK CBC
#         ('nonlin_mult_term_4', ['d','b']), # OK
#         ('nonlin_mult_term_6', ['d','b']), # OK
#         ('nonlin_mult_term_7', ['j','b']), # OK
#         ('nonlin_mult_term_8', ['x','y','z']), # OK CBC
#         ('nonlin_mult_term_9', ['j','b']), # OK
#         ('Parallel_true-no-overflow_true-termination_true-valid-memsafety', ['x','y']), # OK
#         ('Piecewise_true-no-overflow_true-termination_true-valid-memsafety', ['_i','j']), # OK
#         ('PodelskiRybalchenko-LICS2004-Fig2_true-termination-modif1', ['x','y']), # OK 
#         ('PodelskiRybalchenko-LICS2004-Fig2_true-termination-simpl', ['x','y']), # OK 
#         ('PodelskiRybalchenko-VMCAI2004-Ex1_false-no-overflow', ['_i','j']), # OK
#         ('PodelskiRybalchenko-VMCAI2004-Ex1_false-no-overflow-version', ['_i','j','_i1','j1']), # OK 
#         ('Pure2Phase_true-termination_true-valid-memsafety', ['y','z']), # TO
#         ('Singapore_false-no-overflow', ['x','y']), # OK
#         ('Singapore_false-no-overflow-version', ['x','y']), # OK
#         ('TelAviv-Amir-Minimum-alloca_true-termination', ['x','y']), # OK
#         ('term_01', ['x','y']), # OK
#         ('term_02', ['x','y','z']), # OK
#         ('term_03', ['x','y','z']), # OK？ Rand Problem
#         ('term_04', ['j','d']), # OK
#         ('term_05', ['j','d']), # OK
#         ('term_10', ['K','x','y']), # OK
#         ('term_11', ['K','x','y']), # OK
#         ('term_13', ['_i','j','k']), # OK
#         ('term_14', ['_i','j','a','b']), # OK
#         ('term_24', ['x','y','z']), # OK
#         ('term_27', ['x','y']), # 
#         ('term_28', ['x','y']), # OK
#         ('Thun_false-no-overflow', ['x','y']), # OK
#         ('trex03_false-unreach-call_true-termination-simpl', ['x1','x2','x3']), # OK
#         # ('3pieces_Caterina_TACAS16_modif_1', ['x','y']), # 
#         # ('3pieces_Caterina_TACAS16_modif_2', ['x','y']), # 
#         ('3pieces_Caterina_TACAS16', ['x','y']), # OK
#         # ('4NestedWith3Variables_false-no-overflow', ['q','a','b']), # 
#         # ('aaron3_false-no-overflow-version', ['x','y','z','tx']), # 
#         ('aaron3_false-no-overflow', ['x','y','z','tx']), # 
#         ('aaron3_true-termination_true-valid-memsafety', ['x','y','z','tx']), # 
#         ('AliasDarteFeautrierGonnord-SAS2010-speedpldi2_true-termination_true-no-overflow', ['n','m']), # 
#         # ('AliasDarteFeautrierGonnord-SAS2010-speedpldi3_true-termination_true-no-overflow', ['n','m']), # 
#         ('aviad_true-termination_true-no-overflow-version1', ['a']), # OK
#         ('Ben-Amram-2010LMCS-Ex2.3-alloca_true-termination-modified1', ['x','y','z']),
#         ('determ_term_5', []), # determ 
#         ('determ_term_7', []), # determ 
#         ('determ_term_8', []), # determ 
#         # ('Et1_false-no-overflow_true-termination', ['a','b']),
#         ('genady_true-termination_true-no-overflow', []),
#         # ('AliasDarteFeautrierGonnord-SAS2010-counterex1a_false-no-overflow', ['n', 'b', 'x', 'y']), # Result: ?
#         ('AliasDarteFeautrierGonnord-SAS2010-cousot9_true-termination_true-no-overflow', ['j', 'N']), # Result: ?
#         # ('AliasDarteFeautrierGonnord-SAS2010-rsd_true-termination', ['_r']), # Result: ?
#         ('Ben-Amram-2010LMCS-Ex2.3-alloca_true-termination', ['x', 'y', 'z']), # Result: ?
#         ('Ben-Amram-2010LMCS-Ex2.3-alloca_true-termination-modified2', ['x', 'y', 'z']), # Result: ?
#         # ('ChawdharyCookGulwaniSagivYang-ESOP2008-aaron12_false-no-overflow', ['x', 'y', 'z']), # Result: ?
#         # ('ChawdharyCookGulwaniSagivYang-ESOP2008-aaron4_true-termination', ['_i', 'j', 'k', 'an', 'bn', 'tk']), # Result: ?
#         ('ChawdharyCookGulwaniSagivYang-ESOP2008-aaron6_true-termination', ['x', 'tx', 'y', 'ty', 'n']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow', ['x']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version1', ['x']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version2', ['x']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version4', ['x', 'y']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex1.01_false-no-overflow-version6', ['x', 'y']), # Result: ?
#         # ('ChenFlurMukhopadhyay-SAS2012-Ex2.06_false-no-overflow', ['x', 'y']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow', ['x', 'y', 'z', 'n']), # Result: ?
#         ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow-version1', ['x', 'y', 'z', 'n']), # Result: ?
#         # ('ChenFlurMukhopadhyay-SAS2012-Ex4.01_false-no-overflow-version2', ['x', 'y', 'z', 'n']), # Result: ?
#         ('CookSeeZuleger-TACAS2013-Fig1_true-termination_true-no-overflow', ['x', 'y']), # Result: ?
#         ('CookSeeZuleger-TACAS2013-Fig7a-true-termination_true-no-overflow', ['x', 'y', 'd']), # Result: ?
#         # ('CookSeeZuleger-TACAS2013-Fig7b-true-termination_true-no-overflow', ['x', 'y', 'z']), # Result: ?
#         ('GulavaniGulwani-CAV2008-Fig1a_true-termination', ['x', 'y', 'z']), # Result: ?
#         # ('GulwaniJainKoskinen-PLDI2009-Fig1_true-termination-version1', ['id', 'maxId']), # Result: ?
#         # ('GulwaniJainKoskinen-PLDI2009-Fig1_true-termination-version2', ['id', 'maxId']), # Result: ?
#         # ('Masse-VMCAI2014-Fig1a_true-termination', ['a', 'b']), # Result: ?
#         ('Masse-VMCAI2014-Fig1b_true-termination', ['x']), # Result: ?
#         ('Masse-VMCAI2014-Fig1b_true-termination-version-1', ['x']), # Result: ?
#         ('Masse-VMCAI2014-Fig1b_true-termination-version-2', ['x']), # Result: ?
#         # ('McCarthyIterative_true-termination_true-no-overflow', ['x']), # Result: ?
#         ('MenloPark_true-no-overflow_true-termination_true-valid-memsafety-modif', ['x', 'y']), # Result: ?
#         ('NoriSharma-2013FSE-Fig8-true-termination', ['x', 'y', 'z']), # Result: ?
#         # ('NoriSharma-2013FSE-Fig8-true-termination-modif', ['x', 'y', 'z']), # Result: ?
#         ('Nyala-2lex_true-no-overflow_true-termination_true-valid-memsafety', ['x', 'y']), # Result: ?
#         ('Nyala-2lex_true-no-overflow_true-termination_true-valid-memsafety-version', ['x', 'y']), # Result: ?
#         ('PodelskiRybalchenko-LICS2004-Fig2_true-termination', ['x', 'y']), # Result: ?
#         # ('PodelskiRybalchenko-LICS2004-Fig2_true-termination-modif2', ['x', 'y']), # Result: ?
#         ('PodelskiRybalchenko-TACAS2011-Fig4_true-termination_true-no-overflow', ['x', 'y']), # Result: ?
#         ('PodelskiRybalchenko-simpl1', ['x', 'y']), # Result: ?
#         ('PodelskiRybalchenko-simpl2', ['x', 'y']), # Result: ?
#         ('PodelskiRybalchenko-simpl3', ['x', 'y']), # Result: ?
#         ('Problem00_label00_true-unreach-call-toy', []), # Result: ?
#         ('Pure2Phase_false-no-overflow', ['y', 'z']), # Result: ?
#         # ('Pure3Phase_false-no-overflow', ['x', 'y', 'z']), # Result: ?
#         # ('Toulouse-BranchesToLoop-alloca_true-termination', ['x', 'y', 'z']), # Result: ?
#         # ('UrbanMine-ESOP2014-Fig3_true-termination_true-no-overflow', ['x', 'y']), # Result: ?
#         ('genady_true-termination_true-no-overflow-version', []), # Result: ?
#         ('nonlin_div_term_2', ['x', 'y']), # Result: ?
#         # ('nonlin_jump_over_1_term', ['x', 'y']), # Result: ?
#         # ('nonlin_mod_term_3', ['x', 'y']), # Result: ?
#         ('nonlin_mod_term_4', ['x', 'y']), # Result: ?
#         # ('nonlin_mult_term_5', ['x', 'y']), # Result: ?
#         ('term_06', []), # Result: ?
#         ('term_07', ['x']), # Result: ?
#         ('term_08', []), # Result: ?
#         ('term_09', ['K', 'x', 'y']), # Result: ?
#         ('term_12', []), # Result: ?
#         ('term_15', ['x', 'y']), # Result: ?
#         # ('term_16', ['x', 'y']), # Result: ?
#         ('term_17', []), # Result: ?
#         ('term_18', []), # Result: ?
#         # ('term_19', ['x'], {'Test:Sp': lambda d: [d[0] * 10]}), # Result: ?
#         ('term_20', []), # Result: ?
#         # ('term_21', ['z']), # Result: ?
#         # ('term_22', ['K', 'x', 'y']), # Result: ?
#         # ('term_23', ['x', 'y']), # Result: ?
#         ('term_25', ['x', 'y', 'z']), # Result: ?
#         ('term_26', ['x', 'y']), # Result: ?
#         # ('term_29', ['N']), # Result: ?
#         # ('transform_1', ['x', 'y']), # Result: ?
#         ('trex03_false-unreach-call_true-termination', ['x1', 'x2', 'x3']), # Result: ?
#         ('trex03_false-unreach-call_true-termination-modif', ['x1', 'x2', 'x3', 'd1', 'd2', 'd3']), # Result: ?
#     ]
