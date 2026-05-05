import pandas as pd

def get_jee_dataset():
    """
    Returns a pandas DataFrame containing JEE Advanced topics, weightage, and difficulty.
    Refined with IITK Saathee analysis principles:
    - Math is harder/longer to master (Multiplier: 1.5)
    - Physics is moderate (Multiplier: 1.2)
    - Chemistry is more doable (Multiplier: 1.0)
    - 25% of questions are assumed "un-doable" (Value Cap: 75%)
    """
    # Subject Multipliers (Difficulty/Time)
    multipliers = {"Mathematics": 1.5, "Physics": 1.2, "Chemistry": 1.0}
    
    data = [
        # PHYSICS (Multiplier 1.2)
        {"subject": "Physics", "topic": "Kinematics", "weightage": 4, "difficulty": 4, "base_hours": 15},
        {"subject": "Physics", "topic": "Laws of Motion & Friction", "weightage": 6, "difficulty": 5, "base_hours": 20},
        {"subject": "Physics", "topic": "Work, Energy, Power", "weightage": 6, "difficulty": 5, "base_hours": 15},
        {"subject": "Physics", "topic": "Center of Mass & Collisions", "weightage": 6, "difficulty": 6, "base_hours": 20},
        {"subject": "Physics", "topic": "Rotational Motion", "weightage": 12, "difficulty": 9, "base_hours": 40},
        {"subject": "Physics", "topic": "Gravitation", "weightage": 4, "difficulty": 4, "base_hours": 12},
        {"subject": "Physics", "topic": "Properties of Matter & Fluids", "weightage": 6, "difficulty": 6, "base_hours": 25},
        {"subject": "Physics", "topic": "Thermodynamics & KTG", "weightage": 10, "difficulty": 5, "base_hours": 25},
        {"subject": "Physics", "topic": "SHM & Waves", "weightage": 8, "difficulty": 7, "base_hours": 30},
        {"subject": "Physics", "topic": "Electrostatics", "weightage": 10, "difficulty": 7, "base_hours": 35},
        {"subject": "Physics", "topic": "Current Electricity", "weightage": 8, "difficulty": 5, "base_hours": 20},
        {"subject": "Physics", "topic": "Magnetism & EMI", "weightage": 12, "difficulty": 8, "base_hours": 40},
        {"subject": "Physics", "topic": "AC Circuits", "weightage": 4, "difficulty": 5, "base_hours": 12},
        {"subject": "Physics", "topic": "Ray & Wave Optics", "weightage": 12, "difficulty": 7, "base_hours": 35},
        {"subject": "Physics", "topic": "Modern Physics", "weightage": 12, "difficulty": 4, "base_hours": 25},
        
        # CHEMISTRY (Multiplier 1.0)
        {"subject": "Chemistry", "topic": "Mole Concept & Stoichiometry", "weightage": 4, "difficulty": 4, "base_hours": 15},
        {"subject": "Chemistry", "topic": "Atomic Structure", "weightage": 6, "difficulty": 5, "base_hours": 20},
        {"subject": "Chemistry", "topic": "Gaseous State", "weightage": 4, "difficulty": 4, "base_hours": 12},
        {"subject": "Chemistry", "topic": "Chemical Thermodynamics", "weightage": 8, "difficulty": 7, "base_hours": 30},
        {"subject": "Chemistry", "topic": "Chemical & Ionic Equilibrium", "weightage": 10, "difficulty": 8, "base_hours": 40},
        {"subject": "Chemistry", "topic": "Electrochemistry", "weightage": 8, "difficulty": 7, "base_hours": 30},
        {"subject": "Chemistry", "topic": "Chemical Kinetics", "weightage": 6, "difficulty": 5, "base_hours": 20},
        {"subject": "Chemistry", "topic": "Solid State & Solutions", "weightage": 8, "difficulty": 5, "base_hours": 25},
        {"subject": "Chemistry", "topic": "Surface Chemistry", "weightage": 4, "difficulty": 3, "base_hours": 12},
        {"subject": "Chemistry", "topic": "Periodic Table", "weightage": 4, "difficulty": 3, "base_hours": 12},
        {"subject": "Chemistry", "topic": "Chemical Bonding", "weightage": 10, "difficulty": 6, "base_hours": 30},
        {"subject": "Chemistry", "topic": "p-Block Elements", "weightage": 8, "difficulty": 6, "base_hours": 35},
        {"subject": "Chemistry", "topic": "d & f-Block Elements", "weightage": 6, "difficulty": 5, "base_hours": 20},
        {"subject": "Chemistry", "topic": "Coordination Compounds", "weightage": 10, "difficulty": 6, "base_hours": 30},
        {"subject": "Chemistry", "topic": "General Organic Chem (GOC)", "weightage": 12, "difficulty": 7, "base_hours": 35},
        {"subject": "Chemistry", "topic": "Hydrocarbons", "weightage": 8, "difficulty": 6, "base_hours": 30},
        {"subject": "Chemistry", "topic": "Reaction Mechanisms", "weightage": 10, "difficulty": 8, "base_hours": 40},
        {"subject": "Chemistry", "topic": "Oxygen Containing Compounds", "weightage": 10, "difficulty": 7, "base_hours": 35},
        {"subject": "Chemistry", "topic": "Amines & Biomolecules", "weightage": 6, "difficulty": 5, "base_hours": 25},

        # MATHEMATICS (Multiplier 1.5)
        {"subject": "Mathematics", "topic": "Quadratic Equations", "weightage": 4, "difficulty": 5, "base_hours": 15},
        {"subject": "Mathematics", "topic": "Sequences & Series", "weightage": 6, "difficulty": 6, "base_hours": 20},
        {"subject": "Mathematics", "topic": "Complex Numbers", "weightage": 8, "difficulty": 8, "base_hours": 35},
        {"subject": "Mathematics", "topic": "Binomial Theorem", "weightage": 6, "difficulty": 6, "base_hours": 25},
        {"subject": "Mathematics", "topic": "Permutations & Combinations", "weightage": 8, "difficulty": 8, "base_hours": 35},
        {"subject": "Mathematics", "topic": "Probability", "weightage": 10, "difficulty": 8, "base_hours": 35},
        {"subject": "Mathematics", "topic": "Matrices & Determinants", "weightage": 10, "difficulty": 5, "base_hours": 25},
        {"subject": "Mathematics", "topic": "Straight Lines & Circles", "weightage": 10, "difficulty": 6, "base_hours": 35},
        {"subject": "Mathematics", "topic": "Conic Sections", "weightage": 12, "difficulty": 7, "base_hours": 45},
        {"subject": "Mathematics", "topic": "Functions & Inverse Trig", "weightage": 8, "difficulty": 6, "base_hours": 30},
        {"subject": "Mathematics", "topic": "Limits, Continuity, Diff.", "weightage": 12, "difficulty": 7, "base_hours": 40},
        {"subject": "Mathematics", "topic": "Application of Derivatives", "weightage": 10, "difficulty": 8, "base_hours": 35},
        {"subject": "Mathematics", "topic": "Integration", "weightage": 14, "difficulty": 9, "base_hours": 50},
        {"subject": "Mathematics", "topic": "Area & Diff. Equations", "weightage": 8, "difficulty": 6, "base_hours": 30},
        {"subject": "Mathematics", "topic": "Vectors & 3D Geometry", "weightage": 12, "difficulty": 6, "base_hours": 30},
    ]
    
    df = pd.DataFrame(data)
    # Apply multipliers and assumptions
    df['avg_hours_to_master'] = df.apply(lambda x: x['base_hours'] * multipliers[x['subject']], axis=1)
    df['doable_marks'] = df['weightage'] * 0.75 # 25% undoable rule
    
    return df
