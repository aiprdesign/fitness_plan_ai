import streamlit as st
from datetime import datetime
import pandas as pd

# --- Initialize session state ---
if "progress_data" not in st.session_state:
    st.session_state.progress_data = []

# --- Utility Functions ---
def cm_to_feet_inches(height_cm):
    """Converts cm to feet and inches"""
    inches = height_cm / 2.54
    feet = int(inches // 12)
    inches = int(inches % 12)
    return feet, inches

def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

def calculate_healthy_weight(height):
    """Returns the lower and upper bounds of a healthy weight range"""
    return round(18.5 * ((height / 100) ** 2), 1), round(24.9 * ((height / 100) ** 2), 1)

def calculate_caloric_needs(age, weight, height, activity_level, goal):
    """Calculates daily calorie needs based on activity level and fitness goal"""
    bmr = (10 * weight) + (6.25 * height) - (5 * age)  
    activity_multipliers = {
        "Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55,
        "Very Active": 1.725, "Extremely Active": 1.9
    }
    calories = bmr * activity_multipliers[activity_level]
    if goal == "Lose Weight":
        calories -= 500
    elif goal == "Gain Muscle":
        calories += 500
    return round(calories)

# --- Modern UI & Styling ---
st.markdown("""
    <style>
    .bmi-gauge { text-align: center; font-size: 22px; font-weight: bold; padding: 10px; color: white; border-radius: 10px; }
    .bmi-good { background-color: #4CAF50; }  
    .bmi-warning { background-color: #FFA500; }  
    .bmi-danger { background-color: #FF5733; }  
    .bmi-low { background-color: #1E90FF; }  
    .meter { width: 100%; height: 25px; border-radius: 8px; }
    .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️ AI Health & Fitness Planner")

# --- User Profile Inputs ---
st.header("👤 Your Profile")
st.markdown("Enter your details to get a **personalized health plan**")

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Age", 10, 100, 30, 1)
    weight = st.slider("Weight (kg)", 30.0, 200.0, 70.0, 0.1)
    
with col2:
    height_cm = st.slider("Height (cm)", 100.0, 250.0, 170.0, 0.1)
    feet, inches = cm_to_feet_inches(height_cm)
    st.markdown(f"**Converted Height:** {feet} ft {inches} in")

# --- Activity Level & Fitness Goals ---
st.header("🏃 Lifestyle & Goals")
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
fitness_goal = st.selectbox("Fitness Goal", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
daily_calories = calculate_caloric_needs(age, weight, height_cm, activity_level, fitness_goal)
st.markdown(f"**Estimated Daily Calories:** {daily_calories} kcal")

# --- BMI & Weight Analysis ---
st.header("📈 Health Insights")
bmi = calculate_bmi(weight, height_cm)
healthy_weight_lower, healthy_weight_upper = calculate_healthy_weight(height_cm)

st.markdown(f"**Your BMI:** {bmi}")
st.markdown(f"**Healthy Weight Range:** {healthy_weight_lower} kg - {healthy_weight_upper} kg")

# --- BMI Gauge (Dynamic Color) ---
st.header("📊 BMI Gauge")

bmi_category = "🔵 Underweight" if bmi < 18.5 else "🟢 Healthy" if bmi < 25 else "🟠 Overweight" if bmi < 30 else "🔴 Obese"
bmi_class = "bmi-low" if bmi < 18.5 else "bmi-good" if bmi < 25 else "bmi-warning" if bmi < 30 else "bmi-danger"

st.markdown(f"""
    <div class="bmi-gauge {bmi_class}">
        <meter min="10" max="40" value="{bmi}" class="meter"></meter><br>
        <span>{bmi_category}</span>
    </div>
""", unsafe_allow_html=True)

# --- Weight Progress Tracking ---
st.header("📊 Weight Tracking")
weight_today = st.number_input("Log Today's Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)

if st.button("Log Weight"):
    st.session_state.progress_data.append({"date": datetime.today().strftime('%Y-%m-%d'), "weight": weight_today})
    st.success("Weight logged successfully!")

if st.session_state.progress_data:
    df = pd.DataFrame(st.session_state.progress_data)
    st.line_chart(df.set_index("date"))

# --- Personalized Diet Plan ---
st.header("🍽️ Your Personalized Diet Plan")
diet_choices = ["Vegetarian", "Vegan", "Keto", "Low Carb", "Gluten Free", "Dairy Free"]
dietary_preferences = st.selectbox("Select Your Diet Preference", diet_choices)

diet_plan = {
    "Vegetarian": ["Oatmeal with nuts", "Chickpea salad", "Lentil soup & rice"],
    "Vegan": ["Smoothie bowl", "Quinoa & spinach salad", "Tofu stir-fry"],
    "Keto": ["Scrambled eggs & avocado", "Grilled chicken & greens", "Salmon with butter sauce"],
    "Low Carb": ["Greek yogurt & almonds", "Chicken & steamed broccoli", "Steak with spinach"],
    "Gluten Free": ["Fruit & nuts", "Grilled fish & rice", "Chicken & roasted vegetables"],
    "Dairy Free": ["Almond milk smoothie", "Quinoa & tofu bowl", "Sweet potatoes & grilled chicken"]
}

st.write(f"**Breakfast:** {diet_plan[dietary_preferences][0]}")
st.write(f"**Lunch:** {diet_plan[dietary_preferences][1]}")
st.write(f"**Dinner:** {diet_plan[dietary_preferences][2]}")

# --- Workout Plan ---
st.header("💪 Workout Plan")
workout_plan = {
    "Lose Weight": ["30 min jogging", "Full-body strength exercises", "Evening Yoga"],
    "Gain Muscle": ["Weightlifting (4 sets of 8 reps)", "High protein intake", "Stretching & recovery"],
    "Maintain Weight": ["45 min brisk walk", "Bodyweight exercises", "Relaxation & deep breathing"]
}

st.write(f"**Morning:** {workout_plan[fitness_goal][0]}")
st.write(f"**Afternoon:** {workout_plan[fitness_goal][1]}")
st.write(f"**Evening:** {workout_plan[fitness_goal][2]}")

st.success("Your health plan is ready! 🎯")
