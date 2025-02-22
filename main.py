import streamlit as st
from datetime import datetime
import pandas as pd

# Mock AI Agents (replace with actual Gemini API integration)
class DietaryExpert:
    def generate_plan(self, profile):
        return {
            "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
            "meal_plan": """
            **Breakfast**: Scrambled eggs with spinach and avocado.
            **Lunch**: Grilled chicken salad with quinoa and olive oil dressing.
            **Dinner**: Baked salmon with steamed broccoli and sweet potatoes.
            **Snacks**: Greek yogurt with berries and a handful of almonds.
            """,
            "important_considerations": """
            - Hydration: Drink plenty of water throughout the day.
            - Electrolytes: Monitor sodium, potassium, and magnesium levels.
            - Fiber: Ensure adequate intake through vegetables and fruits.
            - Listen to your body: Adjust portion sizes as needed.
            """
        }

class FitnessExpert:
    def generate_plan(self, profile):
        return {
            "goals": "Build strength, improve endurance, and maintain overall fitness",
            "routine": """
            **Warm-up**: 10 minutes of dynamic stretching.
            **Workout**:
            - Squats: 3 sets of 12 reps.
            - Push-ups: 3 sets of 15 reps.
            - Plank: 3 sets of 1 minute.
            **Cool-down**: 5 minutes of static stretching.
            """,
            "tips": """
            - Track your progress regularly.
            - Allow proper rest between workouts.
            - Focus on proper form.
            - Stay consistent with your routine.
            """
        }

# Initialize session state
if 'dietary_plan' not in st.session_state:
    st.session_state.dietary_plan = {}
if 'fitness_plan' not in st.session_state:
    st.session_state.fitness_plan = {}
if 'progress_data' not in st.session_state:
    st.session_state.progress_data = []
if 'qa_pairs' not in st.session_state:
    st.session_state.qa_pairs = []
if 'plans_generated' not in st.session_state:
    st.session_state.plans_generated = False

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
    }
    .stNumberInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
        padding: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f8ff;
        border: 1px solid #87CEEB;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API Key and Navigation
with st.sidebar:
    st.title("⚙️ Settings")
    gemini_api_key = st.text_input("Enter Gemini API Key", type="password", help="Required for AI functionality.")
    if not gemini_api_key:
        st.warning("Please enter your API key to proceed.")
        st.markdown("[Get your API key here](https://aistudio.google.com/apikey)")
    else:
        st.success("API Key accepted!")

    st.title("📊 Progress Tracker")
    weight_today = st.number_input("Today's Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
    if st.button("Log Weight"):
        if weight_today <= 0:
            st.error("Weight must be a positive number.")
        else:
            st.session_state.progress_data.append({
                "date": datetime.today().strftime('%Y-%m-%d'),
                "weight": weight_today
            })
            st.success("Weight logged successfully!")

    if st.session_state.progress_data:
        progress_df = pd.DataFrame(st.session_state.progress_data)
        st.line_chart(progress_df.set_index("date"))

# Main App
st.title("🏋️‍♂️ AI Health & Fitness Planner")
st.markdown("""
    <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
    Get personalized dietary and fitness plans tailored to your goals and preferences.
    Our AI-powered system considers your unique profile to create the perfect plan for you.
    </div>
""", unsafe_allow_html=True)

# User Profile Input
st.header("👤 Your Profile")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
    activity_level = st.selectbox(
        "Activity Level",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
    )
with col2:
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
    sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
    fitness_goals = st.selectbox(
        "Fitness Goals",
        options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"]
    )

# Generate Plans
if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
    if not gemini_api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    else:
        with st.spinner("Creating your perfect health and fitness routine..."):
            try:
                dietary_expert = DietaryExpert()
                fitness_expert = FitnessExpert()

                user_profile = f"""
                Age: {age}
                Weight: {weight}kg
                Height: {height}cm
                Sex: {sex}
                Activity Level: {activity_level}
                Fitness Goals: {fitness_goals}
                """

                st.session_state.dietary_plan = dietary_expert.generate_plan(user_profile)
                st.session_state.fitness_plan = fitness_expert.generate_plan(user_profile)
                st.session_state.plans_generated = True

                st.success("Plans generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display Plans
if st.session_state.plans_generated:
    st.header("📋 Your Personalized Plans")
    with st.expander("🍽️ Dietary Plan", expanded=True):
        st.markdown("### 🎯 Why this plan works")
        st.info(st.session_state.dietary_plan["why_this_plan_works"])
        st.markdown("### 🍽️ Meal Plan")
        st.write(st.session_state.dietary_plan["meal_plan"])
        st.markdown("### ⚠️ Important Considerations")
        for consideration in st.session_state.dietary_plan["important_considerations"].split('\n'):
            if consideration.strip():
                st.warning(consideration)

    with st.expander("💪 Fitness Plan", expanded=True):
        st.markdown("### 🎯 Goals")
        st.success(st.session_state.fitness_plan["goals"])
        st.markdown("### 🏋️‍♂️ Exercise Routine")
        st.write(st.session_state.fitness_plan["routine"])
        st.markdown("### 💡 Pro Tips")
        for tip in st.session_state.fitness_plan["tips"].split('\n'):
            if tip.strip():
                st.info(tip)

# Q&A Section
if st.session_state.plans_generated:
    st.header("❓ Questions about your plan?")
    question_input = st.text_input("Ask a question about your plan")
    if st.button("Get Answer"):
        if question_input:
            with st.spinner("Finding the best answer for you..."):
                try:
                    # Mock AI response (replace with Gemini API call)
                    answer = "This is a sample answer. Replace with actual AI response."
                    st.session_state.qa_pairs.append((question_input, answer))
                    st.success("Answer generated!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    if st.session_state.qa_pairs:
        st.header("💬 Q&A History")
        for q, a in st.session_state.qa_pairs:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
