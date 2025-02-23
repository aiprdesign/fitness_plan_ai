import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# --- Initialize session state ---
if "progress_data" not in st.session_state:
    st.session_state.progress_data = []

# --- Utility Functions ---
def cm_to_feet_inches(height_cm):
    inches = height_cm / 2.54
    feet = int(inches // 12)
    inches = int(inches % 12)
    return feet, inches

def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

def calculate_healthy_weight(height):
    return round(18.5 * ((height / 100) ** 2), 1), round(24.9 * ((height / 100) ** 2), 1)

def calculate_caloric_needs(age, weight, height, sex, activity_level, goal):
    """Calculates daily calorie needs based on activity level and fitness goal"""
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if sex == "Male" else -161)
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
    .bmi-good { background-color: #4CAF50; }  /* Green - Healthy */
    .bmi-warning { background-color: #FFA500; }  /* Orange - Overweight */
    .bmi-danger { background-color: #FF5733; }  /* Red - Obese */
    .bmi-low { background-color: #1E90FF; }  /* Blue - Underweight */
    .meter { width: 100%; height: 25px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ AI Health & Fitness Planner")

# --- User Profile Inputs ---
st.header("👤 Your Profile")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("🎂 Age", 10, 100, 30, 1)
    sex = st.radio("⚥ Gender", ["Male", "Female"])
    
with col2:
    weight = st.slider("⚖️ Weight (kg)", 30.0, 200.0, 70.0, 0.1)
    
with col3:
    height_cm = st.slider("📏 Height (cm)", 100.0, 250.0, 170.0, 0.1)
    feet, inches = cm_to_feet_inches(height_cm)

st.markdown(f"**📏 Height:** {height_cm} cm  /  {feet}'{inches}\"")

# --- Activity Level & Fitness Goals ---
st.subheader("🏃 Lifestyle & Goals")
activity_level = st.selectbox("🏋️ Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
fitness_goal = st.selectbox("🎯 Fitness Goal", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
daily_calories = calculate_caloric_needs(age, weight, height_cm, sex, activity_level, fitness_goal)
st.markdown(f"**🔥 Daily Caloric Needs:** {daily_calories} kcal")

# --- BMI & Weight Analysis ---
bmi = calculate_bmi(weight, height_cm)
healthy_weight_lower, healthy_weight_upper = calculate_healthy_weight(height_cm)

st.subheader("📈 Health Insights")
st.write(f"**Your BMI:** {bmi} 🏥")
st.write(f"**Healthy Weight Range:** {healthy_weight_lower} kg - {healthy_weight_upper} kg 🎯")

# --- BMI Gauge (Dynamic Color) ---
st.subheader("📊 BMI Gauge Meter")

bmi_category = "🔵 Underweight" if bmi < 18.5 else "🟢 Healthy" if bmi < 25 else "🟠 Overweight" if bmi < 30 else "🔴 Obese"
bmi_class = "bmi-low" if bmi < 18.5 else "bmi-good" if bmi < 25 else "bmi-warning" if bmi < 30 else "bmi-danger"

st.markdown(f"""
    <div class="bmi-gauge {bmi_class}">
        <meter min="10" max="40" value="{bmi}" class="meter"></meter><br>
        <span>{bmi_category}</span>
    </div>
""", unsafe_allow_html=True)

# --- Weight Progress Tracking ---
st.subheader("📊 Track Your Progress")
weight_today = st.number_input("🔄 Log Today's Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)

if st.button("📌 Log Weight"):
    st.session_state.progress_data.append({"date": datetime.today().strftime('%Y-%m-%d'), "weight": weight_today})
    st.success("✅ Weight logged successfully!")

if st.session_state.progress_data:
    df = pd.DataFrame(st.session_state.progress_data)
    st.line_chart(df.set_index("date"))

# --- AI-Powered Health Recommendations ---
st.subheader("💡 Personalized Tips")
if fitness_goal == "Lose Weight":
    st.info("✅ Focus on a **caloric deficit** and increase daily movement. Try strength training + cardio for best results!")
elif fitness_goal == "Gain Muscle":
    st.info("✅ Increase **protein intake** and focus on **progressive overload** in strength training.")
else:
    st.info("✅ Maintain a **balanced diet** and stick to a sustainable fitness routine!")

# --- Meditation Plan ---
st.subheader("🧘 Meditation & Pranayama Plan")
st.markdown("**🌅 Morning:** 5 min deep breathing + 5 min Alternate Nostril Breathing")
st.markdown("**☀️ Afternoon:** 5 min mindful meditation")
st.markdown("**🌙 Evening:** 10 min guided relaxation")

st.success("🎯 Your personalized health plan is ready! 🚀")
