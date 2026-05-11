from optimizer import optimize_study_plan
from dataset import get_jee_dataset
import pandas as pd

def run_verification():
    print("--- STARTING DEEP-TECH VERIFICATION ---")
    
    df = get_jee_dataset()
    prof = {t: 0.0 for t in df['topic']}
    
    total_hours = 1500
    res = optimize_study_plan(total_hours, prof, lecture_speed=1.5)
    
    if res['status'] != 'Optimal':
        print("FAIL: Optimizer could not find a solution.")
        return

    plan = res['study_plan']
    topics_in_plan = set(plan['Topic'].tolist())
    
    # 1. Prerequisite Rule
    errors = []
    for idx, row in df.iterrows():
        topic = row['topic']
        if topic in topics_in_plan:
            for p in row['prerequisites']:
                if p not in topics_in_plan:
                    errors.append(f"VIOLATION: {topic} is in plan, but its prerequisite '{p}' is NOT.")
    
    if not errors:
        print("PASS: Prerequisite Logic Verified (No orphans found).")
    else:
        for e in errors: print(e)
        
    # 2. Time Formula: (Lec/1.5) + Lec
    rbd_row = plan[plan['Topic'] == 'Rigid Body Dynamics']
    if not rbd_row.empty:
        actual_hours = rbd_row['Hours'].values[0]
        expected_hours = round((21.38 / 1.5) + 21.38, 1)
        if abs(actual_hours - expected_hours) < 0.5:
            print(f"PASS: Time Calculation Verified ({actual_hours}h vs {expected_hours}h).")
        else:
            print(f"FAIL: Time Calculation Mismatch (Actual: {actual_hours}, Expected: {expected_hours}).")

    # 3. Skip List Integrity
    skipped = res['skipped_topics']['Topic'].tolist()
    orphans_in_skip = []
    for topic in topics_in_plan:
        row = df[df['topic'] == topic].iloc[0]
        for p in row['prerequisites']:
            if p in skipped:
                orphans_in_skip.append(f"VIOLATION: Prerequisite '{p}' found in SKIP list while child '{topic}' is in TODO.")

    if not orphans_in_skip:
        print("PASS: Zero Prerequisites in Skip List.")
    else:
        for e in orphans_in_skip: print(e)

    print("--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    run_verification()
