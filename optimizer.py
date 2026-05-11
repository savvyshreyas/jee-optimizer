import pulp
import pandas as pd
from dataset import get_jee_dataset

def optimize_study_plan(total_hours_available, user_proficiencies, target_marks=None, lecture_speed=1.0):
    """
    Solves the Knapsack/MILP problem to maximize marks within total_hours_available.
    - cost = (Lecture_Hours / Speed) + Practice_Hours (where Practice = Lecture)
    """
    df = get_jee_dataset()
    topics = df['topic'].tolist()
    
    # Subject Difficulty Multipliers
    subj_multipliers = {"Mathematics": 1.5, "Physics": 1.2, "Chemistry": 1.0}
    
    # Check optimization mode
    if target_marks is not None and target_marks > 0:
        prob = pulp.LpProblem("JEE_Optimizer", pulp.LpMinimize)
        y = pulp.LpVariable.dicts("study", topics, cat='Binary')
        
        # Calculate costs and values
        costs = {}
        values = {}
        for idx, row in df.iterrows():
            topic = row['topic']
            p = user_proficiencies.get(topic, 0.0)
            
            # THE FORMULA: (Lec / Speed) + (Practice * Multiplier)
            multiplier = subj_multipliers.get(row['subject'], 1.0)
            rem_lec = row['lecture_hours'] * (1 - p)
            rem_prac = row['lecture_hours'] * (1 - p)
            costs[topic] = (rem_lec / lecture_speed) + (rem_prac * multiplier)
            
            values[topic] = row['doable_marks']
            
            # Prerequisite Constraints
            prereqs = row.get('prerequisites', [])
            for prereq in prereqs:
                if prereq in y:
                    prob += y[topic] <= y[prereq], f"Prereq_{topic}_{prereq}"
            
        # Objective function: Minimize total time
        prob += pulp.lpSum([costs[t] * y[t] for t in topics]), "Total Expected Time"
        
        # Constraints
        prob += pulp.lpSum([values[t] * y[t] for t in topics]) >= target_marks, "Target Marks Constraint"
        prob += pulp.lpSum([costs[t] * y[t] for t in topics]) <= total_hours_available, "Total Time Constraint"
        
    else:
        prob = pulp.LpProblem("JEE_Optimizer", pulp.LpMaximize)
        y = pulp.LpVariable.dicts("study", topics, cat='Binary')
        
        # Calculate costs and values
        costs = {}
        values = {}
        for idx, row in df.iterrows():
            topic = row['topic']
            p = user_proficiencies.get(topic, 0.0)
            
            multiplier = subj_multipliers.get(row['subject'], 1.0)
            rem_lec = row['lecture_hours'] * (1 - p)
            rem_prac = row['lecture_hours'] * (1 - p)
            costs[topic] = (rem_lec / lecture_speed) + (rem_prac * multiplier)
            
            values[topic] = row['doable_marks']

            # Prerequisite Constraints
            prereqs = row.get('prerequisites', [])
            for prereq in prereqs:
                if prereq in y:
                    prob += y[topic] <= y[prereq], f"Prereq_{topic}_{prereq}"
            
        # Objective function: Maximize total marks
        prob += pulp.lpSum([values[t] * y[t] for t in topics]), "Total Expected Marks"
        
        # Constraints: Total time cannot exceed available time
        prob += pulp.lpSum([costs[t] * y[t] for t in topics]) <= total_hours_available, "Total Time Constraint"
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # --- THE IRON CHAIN PROTOCOL ---
    # Normalize everything for matching (case-insensitive, stripped)
    topic_map_norm = {row['topic'].strip().lower(): row for _, row in df.iterrows()}
    # Mapping of lower -> original name
    original_name_map = {t.strip().lower(): t for t in topics}
    
    # Initial selection from solver
    initial_selection_lower = {t.strip().lower() for t in topics if pulp.value(y[t]) is not None and pulp.value(y[t]) > 0.5}
    final_selection_lower = set(initial_selection_lower)
    reasons = {original_name_map[t]: "High ROI / Marks" for t in initial_selection_lower}
    
    # Iteratively add all prerequisites until the list stabilizes
    while True:
        added_in_this_pass = False
        current_selection = list(final_selection_lower)
        for t_lower in current_selection:
            row = topic_map_norm.get(t_lower)
            if row is None: continue
            prereqs = row.get('prerequisites', [])
            for p in prereqs:
                p_lower = p.strip().lower()
                if p_lower not in final_selection_lower:
                    if p_lower in original_name_map:
                        orig_p = original_name_map[p_lower]
                        final_selection_lower.add(p_lower)
                        reasons[orig_p] = f"Mandatory Prerequisite for {original_name_map[t_lower]}"
                        added_in_this_pass = True
        if not added_in_this_pass:
            break
            
    final_selection_orig = {original_name_map[t_lower] for t_lower in final_selection_lower}
    
    if pulp.LpStatus[prob.status] != 'Optimal' and not final_selection_orig:
        return {"status": "Failed to find optimal solution. Try increasing time."}
    
    # Extract results
    plan = []
    total_marks_expected = 0
    total_time_used = 0
    
    for t in topics:
        t_clean = t.strip()
        if t in final_selection_orig:
            row = topic_map_norm[t.strip().lower()]
            p = user_proficiencies.get(t, 0.0)
            multiplier = subj_multipliers.get(row['subject'], 1.0)
            rem_lec = row['lecture_hours'] * (1 - p)
            rem_prac = row['lecture_hours'] * (1 - p)
            cost = (rem_lec / lecture_speed) + (rem_prac * multiplier)
            val = row['doable_marks']
            
            plan.append({
                "Topic": t,
                "Subject": row['subject'],
                "Weightage": val,
                "Hours": round(cost, 1),
                "Selection Reason": reasons.get(t, "Optimized Pick"),
                "Proficiency": f"{p*100:.0f}%",
                "Action": "Revise" if p >= 0.8 else "Study Deeply"
            })
            total_marks_expected += val
            total_time_used += cost
            
    skipped = []
    for t in topics:
        if t not in final_selection_orig:
            row = topic_map_norm[t.strip().lower()]
            p = user_proficiencies.get(t, 0.0)
            multiplier = subj_multipliers.get(row['subject'], 1.0)
            rem_lec = row['lecture_hours'] * (1 - p)
            rem_prac = row['lecture_hours'] * (1 - p)
            cost = (rem_lec / lecture_speed) + (rem_prac * multiplier)
            
            skipped.append({
                "Topic": t,
                "Subject": row['subject'],
                "Weightage": row['doable_marks'],
                "Hours_Required": round(cost, 1),
                "Reason": "ROI too low / Dependency not met"
            })
            
    return {
        "status": "Optimal" if final_selection_orig else "No topics selected",
        "total_marks_expected": total_marks_expected,
        "total_time_used": total_time_used,
        "study_plan": pd.DataFrame(plan),
        "skipped_topics": pd.DataFrame(skipped)
    }

if __name__ == "__main__":
    # Test
    prof = {"Kinematics": 0.9, "Laws of Motion & Friction": 0.5, "Work, Energy, Power": 0.8}
    res = optimize_study_plan(200, prof)
    print(f"Status: {res['status']}")
    print(f"Marks: {res.get('total_marks_expected')}")
    print(f"Time: {res.get('total_time_used')}")
