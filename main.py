import streamlit as st
from datetime import datetime
import pandas as pd

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

def calculate_ideal_weight(height, age):
    ideal_weight = 50 + 0.9 * (height - 152)
    if age > 40:
        ideal_weight *= 0.95  
    return round(ideal_weight, 1)

# --- Modern UI & Styling ---
st.markdown("""
    <style>
    .main { padding: 1rem; background-color: #121212; color: white; font-family: 'Arial', sans-serif; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background: linear-gradient(45deg, #ff416c, #ff4b2b); color: white; font-weight: bold; border: none; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px; padding: 10px; background-color: #1e1e1e; color: white; border: 1px solid #ff416c;
    }
    .info-box { padding: 10px; border-radius: 10px; background-color: #2d2d2d; border: 1px solid #87CEEB; margin-bottom: 10px; color: white; }
    .warning-box { padding: 10px; border-radius: 10px; background-color: #4d2d2d; border: 1px solid #fbd38d; margin-bottom: 10px; color: white; }
    .success-box { padding: 10px; border-radius: 10px; background-color: #2d4d2d; border: 1px solid #9ae6b4; margin-bottom: 10px; color: white; }
    .stExpander { border-radius: 10px; background: linear-gradient(45deg, #1e1e1e, #333); color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ AI Health & Fitness Planner")

# --- User Profile Inputs ---
st.header("👤 Your Profile")
age = st.slider("🎂 Age", 10, 100, 30, 1)
weight = st.slider("⚖️ Weight (kg)", 30.0, 200.0, 70.0, 0.1)
height_cm = st.slider("📏 Height (cm)", 100.0, 250.0, 170.0, 0.1)

# --- BMI & Weight Analysis ---
bmi = calculate_bmi(weight, height_cm)
healthy_weight_lower, healthy_weight_upper = calculate_healthy_weight(height_cm)
ideal_weight = calculate_ideal_weight(height_cm, age)
weight_difference = round(weight - ideal_weight, 1)

st.subheader("📈 Health Insights")
st.write(f"**Your BMI:** {bmi}  🏥")
st.write(f"**Ideal Weight Range:** {healthy_weight_lower} kg - {healthy_weight_upper} kg  🎯")
st.write(f"**Your Ideal Weight:** {ideal_weight} kg  ✅")

if weight_difference > 0:
    st.markdown(f"<div class='warning-box'>⚠️ You are {weight_difference} kg over your ideal weight.</div>", unsafe_allow_html=True)
elif weight_difference < 0:
    st.markdown(f"<div class='success-box'>✅ You are {abs(weight_difference)} kg under your ideal weight.</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='success-box'>🎉 You are at your ideal weight!</div>", unsafe_allow_html=True)

# --- Diet Plan ---
st.subheader("🍽️ Personalized Diet Plan")
diet_choices = ["Vegetarian", "Vegan", "Keto", "Low Carb", "Gluten Free", "Dairy Free"]
dietary_preferences = st.selectbox("🥗 Choose your dietary preference:", diet_choices)

diet_plan = {
    "Vegetarian": ["Oatmeal with nuts 🥣", "Lentil soup with salad 🥗", "Paneer curry with rice 🍛"],
    "Vegan": ["Smoothie bowl 🍓", "Quinoa salad 🥙", "Tofu stir-fry 🍜"],
    "Keto": ["Eggs & avocado 🍳", "Grilled chicken with greens 🥩", "Salmon with butter sauce 🐟"],
    "Low Carb": ["Greek yogurt 🍦", "Chicken and veggies 🥩", "Steak with broccoli 🥦"],
    "Gluten Free": ["Fruit salad 🍉", "Rice bowl with fish 🍣", "Grilled meat & veggies 🍗"],
    "Dairy Free": ["Almond milk smoothie 🥤", "Quinoa with tofu 🍲", "Grilled chicken with sweet potatoes 🍠"]
}

st.markdown(f"**🍽️ Breakfast:** {diet_plan[dietary_preferences][0]}")
st.markdown(f"**🥗 Lunch:** {diet_plan[dietary_preferences][1]}")
st.markdown(f"**🍛 Dinner:** {diet_plan[dietary_preferences][2]}")

# --- Workout Plan ---
st.subheader("💪 Workout Plan")
workout_choices = ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"]
fitness_goals = st.selectbox("🏆 Choose your fitness goal:", workout_choices)

workout_plan = {
    "Lose Weight": ["🏃 30 min jogging", "💪 Full-body strength training", "🧘 Evening Yoga"],
    "Gain Muscle": ["🏋️‍♂️ Weightlifting (split routine)", "🥩 Protein-rich diet", "🛌 Active recovery"],
    "Endurance": ["🚴 Morning HIIT", "🏊 Cycling/swimming", "🤸 Evening stretching"],
    "Stay Fit": ["🚶 Daily 30 min walk", "🧍‍♂️ Bodyweight exercises", "🧘 Mindfulness training"],
    "Strength Training": ["🏋️ Powerlifting program", "🦵 Mobility drills", "⚡ Controlled cardio"]
}

st.markdown(f"**🌅 Morning:** {workout_plan[fitness_goals][0]}")
st.markdown(f"**☀️ Afternoon:** {workout_plan[fitness_goals][1]}")
st.markdown(f"**🌙 Evening:** {workout_plan[fitness_goals][2]}")

# --- Meditation Plan ---
st.subheader("🧘 Meditation & Pranayama Plan")
st.markdown("**🌅 Morning:** 5 min deep breathing + 5 min Alternate Nostril Breathing")
st.markdown("**☀️ Afternoon:** 5 min mindful meditation")
st.markdown("**🌙 Evening:** 10 min guided relaxation")

st.success("🎯 Your personalized health plan is ready! 🚀")
