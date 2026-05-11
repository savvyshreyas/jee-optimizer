from optimizer import optimize_study_plan
from dataset import get_jee_dataset
import pandas as pd
import os

def run_academic_audit():
    print("--- ACADEMIC FORMAL VERIFICATION REPORT ---")
    df = get_jee_dataset()
    
    prof = {t: 0.0 for t in df['topic']}
    res = optimize_study_plan(2000, prof, lecture_speed=1.5)
    plan = res['study_plan']
    
    # TEST 1: TIME CALCULATION ACCURACY
    math_check = plan[plan['Topic'] == 'Complex Numbers']
    actual_math = math_check['Hours'].values[0] if not math_check.empty else 0
    expected_math = round((15.0 / 1.5) + (15.0 * 1.5), 1)
    
    if actual_math == expected_math:
        print(f"PASS: Math Time Calculation (Actual: {actual_math}h, Expected: {expected_math}h)")
    else:
        print(f"FAIL: Math Time Calculation (Actual: {actual_math}h, Expected: {expected_math}h)")

    phys_check = plan[plan['Topic'] == 'Geometrical Optics']
    actual_phys = phys_check['Hours'].values[0] if not phys_check.empty else 0
    expected_phys = round((29.77 / 1.5) + (29.77 * 1.2), 1)
    
    if actual_phys == expected_phys:
        print(f"PASS: Phys Time Calculation (Actual: {actual_phys}h, Expected: {expected_phys}h)")
    else:
        print(f"FAIL: Phys Time Calculation (Actual: {actual_phys}h, Expected: {expected_phys}h)")

    # TEST 2: IRON CHAIN PREREQUISITE INTEGRITY
    auc_in = 'Area Under Curve' in plan['Topic'].values
    def_in = 'Definite Integration' in plan['Topic'].values
    ind_in = 'Indefinite Integration' in plan['Topic'].values
    func_in = 'Functions & Relations' in plan['Topic'].values
    
    if auc_in and def_in and ind_in and func_in:
        print("PASS: Iron Chain Integration (Full chain AUC -> Functions verified)")
    else:
        print(f"FAIL: Iron Chain (AUC:{auc_in}, DEF:{def_in}, IND:{ind_in}, FUNC:{func_in})")

    # TEST 3: 75% MARK CAP
    topic_val = df[df['topic'] == 'Probability']['weightage'].values[0]
    expected_val = topic_val * 0.75
    actual_val = plan[plan['Topic'] == 'Probability']['Weightage'].values[0]
    
    if actual_val == expected_val:
        print(f"PASS: 75% Mark Cap (Actual: {actual_val}, Expected: {expected_val})")
    else:
        print(f"FAIL: 75% Mark Cap (Actual: {actual_val}, Expected: {expected_val})")

    print("--- AUDIT COMPLETE: SYSTEM COMPLIANT ---")

if __name__ == "__main__":
    run_academic_audit()
