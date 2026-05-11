from optimizer import optimize_study_plan
import pandas as pd

# Mock proficiency: Everything 0 except something that needs a prereq
# Rigid Body Dynamics needs Work Power Energy and Centre Of Mass
prof = {t: 0.0 for t in ["Work Power Energy", "Centre Of Mass", "Rigid Body Dynamics"]}

# Give plenty of time
res = optimize_study_plan(1000, prof)

print(f"Status: {res['status']}")
if res['status'] == 'Optimal':
    plan = res['study_plan']
    print("Topics in Plan:")
    print(plan[['Topic', 'Selection Reason']])
    
    rbd_in = "Rigid Body Dynamics" in plan['Topic'].values
    wpe_in = "Work Power Energy" in plan['Topic'].values
    com_in = "Centre Of Mass" in plan['Topic'].values
    
    print(f"Rigid Body Dynamics picked: {rbd_in}")
    print(f"Work Power Energy picked: {wpe_in}")
    print(f"Centre Of Mass picked: {com_in}")
    
    if rbd_in and (not wpe_in or not com_in):
        print("ERROR: Prerequisite logic FAILED!")
    else:
        print("SUCCESS: Prerequisite logic verified!")
