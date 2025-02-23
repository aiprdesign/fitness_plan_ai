import streamlit as st
from datetime import datetime
import pandas as pd

# Function to convert height from cm to feet and inches
def cm_to_feet_inches(height_cm):
    inches = height_cm / 2.54
    feet = int(inches // 12)
    inches = int(inches % 12)
    return feet, inches

# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

# Function to calculate caloric needs
def calculate_caloric_needs(age, weight, height, sex, activity_level, fitness_goals):
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if sex == "Male" else -161)
    activity_multipliers = {
        "Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55,
        "Very Active": 1.725, "Extremely Active": 1.9
    }
    calories = bmr * activity_multipliers[activity_level]
    if fitness_goals == "Lose Weight":
        calories *= 0.85  # Reduce for weight loss
    elif fitness_goals == "Gain Muscle":
        calories *= 1.15  # Increase for muscle gain
    return round(calories)

# Function to generate diet plan
def generate_diet_plan(dietary_preferences, daily_calories):
    diet_map = {
        "Vegetarian": ["Oatmeal with nuts", "Lentil soup with salad", "Paneer curry with rice"],
        "Vegan": ["Smoothie bowl", "Quinoa salad", "Tofu stir-fry with veggies"],
        "Keto": ["Eggs and avocado", "Grilled chicken with greens", "Salmon with butter sauce"],
        "Low Carb": ["Greek yogurt", "Chicken and veggies", "Steak with broccoli"],
        "Gluten Free": ["Fruit salad", "Rice bowl with grilled fish", "Grilled meat with veggies"],
        "Dairy Free": ["Almond milk smoothie", "Quinoa with tofu", "Grilled chicken with sweet potatoes"]
    }
    return {
        "Breakfast": diet_map[dietary_preferences][0],
        "Lunch": diet_map[dietary_preferences][1],
        "Dinner": diet_map[dietary_preferences][2],
        "Daily Caloric Goal": f"{daily_calories} kcal"
    }

# Function to generate workout plan
def generate_workout_plan(fitness_goals, activity_level):
    workouts = {
        "Lose Weight": ["30 min jogging", "Full-body strength training", "Evening Yoga"],
        "Gain Muscle": ["Weightlifting (split routine)", "Protein-rich diet", "Active recovery"],
        "Endurance": ["Morning HIIT", "Cycling or swimming", "Evening stretching"],
        "Stay Fit": ["Daily 30 min walk", "Bodyweight exercises", "Mindfulness training"],
        "Strength Training": ["Powerlifting program", "Mobility drills", "Controlled cardio"]
    }
    return {
        "Morning": workouts[fitness_goals][0],
        "Afternoon": workouts[fitness_goals][1],
        "Evening": workouts[fitness_goals][2]
    }

# Function to generate meditation & pranayama plan
def generate_meditation_plan():
    return {
        "Morning": "5 min deep breathing + 5 min Alternate Nostril Breathing",
        "Afternoon": "5 min mindful meditation",
        "Evening": "10 min guided relaxation"
    }

# Initialize session state
if "progress_data" not in st.session_state:
    st.session_state.progress_data = []

st.markdown("""
    <style>
    .main { padding: 1rem; background-color: #1e1e1e; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4CAF50; color: white; font-weight: bold; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px; padding: 10px; background-color: #2d2d2d; color: #ffffff;
    }
    .info-box, .warning-box, .success-box {
        padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 0.5rem; color: #ffffff;
    }
    .info-box { background-color: #2d2d2d; border: 1px solid #87CEEB; }
    .warning-box { background-color: #4d2d2d; border: 1px solid #fbd38d; }
    .success-box { background-color: #2d4d2d; border: 1px solid #9ae6b4; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ AI Health & Wellness Planner")

# Sidebar for Progress Tracking
with st.sidebar:
    st.title("📊 Progress Tracker")
    weight_today = st.number_input("Today's Weight (kg)", min_value=20.0, max_value=300.0, step=0.1, value=70.0)
    if st.button("Log Weight"):
        st.session_state.progress_data.append({"date": datetime.today().strftime('%Y-%m-%d'), "weight": weight_today})
        st.success("Weight logged successfully!")
    if st.session_state.progress_data:
        progress_df = pd.DataFrame(st.session_state.progress_data)
        st.line_chart(progress_df.set_index("date"))

# User Profile Inputs
st.header("👤 Your Profile")
age = st.slider("Age", 10, 100, 30, 1)
weight = st.slider("Weight (kg)", 30.0, 200.0, 70.0, 0.1)
height_cm = st.slider("Height (cm)", 100.0, 250.0, 170.0, 0.1)
sex = st.radio("Gender", ["Male", "Female", "Other"])
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Vegan", "Keto", "Low Carb", "Gluten Free", "Dairy Free"])
fitness_goals = st.selectbox("Fitness Goals", ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"])

# Calculate BMI & Plans
bmi = calculate_bmi(weight, height_cm)
calories_needed = calculate_caloric_needs(age, weight, height_cm, sex, activity_level, fitness_goals)
diet_plan = generate_diet_plan(dietary_preferences, calories_needed)
workout_plan = generate_workout_plan(fitness_goals, activity_level)
meditation_plan = generate_meditation_plan()

st.subheader("📈 BMI Status")
st.write(f"Your BMI: **{bmi:.1f}**")

with st.expander("🍽️ Diet Plan", expanded=True):
    st.write(diet_plan)

with st.expander("💪 Workout Plan", expanded=True):
    st.write(workout_plan)

with st.expander("🧘‍♂️ Meditation & Pranayama", expanded=True):
    st.write(meditation_plan)

st.success("🎯 Your personalized health plan is ready!")
