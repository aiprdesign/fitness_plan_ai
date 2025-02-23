import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

# Mock AI Agents (replace with actual API integration)
class DietaryExpert:
    def generate_plan(self, profile):
        age = profile.get("age", 45)
        weight = profile.get("weight", 90)
        height = profile.get("height", 167.64)
        dietary_preferences = profile.get("dietary_preferences", "Keto")
        fitness_goals = profile.get("fitness_goals", "Gain Muscle")

        return {
            "why_this_plan_works": f"Tailored for a {age}-year-old {profile.get('sex', 'Male')} weighing {weight}kg and {height}cm tall.",
            "meal_plan": f"""
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
        age = profile.get("age", 45)
        weight = profile.get("weight", 90)
        height = profile.get("height", 167.64)
        fitness_goals = profile.get("fitness_goals", "Gain Muscle")

        return {
            "goals": f"Build strength, improve endurance, and maintain overall fitness for a {age}-year-old.",
            "routine": f"""
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

# Function to generate a basic plan without AI
def generate_basic_plan(profile):
    age = profile.get("age", 45)
    weight = profile.get("weight", 90)
    height = profile.get("height", 167.64)
    sex = profile.get("sex", "Male")
    activity_level = profile.get("activity_level", "Moderately Active")
    dietary_preferences = profile.get("dietary_preferences", "Keto")
    fitness_goals = profile.get("fitness_goals", "Gain Muscle")

    # Basic meal plan
    meal_plan = """
    **Breakfast**: Scrambled eggs with spinach and avocado.
    **Lunch**: Grilled chicken salad with quinoa and olive oil dressing.
    **Dinner**: Baked salmon with steamed broccoli and sweet potatoes.
    **Snacks**: Greek yogurt with berries and a handful of almonds.
    """

    # Basic fitness routine
    fitness_routine = """
    **Warm-up**: 10 minutes of dynamic stretching.
    **Workout**:
    - Squats: 3 sets of 12 reps.
    - Push-ups: 3 sets of 15 reps.
    - Plank: 3 sets of 1 minute.
    **Cool-down**: 5 minutes of static stretching.
    """

    # Hydration and fasting tips
    hydration_tips = """
    - Drink at least 2-3 liters of water daily.
    - Start your day with a glass of water.
    - Avoid sugary drinks.
    """
    fasting_tips = """
    - Consider intermittent fasting (e.g., 16:8 method).
    - Avoid eating late at night.
    """

    return {
        "why_this_plan_works": f"Tailored for a {age}-year-old {sex} weighing {weight}kg and {height}cm tall.",
        "meal_plan": meal_plan,
        "fitness_routine": fitness_routine,
        "hydration_tips": hydration_tips,
        "fasting_tips": fasting_tips,
        "important_considerations": """
        - Hydration: Drink plenty of water throughout the day.
        - Electrolytes: Monitor sodium, potassium, and magnesium levels.
        - Fiber: Ensure adequate intake through vegetables and fruits.
        - Listen to your body: Adjust portion sizes as needed.
        """
    }

# Function to validate API key (placeholder)
def validate_api_key(api_key, api_provider):
    # Replace with actual API validation logic
    return True  # Placeholder

# Function to get age icon based on age
def get_age_icon(age):
    if age < 18:
        return "👦"  # Child
    elif 18 <= age < 40:
        return "👨"  # Young adult
    elif 40 <= age < 60:
        return "🧔"  # Middle-aged adult
    else:
        return "👴"  # Elderly person

# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

# Function to calculate healthy weight range
def calculate_healthy_weight(height):
    lower_range = 18.5 * ((height / 100) ** 2)
    upper_range = 24.9 * ((height / 100) ** 2)
    return lower_range, upper_range

# Function to calculate ideal weight based on height and age
def calculate_ideal_weight(height, age):
    # Simple formula for ideal weight (can be adjusted)
    ideal_weight = 50 + 0.9 * (height - 152)  # Adjusted for age
    if age > 40:
        ideal_weight *= 0.95  # Slightly lower ideal weight for older adults
    return ideal_weight

# Function to convert height from cm to feet and inches
def cm_to_feet_inches(height_cm):
    inches = height_cm / 2.54
    feet = int(inches // 12)
    inches = int(inches % 12)
    return feet, inches

# Function to convert height from feet and inches to cm
def feet_inches_to_cm(feet, inches):
    return (feet * 12 + inches) * 2.54

# Function to create a BMI gauge
def create_bmi_gauge(bmi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "BMI"},
        gauge={
            'axis': {'range': [10, 40]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [10, 18.5], 'color': "red"},
                {'range': [18.5, 25], 'color': "green"},
                {'range': [25, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))
    return fig

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

# Custom CSS for compact UI
st.markdown("""
    <style>
    .main {
        padding: 1rem;
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
        background-color: #fffaf        "age": age,
        "weight": weight,
        "height": height_cm,
        "sex": sex,
        "activity_level": activity_level,
        "dietary_preferences": dietary_preferences,
        "fitness_goals": fitness_goals
    }

    if use_ai and api_key:
        with st.spinner("Creating your perfect health and fitness routine using AI..."):
            try:
                dietary_expert = DietaryExpert()
                fitness_expert = FitnessExpert()

                st.session_state.dietary_plan = dietary_expert.generate_plan(user_profile)
                st.session_state.fitness_plan = fitness_expert.generate_plan(user_profile)
                st.session_state.plans_generated = True

                st.success("AI-generated plans created successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        with st.spinner("Creating your basic health and fitness routine..."):
            try:
                basic_plan = generate_basic_plan(user_profile)
                st.session_state.dietary_plan = {
                    "why_this_plan_works": basic_plan["why_this_plan_works"],
                    "meal_plan": basic_plan["meal_plan"],
                    "important_considerations": basic_plan["important_considerations"]
                }
                st.session_state.fitness_plan = {
                    "goals": "Achieve your fitness goals with this basic plan.",
                    "routine": basic_plan["fitness_routine"],
                    "tips": basic_plan["hydration_tips"] + "\n" + basic_plan["fasting_tips"]
                }
                st.session_state.plans_generated = True

                st.success("Basic plans created successfully!")
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

# Q&A Section (Limited to Fitness Plan)
if st.session_state.plans_generated:
    st.header("❓ Questions about your Fitness Plan?")
    question_input = st.text_input("Ask a question about your fitness plan")
    if st.button("Get Answer"):
        if question_input:
            with st.spinner("Finding the best answer for you..."):
                try:
                    # Mock AI response (replace with API call)
                    if "fitness" in question_input.lower() or "exercise" in question_input.lower():
                        answer = "Focus on proper form and consistency. Rest adequately between workouts."
                    else:
                        answer = "I can only answer questions related to your fitness plan."
                    st.session_state.qa_pairs.append((question_input, answer))
                    st.success("Answer generated!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    if st.session_state.qa_pairs:
        st.header("💬 Q&A History")
        for q, a in st.session_state.qa_pairs:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
