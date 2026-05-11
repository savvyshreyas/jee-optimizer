import pandas as pd

def get_jee_dataset():
    """
    Returns a high-fidelity dataset based on provided lecture data and prerequisites.
    Weightage = No. of Questions from User's latest JSON data.
    """
    
    data = [
        # PHYSICS (User's Final JSON Data)
        {"subject": "Physics", "topic": "Mathematical Tool", "lecture_hours": 23.43, "weightage": 2, "difficulty": 3, "prerequisites": []}, # Vector = 2
        {"subject": "Physics", "topic": "Rectilinear Motion", "lecture_hours": 8.28, "weightage": 4, "difficulty": 4, "prerequisites": []},
        {"subject": "Physics", "topic": "Projectile Motion", "lecture_hours": 6.06, "weightage": 8, "difficulty": 4, "prerequisites": []},
        {"subject": "Physics", "topic": "Relative Motion", "lecture_hours": 7.18, "weightage": 4, "difficulty": 5, "prerequisites": []},
        {"subject": "Physics", "topic": "Geometrical Optics", "lecture_hours": 29.77, "weightage": 58, "difficulty": 7, "prerequisites": []},
        {"subject": "Physics", "topic": "Newton's Laws of Motion", "lecture_hours": 14.90, "weightage": 9, "difficulty": 5, "prerequisites": []},
        {"subject": "Physics", "topic": "Friction", "lecture_hours": 7.94, "weightage": 6, "difficulty": 5, "prerequisites": ["Newton's Laws of Motion"]},
        {"subject": "Physics", "topic": "Work Power Energy", "lecture_hours": 12.13, "weightage": 11, "difficulty": 5, "prerequisites": []},
        {"subject": "Physics", "topic": "Circular Motion", "lecture_hours": 13.47, "weightage": 10, "difficulty": 6, "prerequisites": ["Work Power Energy"]},
        {"subject": "Physics", "topic": "Centre Of Mass", "lecture_hours": 16.17, "weightage": 19, "difficulty": 7, "prerequisites": ["Work Power Energy"]},
        {"subject": "Physics", "topic": "Rigid Body Dynamics", "lecture_hours": 21.38, "weightage": 52, "difficulty": 9, "prerequisites": ["Work Power Energy", "Centre Of Mass"]},
        {"subject": "Physics", "topic": "SHM", "lecture_hours": 11.16, "weightage": 17, "difficulty": 7, "prerequisites": []},
        {"subject": "Physics", "topic": "Gravitation", "lecture_hours": 8.51, "weightage": 17, "difficulty": 4, "prerequisites": ["Work Power Energy", "Circular Motion"]},
        {"subject": "Physics", "topic": "Electrostatics", "lecture_hours": 31.31, "weightage": 56, "difficulty": 7, "prerequisites": []},
        {"subject": "Physics", "topic": "Capacitance", "lecture_hours": 14.83, "weightage": 18, "difficulty": 6, "prerequisites": ["Electrostatics"]},
        {"subject": "Physics", "topic": "Current Electricity", "lecture_hours": 17.47, "weightage": 29, "difficulty": 5, "prerequisites": ["Electrostatics"]},
        {"subject": "Physics", "topic": "Electromagnetic Force", "lecture_hours": 26.74, "weightage": 44, "difficulty": 8, "prerequisites": ["Electrostatics", "Current Electricity"]}, # EMF
        {"subject": "Physics", "topic": "Electromagnetic Induction", "lecture_hours": 15.87, "weightage": 20, "difficulty": 8, "prerequisites": ["Electrostatics", "Electromagnetic Force", "Current Electricity"]}, # EMI
        {"subject": "Physics", "topic": "Alternating Current", "lecture_hours": 6.93, "weightage": 12, "difficulty": 5, "prerequisites": ["Electromagnetic Induction"]},
        {"subject": "Physics", "topic": "Modern Physics - 1", "lecture_hours": 14.77, "weightage": 42, "difficulty": 4, "prerequisites": []}, # Modern Phys
        {"subject": "Physics", "topic": "Modern Physics - 2", "lecture_hours": 8.60, "weightage": 32, "difficulty": 4, "prerequisites": ["Modern Physics - 1"]}, # Nuclear
        {"subject": "Physics", "topic": "Kinetic Theory Of Gases", "lecture_hours": 3.18, "weightage": 10, "difficulty": 4, "prerequisites": []}, # KTG part
        {"subject": "Physics", "topic": "Thermodynamics", "lecture_hours": 7.02, "weightage": 32, "difficulty": 6, "prerequisites": ["Kinetic Theory Of Gases"]}, # Thermo part
        {"subject": "Physics", "topic": "Thermal Expansion & Calorimetry", "lecture_hours": 5.07, "weightage": 21, "difficulty": 4, "prerequisites": []}, # Heat Transfer
        {"subject": "Physics", "topic": "Fluid Mechanics", "lecture_hours": 10.42, "weightage": 39, "difficulty": 7, "prerequisites": []}, # Fluid & Surface Tension
        {"subject": "Physics", "topic": "Elasticity", "lecture_hours": 3.32, "weightage": 9, "difficulty": 5, "prerequisites": ["Fluid Mechanics"]}, # Elasticity & Viscosity
        {"subject": "Physics", "topic": "Wave On String", "lecture_hours": 9.99, "weightage": 9, "difficulty": 7, "prerequisites": ["SHM"]}, # String Wave
        {"subject": "Physics", "topic": "Sound Wave", "lecture_hours": 6.81, "weightage": 24, "difficulty": 7, "prerequisites": ["Wave On String"]},
        {"subject": "Physics", "topic": "Wave Optics", "lecture_hours": 9.40, "weightage": 11, "difficulty": 7, "prerequisites": ["Sound Wave"]},
        {"subject": "Physics", "topic": "Semiconductors & Communications", "lecture_hours": 8.23, "weightage": 4, "difficulty": 4, "prerequisites": []},
        {"subject": "Physics", "topic": "Errors & Measurements", "lecture_hours": 7.31, "weightage": 25, "difficulty": 4, "prerequisites": []},

        # CHEMISTRY
        {"subject": "Chemistry", "topic": "Mole Concept", "lecture_hours": 9.20, "weightage": 15, "difficulty": 4, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Atomic Structure", "lecture_hours": 21.71, "weightage": 29, "difficulty": 5, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Periodic Table", "lecture_hours": 8.84, "weightage": 3, "difficulty": 4, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Chemical Bonding", "lecture_hours": 22.10, "weightage": 31, "difficulty": 6, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Gaseous State & Real Gas", "lecture_hours": 20.51, "weightage": 13, "difficulty": 5, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Thermodynamics (Chem)", "lecture_hours": 15.63, "weightage": 39, "difficulty": 8, "prerequisites": ["Gaseous State & Real Gas"]},
        {"subject": "Chemistry", "topic": "Chemical Equilibrium", "lecture_hours": 8.73, "weightage": 10, "difficulty": 6, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Ionic Equilibrium", "lecture_hours": 16.44, "weightage": 11, "difficulty": 8, "prerequisites": ["Chemical Equilibrium"]},
        {"subject": "Chemistry", "topic": "Electrochemistry", "lecture_hours": 14.71, "weightage": 34, "difficulty": 7, "prerequisites": ["Thermodynamics (Chem)", "Chemical Equilibrium"]},
        {"subject": "Chemistry", "topic": "Coordination Compounds", "lecture_hours": 13.73, "weightage": 42, "difficulty": 6, "prerequisites": ["Chemical Bonding"]},
        {"subject": "Chemistry", "topic": "Metallurgy", "lecture_hours": 6.45, "weightage": 23, "difficulty": 5, "prerequisites": []},
        {"subject": "Chemistry", "topic": "P-Block Elements", "lecture_hours": 18.0, "weightage": 62, "difficulty": 6, "prerequisites": []},
        {"subject": "Chemistry", "topic": "D & F Block", "lecture_hours": 6.11, "weightage": 11, "difficulty": 5, "prerequisites": []},
        {"subject": "Chemistry", "topic": "Salt Analysis", "lecture_hours": 14.90, "weightage": 37, "difficulty": 8, "prerequisites": ["P-Block Elements", "D & F Block"]},
        
        # Organic Chain
        {"subject": "Chemistry", "topic": "IUPAC Nomenclature", "lecture_hours": 9.85, "weightage": 25, "difficulty": 4, "prerequisites": []}, # IUPAC/Isomerism
        {"subject": "Chemistry", "topic": "Structural ID & POC", "lecture_hours": 10.11, "weightage": 10, "difficulty": 5, "prerequisites": ["IUPAC Nomenclature"]},
        {"subject": "Chemistry", "topic": "GOC 1 & 2", "lecture_hours": 22.17, "weightage": 12, "difficulty": 7, "prerequisites": ["Structural ID & POC"]},
        {"subject": "Chemistry", "topic": "Stereoisomerism", "lecture_hours": 19.38, "weightage": 10, "difficulty": 8, "prerequisites": ["GOC 1 & 2"]},
        {"subject": "Chemistry", "topic": "Reaction Mechanisms (ORM 1-4)", "lecture_hours": 36.5, "weightage": 39, "difficulty": 8, "prerequisites": ["Stereoisomerism"]}, # Hydrocarbons = 39
        {"subject": "Chemistry", "topic": "Reduction/Oxidation", "lecture_hours": 9.39, "weightage": 4, "difficulty": 6, "prerequisites": ["Reaction Mechanisms (ORM 1-4)"]}, # Redox = 4
        {"subject": "Chemistry", "topic": "Aromatic Compounds", "lecture_hours": 8.23, "weightage": 10, "difficulty": 8, "prerequisites": ["Reduction/Oxidation"]}, # Alkyl Halides = 10
        {"subject": "Chemistry", "topic": "Carbonyl Compounds", "lecture_hours": 8.13, "weightage": 65, "difficulty": 8, "prerequisites": ["Aromatic Compounds"]},
        {"subject": "Chemistry", "topic": "Biomolecules & Polymers", "lecture_hours": 7.07, "weightage": 20, "difficulty": 5, "prerequisites": ["Carbonyl Compounds"]}, # Biomolecules(14) + Polymers(6)

        # MATHEMATICS
        {"subject": "Mathematics", "topic": "Fundamentals of Math & Log", "lecture_hours": 12.0, "weightage": 6, "difficulty": 4, "prerequisites": []},
        {"subject": "Mathematics", "topic": "Quadratic Equations", "lecture_hours": 9.0, "weightage": 14, "difficulty": 5, "prerequisites": ["Fundamentals of Math & Log"]},
        {"subject": "Mathematics", "topic": "Sequence & Series", "lecture_hours": 9.0, "weightage": 27, "difficulty": 4, "prerequisites": []},
        {"subject": "Mathematics", "topic": "Trigonometric Ratios & Identity", "lecture_hours": 15.0, "weightage": 10, "difficulty": 6, "prerequisites": []},
        {"subject": "Mathematics", "topic": "Trigonometric Equations", "lecture_hours": 6.0, "weightage": 10, "difficulty": 6, "prerequisites": ["Trigonometric Ratios & Identity"]},
        {"subject": "Mathematics", "topic": "Solution of Triangles", "lecture_hours": 9.0, "weightage": 20, "difficulty": 7, "prerequisites": ["Trigonometric Ratios & Identity"]},
        {"subject": "Mathematics", "topic": "Straight Lines", "lecture_hours": 12.0, "weightage": 9, "difficulty": 5, "prerequisites": ["Fundamentals of Math & Log"]},
        {"subject": "Mathematics", "topic": "Circles", "lecture_hours": 9.0, "weightage": 34, "difficulty": 6, "prerequisites": ["Straight Lines"]},
        {"subject": "Mathematics", "topic": "Parabola", "lecture_hours": 7.5, "weightage": 31, "difficulty": 7, "prerequisites": ["Circles"]},
        {"subject": "Mathematics", "topic": "Ellipse & Hyperbola", "lecture_hours": 12.0, "weightage": 35, "difficulty": 8, "prerequisites": ["Parabola"]}, # 16+19
        {"subject": "Mathematics", "topic": "Permutations & Combinations", "lecture_hours": 12.0, "weightage": 23, "difficulty": 8, "prerequisites": []},
        {"subject": "Mathematics", "topic": "Binomial Theorem", "lecture_hours": 7.5, "weightage": 7, "difficulty": 7, "prerequisites": []},
        {"subject": "Mathematics", "topic": "Complex Numbers", "lecture_hours": 15.0, "weightage": 39, "difficulty": 9, "prerequisites": ["Quadratic Equations", "Trigonometric Ratios & Identity"]},
        {"subject": "Mathematics", "topic": "Matrices & Determinants", "lecture_hours": 12.0, "weightage": 46, "difficulty": 5, "prerequisites": []}, # 39+7
        {"subject": "Mathematics", "topic": "Functions & Relations", "lecture_hours": 15.0, "weightage": 10, "difficulty": 7, "prerequisites": []},
        {"subject": "Mathematics", "topic": "Inverse Trigonometric Functions", "lecture_hours": 7.5, "weightage": 12, "difficulty": 7, "prerequisites": ["Functions & Relations"]},
        {"subject": "Mathematics", "topic": "Limits, Continuity & Diff", "lecture_hours": 15.0, "weightage": 38, "difficulty": 8, "prerequisites": ["Functions & Relations"]}, # 20+18
        {"subject": "Mathematics", "topic": "Application of Derivatives", "lecture_hours": 15.0, "weightage": 44, "difficulty": 8, "prerequisites": ["Limits, Continuity & Diff"]},
        {"subject": "Mathematics", "topic": "Indefinite Integration", "lecture_hours": 15.0, "weightage": 5, "difficulty": 9, "prerequisites": ["Functions & Relations"]},
        {"subject": "Mathematics", "topic": "Definite Integration", "lecture_hours": 12.0, "weightage": 63, "difficulty": 9, "prerequisites": ["Indefinite Integration"]},
        {"subject": "Mathematics", "topic": "Area Under Curve", "lecture_hours": 6.0, "weightage": 18, "difficulty": 7, "prerequisites": ["Definite Integration"]},
        {"subject": "Mathematics", "topic": "Differential Equations", "lecture_hours": 7.5, "weightage": 25, "difficulty": 7, "prerequisites": ["Definite Integration"]},
        {"subject": "Mathematics", "topic": "Vectors", "lecture_hours": 9.0, "weightage": 37, "difficulty": 6, "prerequisites": []}, # Split 74
        {"subject": "Mathematics", "topic": "3D Geometry", "lecture_hours": 12.0, "weightage": 37, "difficulty": 7, "prerequisites": ["Vectors"]}, # Split 74
        {"subject": "Mathematics", "topic": "Probability", "lecture_hours": 15.0, "weightage": 50, "difficulty": 9, "prerequisites": ["Permutations & Combinations"]},
        {"subject": "Mathematics", "topic": "Statistics & Reasoning", "lecture_hours": 6.0, "weightage": 1, "difficulty": 3, "prerequisites": []}
    ]
    
    df = pd.DataFrame(data)
    df['avg_hours_to_master'] = df['lecture_hours'] * 2
    df['doable_marks'] = df['weightage'] * 0.75
    return df
