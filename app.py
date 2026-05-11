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

st.title("🚀 JEE Advanced Preparation Optimizer")
st.markdown("""
**Deep-Tech Strategy for AIR 2000.** 
Refined with **IITK Saathee** analysis principles:
- ✅ **Prerequisite Logic Enabled**: Topics are now sequenced logically.
- ✅ **75% Rule**: 25% of Advanced questions are designed to be "undoable".
- ✅ **Difficulty Hierarchy**: Math (1.5x) > Physics (1.2x) > Chemistry (1.0x).
""")

# Load dataset
df = get_jee_dataset()

# Sidebar for Global Constraints
st.sidebar.header("⏱️ Time Constraints")
st.sidebar.markdown(
    "How much time do you realistically have left? "
    "(e.g., 365 days * 6 hours = ~2190 hours)"
)
total_hours = st.sidebar.number_input("Total Study Hours Available", min_value=100, max_value=5000, value=1500, step=100)

st.sidebar.header("⏩ Study Efficiency")
lec_speed = st.sidebar.select_slider(
    "Lecture Watch Speed",
    options=[1.0, 1.25, 1.5, 1.75, 2.0],
    value=1.5
)

st.sidebar.header("🎯 Optimization Goal")
opt_mode = st.sidebar.radio(
    "Choose your strategy:",
    ("Minimize Effort to reach Target Rank", "Maximize Marks with Available Time")
)

target_marks = None
if opt_mode == "Minimize Effort to reach Target Rank":
    st.sidebar.markdown("Targeting AIR 2000 usually means getting around 150-160 marks.")
    target_marks = st.sidebar.number_input("Target Marks", min_value=50, max_value=360, value=160, step=10)
else:
    st.sidebar.markdown("We will maximize your expected marks for the time you have.")

# Tabs
tab1, tab2 = st.tabs(["📝 Input Proficiency", "🧠 AI Optimized Plan"])

# State for proficiencies
if 'proficiencies' not in st.session_state:
    stored_data = load_data()
    st.session_state.proficiencies = {topic: stored_data.get(topic, 0.0) for topic in df['topic']}

with tab1:
    st.header("Assess Your Current State")
    st.markdown("Rate your current knowledge in each topic (0% = completely new, 100% = JEE Advanced ready).")
    
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
    st.header("Your Deep-Tech Study Plan")
    
    if st.button("🚀 Generate Optimized Plan", type="primary"):
        # Save current state before generating
        save_data(st.session_state.proficiencies)
        
        with st.spinner("Solving MILP Optimization..."):
            res = optimize_study_plan(total_hours, st.session_state.proficiencies, target_marks=target_marks, lecture_speed=lec_speed)
            
        if res['status'] != "Optimal":
            st.error("Could not find an optimal solution. Try increasing your available time.")
        else:
            st.success(f"Plan Generated! Expected relative marks score: {res['total_marks_expected']} (out of ~360 max base)")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("✅ What to Study")
                st.dataframe(res['study_plan'], use_container_width=True)
                
            with col2:
                st.subheader("Time Allocation by Subject")
                if not res['study_plan'].empty:
                    fig = px.pie(res['study_plan'], values='Hours', names='Subject', hole=0.3)
                    st.plotly_chart(fig, use_container_width=True)
                    
            st.markdown("---")
            st.subheader("❌ What to Skip")
            st.markdown("Based on your time limit, these topics are mathematically not worth the effort right now.")
            st.dataframe(res['skipped_topics'], use_container_width=True)
            
            total_allocated = res['total_time_used']
            st.info(f"Total time required for this plan: {total_allocated:.1f} hours (out of {total_hours} available).")
