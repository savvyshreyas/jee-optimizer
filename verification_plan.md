# Formal Verification Checklist

## A. Mathematical Verification
- [ ] **Cost Formula**: Verify `(Lec/Speed) + (Lec * Multiplier)` across all subjects.
- [ ] **75% Cap**: Verify `Expected_Marks = Weightage * 0.75`.
- [ ] **Optimization Modes**: Verify both "Minimize Time" and "Maximize Marks" branches.

## B. Logical Verification
- [ ] **Iron Chain**: Verify recursive dependency inclusion (e.g., Vectors -> 3D Geometry).
- [ ] **Conflict Resolution**: Verify that prerequisites are never in the "Skip" list if a child is in "To-Do".

## C. Data Persistence
- [ ] **State Integrity**: Verify `user_data.json` accurately saves/loads proficiency sliders.

## D. UI/UX Integrity
- [ ] **Responsive Scaling**: Verify Streamlit layout at different screen sizes.
