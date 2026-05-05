# JEE Advanced Preparation Optimizer

This document outlines the plan to build a "deep-tech" optimization algorithm that will help you achieve a top 2000 rank in JEE Advanced by strategically deciding what to study, what to skip, and how much time to allocate to each topic. 

The core idea is to treat your preparation as an **Optimization Problem**: you have limited resources (time, energy) and want to maximize your return (marks/rank) by investing in the highest-ROI (Return on Investment) topics based on your current strengths and weaknesses.

## User Review Required

> [!IMPORTANT]
> Please review this plan. This approach will use mathematical optimization to find the absolute most efficient path to your target rank.
> I suggest building this as a **Streamlit Web App**. It will give you a beautiful, interactive dashboard where you can use sliders to input your proficiency in different topics and instantly see the algorithm recalculate your optimal study plan.

## Open Questions

> [!WARNING]
> To tailor this perfectly to your situation, I need you to answer these questions:
> 1. **Time Available:** Approximately how many hours per day can you study, and how many days are left until the exam?
> 2. **Data Source:** I can generate a standard dataset of JEE Advanced topics, their historical weightage, and general difficulty. Do you want to use this, or do you have your own list of topics and weightages you want to use?
> 3. **Interface:** Does an interactive web dashboard (using Streamlit) sound good to you, or would you prefer a simple text-based script?

## Proposed Architecture & Algorithm

### 1. Data Structure (`data.json` or `topics.csv`)
We will create a comprehensive dataset of physics, chemistry, and math topics. Each topic will have:
- `subject`: Physics / Chemistry / Math
- `topic_name`: e.g., "Rotational Motion", "Electrostatics"
- `historical_weightage`: Average marks asked in the last 5-10 years.
- `base_difficulty`: General difficulty level (1-10).
- `dependencies`: Topics you must know before studying this one.

### 2. The Optimization Engine (`optimizer.py`)
This is the core "smart algorithm". We will likely use **Mixed Integer Linear Programming (MILP)** using a Python library like `PuLP` or `SciPy`.

**Variables:**
- `study_topic_i` (Boolean: 0 or 1): Whether to study topic $i$ or skip it entirely.
- `time_spent_i` (Continuous): Hours allocated to topic $i$.

**Objective Function:**
- **Maximize Expected Marks**, which is a function of:
  `sum(historical_weightage * f(time_spent, current_proficiency, difficulty))`
  *(We will use a logarithmic or diminishing returns curve to model that going from 0 to 80% proficiency is fast, but 80% to 100% takes much longer).*

**Constraints:**
- `Total Time Spent <= Max Available Time`
- `Expected Marks >= Target Marks` (Rank 2000 usually requires around 40-50% of total marks, depending on the year).
- Logical constraints (e.g., cannot allocate time if `study_topic` is 0).

### 3. Interactive Dashboard (`app.py`)
A Streamlit web application.
- **Sidebar:** Input your total available hours and target rank/marks.
- **Input Form/Table:** A quick way for you to rate your *current proficiency* (1-10) for major topics. If you are already a 9/10 in a high-weightage topic, the algorithm will tell you to just revise, not study from scratch. If you are a 2/10 in a hard, low-weightage topic, the algorithm will tell you to *skip it completely*.
- **Output:**
  - A definitive "Study List" vs "Skip List".
  - A pie chart or bar chart of time allocation per subject/topic.
  - Estimated final score based on the plan.

## Proposed Changes

### Core Engine
#### [NEW] `requirements.txt`
Dependencies like `streamlit`, `pandas`, `pulp` (for the math optimizer), `numpy`.
#### [NEW] `dataset.py`
To generate or load the base syllabus data and weightages.
#### [NEW] `optimizer.py`
The mathematical engine that formulates the Knapsack/MILP problem and solves it.
#### [NEW] `app.py`
The Streamlit frontend dashboard.

## Verification Plan

### Automated Tests
- Create dummy profiles (e.g., "Strong in Math, Weak in Physics", "Only 100 hours left") and verify that the optimizer outputs logical study plans (e.g., skips hard/low-weightage topics when time is low).
- Verify the mathematical constraints are never violated (time spent <= total time).

### Manual Verification
- Run the Streamlit app locally, input your actual current state, and review if the generated plan feels actionable and realistic to you. Adjust the "diminishing returns" mathematical curve until the time estimates feel accurate.
