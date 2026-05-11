import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from dataset import get_jee_dataset
from optimizer import optimize_study_plan

USER_DATA_FILE = "user_data.json"

def save_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

st.set_page_config(page_title="JEE Advanced Optimizer", layout="wide")

# Navigation Sidebar
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["🧠 AI Optimizer", "🛠️ Manual Study Sandbox"])

# Global Constraints (Used by both pages)
st.sidebar.markdown("---")
st.sidebar.header("⏱️ Global Settings")
lec_speed = st.sidebar.select_slider(
    "Lecture Watch Speed",
    options=[1.0, 1.25, 1.5, 1.75, 2.0],
    value=1.5
)

# Load dataset
df = get_jee_dataset()
subj_multipliers = {"Mathematics": 1.5, "Physics": 1.2, "Chemistry": 1.0}

# State for proficiencies
if 'proficiencies' not in st.session_state:
    stored_data = load_data()
    st.session_state.proficiencies = {topic: stored_data.get(topic, 0.0) for topic in df['topic']}

if page == "🧠 AI Optimizer":
    st.title("🚀 JEE Advanced AI Optimizer")
    st.markdown("""
    **The strategic brain for AIR 2000.** Uses MILP (Mixed Integer Linear Programming) to find your perfect roadmap.
    """)

    # Sidebar for Global Constraints
    st.sidebar.header("Optimization Settings")
    total_hours = st.sidebar.number_input("Total Study Hours Available", min_value=100, max_value=5000, value=1500, step=100)
    
    opt_mode = st.sidebar.radio(
        "Choose your strategy:",
        ("Minimize Effort to reach Target Rank", "Maximize Marks with Available Time")
    )
    
    target_marks = None
    if opt_mode == "Minimize Effort to reach Target Rank":
        st.sidebar.markdown("Targeting AIR 2000 usually means getting around 150-160 marks.")
        target_marks = st.sidebar.number_input("Target Marks", min_value=50, max_value=360, value=160, step=10)
    
    # Tabs
    tab1, tab2 = st.tabs(["📝 Input Proficiency", "🧠 AI Optimized Plan"])
    
    with tab1:
        st.header("Assess Your Current State")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Physics")
            for topic in df[df['subject'] == 'Physics']['topic']:
                val = st.slider(topic, 0, 100, int(st.session_state.proficiencies[topic]*100), key=f"phys_{topic}")
                st.session_state.proficiencies[topic] = val / 100.0
        with col2:
            st.subheader("Chemistry")
            for topic in df[df['subject'] == 'Chemistry']['topic']:
                val = st.slider(topic, 0, 100, int(st.session_state.proficiencies[topic]*100), key=f"chem_{topic}")
                st.session_state.proficiencies[topic] = val / 100.0
        with col3:
            st.subheader("Mathematics")
            for topic in df[df['subject'] == 'Mathematics']['topic']:
                val = st.slider(topic, 0, 100, int(st.session_state.proficiencies[topic]*100), key=f"math_{topic}")
                st.session_state.proficiencies[topic] = val / 100.0

    with tab2:
        st.header("Your AI Generated Roadmap")
        if st.button("🚀 Generate Optimized Plan", type="primary"):
            save_data(st.session_state.proficiencies)
            with st.spinner("Solving Optimization..."):
                res = optimize_study_plan(total_hours, st.session_state.proficiencies, target_marks=target_marks, lecture_speed=lec_speed)
                
            if res['status'] != "Optimal":
                st.error("Could not find an optimal solution. Try increasing your available time.")
            else:
                st.success(f"Plan Generated! Expected marks: {res['total_marks_expected']:.1f}")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("✅ To-Do List")
                    st.dataframe(res['study_plan'], use_container_width=True)
                with col2:
                    st.subheader("Subject Allocation")
                    fig = px.pie(res['study_plan'], values='Hours', names='Subject', hole=0.3)
                    st.plotly_chart(fig, use_container_width=True)
                st.subheader("❌ Skip List")
                st.dataframe(res['skipped_topics'], use_container_width=True)

else:
    st.title("🛠️ Manual Study Sandbox")
    st.markdown("Cherry-pick your chapters. Calculations are now **stabilized** and lag-free.")
    
    # 1. Prepare/Cache the Base Data
    if 'base_sandbox_df' not in st.session_state:
        sandbox_df = df.copy()
        sandbox_df['Multiplier'] = sandbox_df['subject'].map(subj_multipliers)
        st.session_state.base_sandbox_df = sandbox_df

    # 2. Calculate personalized hours (Dynamic to speed and proficiency)
    # We do this every time to keep it live, but we optimize the df merge
    current_df = st.session_state.base_sandbox_df.copy()
    personalized_hours = []
    for idx, row in current_df.iterrows():
        p = st.session_state.proficiencies.get(row['topic'], 0.0)
        rem_lec = row['lecture_hours'] * (1 - p)
        rem_prac = row['lecture_hours'] * (1 - p)
        cost = (rem_lec / lec_speed) + (rem_prac * row['Multiplier'])
        personalized_hours.append(round(cost, 1))
    
    current_df['Net Study Hours'] = personalized_hours
    current_df['Exp. Marks'] = current_df['doable_marks'].round(1)
    
    # 3. Handle Selection State (The "Glitches" Fix)
    if 'manual_selection_set' not in st.session_state:
        st.session_state.manual_selection_set = set()

    # Create the display DF with checkboxes reflecting the set
    current_df.insert(0, 'Select', [t in st.session_state.manual_selection_set for t in current_df['topic']])
    
    display_df = current_df[[
        'Select', 'subject', 'topic', 'lecture_hours', 'Net Study Hours', 
        'weightage', 'Exp. Marks', 'prerequisites'
    ]].rename(columns={
        'subject': 'Subject', 'topic': 'Chapter', 'lecture_hours': 'Lec Hours',
        'weightage': 'Questions (16yr)', 'prerequisites': 'Prerequisites'
    })

    # 4. Interactive Data Editor
    st.subheader("Unified Strategy Table")
    edited_output = st.data_editor(
        display_df,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=True),
            "Lec Hours": st.column_config.NumberColumn(format="%.1f h"),
            "Net Study Hours": st.column_config.NumberColumn(format="%.1f h"),
            "Prerequisites": st.column_config.ListColumn()
        },
        disabled=["Subject", "Chapter", "Lec Hours", "Net Study Hours", "Questions (16yr)", "Exp. Marks", "Prerequisites"],
        hide_index=True,
        use_container_width=True,
        key="sandbox_editor_v2"
    )
    
    # Update the selection set based on the editor's output
    # This ensures that even after a rerun, the checkboxes stay checked
    new_selection = set(edited_output[edited_output['Select']]['Chapter'])
    if new_selection != st.session_state.manual_selection_set:
        st.session_state.manual_selection_set = new_selection
        st.rerun() # Single clean rerun to sync metrics
    
    # 5. Real-time Summary
    selected_data = edited_output[edited_output['Select']]
    total_h = selected_data['Net Study Hours'].sum()
    total_m = selected_data['Exp. Marks'].sum()
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Selected Chapters", len(st.session_state.manual_selection_set))
    c2.metric("Total Time Required", f"{total_h:.1f} hours")
    c3.metric("Expected Total Marks", f"{total_m:.1f}")
    
    if len(st.session_state.manual_selection_set) > 0:
        with st.expander("🔍 View Selected Sub-Totals by Subject"):
            subject_summary = selected_data.groupby('Subject')[['Net Study Hours', 'Exp. Marks']].sum()
            st.table(subject_summary)
    else:
        st.info("Select chapters from the table to see your customized roadmap summary.")
