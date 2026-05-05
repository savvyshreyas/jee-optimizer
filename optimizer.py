import pulp
import pandas as pd
from dataset import get_jee_dataset

def optimize_study_plan(total_hours_available, user_proficiencies, target_marks=None):
    """
    Solves the Knapsack/MILP problem to maximize marks within total_hours_available.
    
    Args:
        total_hours_available (float): Total study hours available.
        user_proficiencies (dict): Mapping of topic -> proficiency (0 to 1).
        target_marks (float, optional): If provided, it can act as a constraint or just be ignored if maximizing marks is the goal.
        
    Returns:
        dict: containing the optimal plan and stats.
    """
    df = get_jee_dataset()
    topics = df['topic'].tolist()
    
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
            costs[topic] = (1 - 0.8 * p) * row['avg_hours_to_master']
            values[topic] = row['doable_marks'] # Use 75% doable marks
            
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
            costs[topic] = (1 - 0.8 * p) * row['avg_hours_to_master']
            values[topic] = row['doable_marks'] # Use 75% doable marks
            
        # Objective function: Maximize total marks
        prob += pulp.lpSum([values[t] * y[t] for t in topics]), "Total Expected Marks"
        
        # Constraints: Total time cannot exceed available time
        prob += pulp.lpSum([costs[t] * y[t] for t in topics]) <= total_hours_available, "Total Time Constraint"
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        return {"status": "Failed to find optimal solution. Try increasing time."}
    
    # Extract results
    plan = []
    total_marks_expected = 0
    total_time_used = 0
    
    for t in topics:
        if pulp.value(y[t]) == 1.0:
            plan.append({
                "Topic": t,
                "Subject": df[df['topic'] == t]['subject'].values[0],
                "Weightage (Doable)": values[t],
                "Hours_Allocated": round(costs[t], 1),
                "Current_Proficiency": f"{user_proficiencies.get(t, 0.0)*100:.0f}%",
                "Action": "Revise" if user_proficiencies.get(t, 0.0) >= 0.8 else "Study Deeply"
            })
            total_marks_expected += values[t]
            total_time_used += costs[t]
            
    skipped = []
    for t in topics:
        if pulp.value(y[t]) == 0.0:
            skipped.append({
                "Topic": t,
                "Subject": df[df['topic'] == t]['subject'].values[0],
                "Weightage (Doable)": values[t],
                "Hours_Required": round(costs[t], 1),
                "Reason": "Low ROI / Too Time Consuming"
            })
            
    return {
        "status": "Optimal",
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
