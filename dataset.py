import pandas as pd

def get_jee_dataset():
    """
    Returns a high-fidelity dataset based on provided lecture data.
    Total Hours per chapter = Lecture Duration * 2 (1:1 Practice Ratio).
    """
    
    data = [
        # PHYSICS (Data from HH:MM:SS table provided by user)
        {"subject": "Physics", "topic": "Mathematical Tool", "lecture_hours": 23.43, "weightage": 0, "difficulty": 3},
        {"subject": "Physics", "topic": "Rectilinear Motion", "lecture_hours": 8.28, "weightage": 4, "difficulty": 4},
        {"subject": "Physics", "topic": "Projectile Motion", "lecture_hours": 6.06, "weightage": 4, "difficulty": 4},
        {"subject": "Physics", "topic": "Relative Motion", "lecture_hours": 7.18, "weightage": 4, "difficulty": 5},
        {"subject": "Physics", "topic": "Geometrical Optics", "lecture_hours": 29.77, "weightage": 12, "difficulty": 7},
        {"subject": "Physics", "topic": "Newton's Laws of Motion", "lecture_hours": 14.90, "weightage": 6, "difficulty": 5},
        {"subject": "Physics", "topic": "Friction", "lecture_hours": 7.94, "weightage": 2, "difficulty": 5},
        {"subject": "Physics", "topic": "Work Power Energy", "lecture_hours": 12.13, "weightage": 6, "difficulty": 5},
        {"subject": "Physics", "topic": "Circular Motion", "lecture_hours": 13.47, "weightage": 6, "difficulty": 6},
        {"subject": "Physics", "topic": "Centre Of Mass", "lecture_hours": 16.17, "weightage": 8, "difficulty": 7},
        {"subject": "Physics", "topic": "Rigid Body Dynamics", "lecture_hours": 21.38, "weightage": 12, "difficulty": 9},
        {"subject": "Physics", "topic": "SHM", "lecture_hours": 11.16, "weightage": 8, "difficulty": 7},
        {"subject": "Physics", "topic": "Electrostatics", "lecture_hours": 31.31, "weightage": 10, "difficulty": 7},
        {"subject": "Physics", "topic": "Gravitation", "lecture_hours": 8.51, "weightage": 4, "difficulty": 4},
        {"subject": "Physics", "topic": "Current Electricity", "lecture_hours": 17.47, "weightage": 10, "difficulty": 5},
        {"subject": "Physics", "topic": "Capacitance", "lecture_hours": 14.83, "weightage": 6, "difficulty": 6},
        {"subject": "Physics", "topic": "Electromagnetic Force", "lecture_hours": 26.74, "weightage": 8, "difficulty": 8},
        {"subject": "Physics", "topic": "Electromagnetic Induction", "lecture_hours": 15.87, "weightage": 10, "difficulty": 8},
        {"subject": "Physics", "topic": "Alternating Current", "lecture_hours": 6.93, "weightage": 4, "difficulty": 5},
        {"subject": "Physics", "topic": "Modern Physics - 1", "lecture_hours": 14.77, "weightage": 10, "difficulty": 4},
        {"subject": "Physics", "topic": "Modern Physics - 2", "lecture_hours": 8.60, "weightage": 8, "difficulty": 4},
        {"subject": "Physics", "topic": "Kinetic Theory Of Gases", "lecture_hours": 3.18, "weightage": 4, "difficulty": 4},
        {"subject": "Physics", "topic": "Thermodynamics", "lecture_hours": 7.02, "weightage": 8, "difficulty": 6},
        {"subject": "Physics", "topic": "Thermal Expansion & Calorimetry", "lecture_hours": 5.07, "weightage": 4, "difficulty": 4},
        {"subject": "Physics", "topic": "Fluid Mechanics", "lecture_hours": 10.42, "weightage": 6, "difficulty": 7},
        {"subject": "Physics", "topic": "Properties of Matter (Elastic/Visco/Surf)", "lecture_hours": 10.0, "weightage": 4, "difficulty": 5},
        {"subject": "Physics", "topic": "Wave On String", "lecture_hours": 9.99, "weightage": 6, "difficulty": 7},
        {"subject": "Physics", "topic": "Sound Wave", "lecture_hours": 6.81, "weightage": 6, "difficulty": 7},
        {"subject": "Physics", "topic": "Wave Optics", "lecture_hours": 9.40, "weightage": 6, "difficulty": 7},
        {"subject": "Physics", "topic": "Semiconductors & Communications", "lecture_hours": 8.23, "weightage": 4, "difficulty": 4},
        {"subject": "Physics", "topic": "Errors & Measurements", "lecture_hours": 7.31, "weightage": 4, "difficulty": 4},

        # CHEMISTRY (Physical & Inorganic)
        {"subject": "Chemistry", "topic": "Mole Concept", "lecture_hours": 9.20, "weightage": 4, "difficulty": 4},
        {"subject": "Chemistry", "topic": "Atomic Structure", "lecture_hours": 21.71, "weightage": 6, "difficulty": 5},
        {"subject": "Chemistry", "topic": "Quantum Mechanical Model", "lecture_hours": 5.31, "weightage": 4, "difficulty": 6},
        {"subject": "Chemistry", "topic": "Periodic Table", "lecture_hours": 8.84, "weightage": 6, "difficulty": 4},
        {"subject": "Chemistry", "topic": "Gaseous State & Real Gas", "lecture_hours": 20.51, "weightage": 6, "difficulty": 5},
        {"subject": "Chemistry", "topic": "Chemical Bonding", "lecture_hours": 22.10, "weightage": 12, "difficulty": 6},
        {"subject": "Chemistry", "topic": "Chemical Equilibrium", "lecture_hours": 8.73, "weightage": 6, "difficulty": 6},
        {"subject": "Chemistry", "topic": "Ionic Equilibrium", "lecture_hours": 16.44, "weightage": 10, "difficulty": 8},
        {"subject": "Chemistry", "topic": "Coordination Compounds", "lecture_hours": 13.73, "weightage": 10, "difficulty": 6},
        {"subject": "Chemistry", "topic": "Electrochemistry", "lecture_hours": 14.71, "weightage": 10, "difficulty": 7},
        {"subject": "Chemistry", "topic": "Metallurgy", "lecture_hours": 6.45, "weightage": 4, "difficulty": 5},
        {"subject": "Chemistry", "topic": "Qualitative Analysis", "lecture_hours": 14.90, "weightage": 8, "difficulty": 8},
        {"subject": "Chemistry", "topic": "P-Block Elements", "lecture_hours": 18.0, "weightage": 12, "difficulty": 6},
        {"subject": "Chemistry", "topic": "Chemical Kinetics", "lecture_hours": 11.16, "weightage": 8, "difficulty": 5},
        {"subject": "Chemistry", "topic": "Liquid Solution", "lecture_hours": 10.51, "weightage": 8, "difficulty": 5},
        {"subject": "Chemistry", "topic": "S-Block", "lecture_hours": 4.04, "weightage": 4, "difficulty": 4},
        {"subject": "Chemistry", "topic": "Solid State", "lecture_hours": 8.57, "weightage": 6, "difficulty": 5},
        {"subject": "Chemistry", "topic": "Thermodynamics (Chem)", "lecture_hours": 15.63, "weightage": 10, "difficulty": 8},
        {"subject": "Chemistry", "topic": "Equivalent Concept", "lecture_hours": 5.41, "weightage": 4, "difficulty": 6},
        {"subject": "Chemistry", "topic": "D & F Block", "lecture_hours": 6.11, "weightage": 6, "difficulty": 5},

        # CHEMISTRY (Organic)
        {"subject": "Chemistry", "topic": "IUPAC Nomenclature", "lecture_hours": 9.85, "weightage": 4, "difficulty": 4},
        {"subject": "Chemistry", "topic": "Structural ID & POC", "lecture_hours": 10.11, "weightage": 4, "difficulty": 5},
        {"subject": "Chemistry", "topic": "GOC 1 & 2", "lecture_hours": 22.17, "weightage": 12, "difficulty": 7},
        {"subject": "Chemistry", "topic": "Stereoisomerism", "lecture_hours": 19.38, "weightage": 10, "difficulty": 8},
        {"subject": "Chemistry", "topic": "Reaction Mechanisms (ORM 1-4)", "lecture_hours": 36.5, "weightage": 20, "difficulty": 8},
        {"subject": "Chemistry", "topic": "Reduction/Oxidation", "lecture_hours": 9.39, "weightage": 6, "difficulty": 6},
        {"subject": "Chemistry", "topic": "Aromatic Compounds", "lecture_hours": 8.23, "weightage": 10, "difficulty": 8},
        {"subject": "Chemistry", "topic": "Carbonyl Compounds", "lecture_hours": 8.13, "weightage": 10, "difficulty": 8},
        {"subject": "Chemistry", "topic": "Biomolecules & Polymers", "lecture_hours": 7.07, "weightage": 8, "difficulty": 5},

        # MATHEMATICS (Distributed 311 hours across topics)
        {"subject": "Mathematics", "topic": "Quadratic & Series", "lecture_hours": 25.0, "weightage": 8, "difficulty": 5},
        {"subject": "Mathematics", "topic": "Complex Numbers", "lecture_hours": 20.0, "weightage": 10, "difficulty": 8},
        {"subject": "Mathematics", "topic": "Binomial & P&C", "lecture_hours": 35.0, "weightage": 12, "difficulty": 8},
        {"subject": "Mathematics", "topic": "Probability", "lecture_hours": 25.0, "weightage": 12, "difficulty": 8},
        {"subject": "Mathematics", "topic": "Matrices & Determinants", "lecture_hours": 15.0, "weightage": 10, "difficulty": 5},
        {"subject": "Mathematics", "topic": "Straight Lines & Circles", "lecture_hours": 30.0, "weightage": 10, "difficulty": 6},
        {"subject": "Mathematics", "topic": "Conic Sections", "lecture_hours": 35.0, "weightage": 12, "difficulty": 7},
        {"subject": "Mathematics", "topic": "Functions & ITF", "lecture_hours": 30.0, "weightage": 10, "difficulty": 6},
        {"subject": "Mathematics", "topic": "Differential Calculus", "lecture_hours": 40.0, "weightage": 14, "difficulty": 7},
        {"subject": "Mathematics", "topic": "Integral Calculus", "lecture_hours": 45.0, "weightage": 16, "difficulty": 9},
        {"subject": "Mathematics", "topic": "Vectors & 3D Geometry", "lecture_hours": 21.0, "weightage": 12, "difficulty": 6},
    ]
    
    df = pd.DataFrame(data)
    
    # 1:1 Practice Rule: Total Hours = Lecture Hours * 2
    df['avg_hours_to_master'] = df['lecture_hours'] * 2
    
    # Keep the 75% Rule (25% undoable trap questions)
    df['doable_marks'] = df['weightage'] * 0.75
    
    return df
