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
    """Calculate BMI using kg and cm; returns one decimal point value"""
    return round(weight / ((height / 100) ** 2), 1)

def calculate_healthy_weight(height):
    """Returns the lower and upper bounds of a healthy weight range"""
    return round(18.5 * ((height / 100) ** 2), 1), round(24.9 * ((height / 100) ** 2), 1)

def calculate_caloric_needs(age, weight, height, activity_level, goal):
    """Calculates daily calorie needs based on activity level and fitness goal"""
    bmr = (10 * weight) + (6.25 * height) - (5 * age)
    multipliers = {
        "Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55,
        "Very Active": 1.725, "Extremely Active": 1.9
    }
    calories = bmr * multipliers[activity_level]
    if goal == "Lose Weight":
        calories -= 500
    elif goal == "Gain Muscle":
        calories += 500
    return round(calories)

# --- Detailed Plans Dictionaries ---
detailed_diet_plans = {
    "Vegetarian": {
        "Breakfast": "A hearty bowl of oatmeal topped with nuts, berries, and a drizzle of honey. This meal is rich in fiber and antioxidants.",
        "Lunch": "A vibrant chickpea salad with mixed greens, tomatoes, cucumbers, and a lemon-tahini dressing. Provides protein and healthy fats.",
        "Dinner": "A warm lentil soup served with brown rice and steamed vegetables. A balanced meal for sustained energy."
    },
    "Vegan": {
        "Breakfast": "A smoothie bowl with blended bananas, spinach, almond milk, and topped with chia seeds and fresh fruits.",
        "Lunch": "A quinoa salad mixed with black beans, corn, avocado, and a zesty lime dressing. Packed with plant protein and fiber.",
        "Dinner": "A tofu stir-fry with broccoli, bell peppers, and snap peas served over brown rice. Full of flavor and nutrients."
    },
    "Keto": {
        "Breakfast": "Scrambled eggs with avocado slices and a side of spinach sautéed in olive oil.",
        "Lunch": "Grilled chicken salad with mixed greens, cheese, and a creamy avocado dressing, keeping carbs low.",
        "Dinner": "Salmon fillet with asparagus cooked in butter, ensuring high protein and omega-3 intake."
    },
    "Low Carb": {
        "Breakfast": "Greek yogurt mixed with almonds and a few berries for natural sweetness.",
        "Lunch": "Grilled chicken served with a side of steamed broccoli and a green salad with olive oil dressing.",
        "Dinner": "A lean steak with sautéed spinach and a small portion of quinoa to keep carbs in check."
    },
    "Gluten Free": {
        "Breakfast": "A bowl of fresh fruits with a handful of nuts and seeds.",
        "Lunch": "Grilled fish with rice and a side of mixed vegetables, ensuring gluten-free grains.",
        "Dinner": "Chicken roasted with sweet potatoes and green beans for a balanced gluten-free meal."
    },
    "Dairy Free": {
        "Breakfast": "An almond milk smoothie with banana, spinach, and flaxseeds.",
        "Lunch": "A quinoa and tofu bowl with mixed vegetables, drizzled with a tahini dressing.",
        "Dinner": "Grilled chicken with roasted vegetables and a side of sweet potatoes, completely dairy free."
    }
}

detailed_workout_plans = {
    "Lose Weight": {
        "Morning": "30 minutes of brisk walking or jogging with a 5-minute warm-up and cool-down.",
        "Afternoon": "Circuit training: 3 sets of 15 squats, 10 push-ups, 15 lunges, and 20 jumping jacks.",
        "Evening": "A 15-minute yoga flow focusing on stretching and core stabilization."
    },
    "Gain Muscle": {
        "Morning": "Strength training: 4 sets of 8-10 reps of bench press, squats, and deadlifts (adjust weights accordingly).",
        "Afternoon": "Accessory work: 3 sets of 10 reps of bicep curls, tricep dips, and shoulder presses.",
        "Evening": "Light cardio (15 minutes of cycling or brisk walking) and stretching to aid recovery."
    },
    "Maintain Weight": {
        "Morning": "A 45-minute brisk walk or light jog to keep the metabolism active.",
        "Afternoon": "Bodyweight exercises: 3 sets of 15 squats, 10 push-ups, and 20 sit-ups.",
        "Evening": "Relaxation exercises and stretching for 15 minutes to wind down."
    }
}

detailed_yoga_plans = {
    "Morning": "5 minutes of deep breathing exercises followed by 5 minutes of alternate nostril breathing to energize your day.",
    "Afternoon": "5 minutes of mindful meditation focusing on body relaxation and stress reduction.",
    "Evening": "10 minutes of guided yoga or gentle stretching to promote relaxation and better sleep quality."
}

# --- Personalized Advice Function ---
def personalized_advice(bmi, healthy_range):
    low, high = healthy_range
    advice = ""
    if bmi < 18.5:
        advice = ("It looks like you are underweight. Consider incorporating nutrient-dense foods and healthy snacks into your diet. "
                  "Ensure you're getting enough calories and proteins. Remember, gradual weight gain through balanced meals and strength exercises "
                  "is key. Always listen to your body and consider seeking advice from a nutritionist.")
    elif 18.5 <= bmi < 25:
        advice = ("Great job maintaining a healthy weight! Continue with your balanced diet and regular exercise. "
                  "Keep up with your active lifestyle and make sure to include variety in your workouts to challenge your body in new ways.")
    elif 25 <= bmi < 30:
        advice = ("Your BMI suggests that you're slightly overweight. A combination of cardiovascular exercises and strength training can help you "
                  "achieve a healthier weight. Focus on whole, unprocessed foods and consider small, sustainable changes to your diet. "
                  "Remember, every small step counts toward a healthier you.")
    else:
        advice = ("Your BMI indicates that you are in the obese range, which can increase the risk of several health issues. "
                  "It's important to approach weight loss gradually by incorporating regular physical activity and a balanced, low-calorie diet. "
                  "Consider speaking with a healthcare professional or a registered dietitian for personalized guidance. "
                  "You're taking the first step by being proactive about your health, and that's commendable.")
    return advice

# --- Modern UI & Styling ---
st.markdown("""
    <style>
    .bmi-gauge { text-align: center; font-size: 22px; font-weight: bold; padding: 10px; color: white; border-radius: 10px; }
    .bmi-good { background-color: #4CAF50; }  
    .bmi-warning { background-color: #FFA500; }  
    .bmi-danger { background-color: #FF5733; }  
    .bmi-low { background-color: #1E90FF; }  
    .meter { width: 100%; height: 25px; border-radius: 8px; }
    .footer { text-align: center; font-size: 14px; margin-top: 30px; color: gray; }
    .stSlider > div[data-baseweb="slider"] > div { height: 6px !important; } /* Thicker slider bar */
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("🏋️ AI Health & Fitness Planner")

# --- User Profile Inputs ---
st.header("👤 Your Profile")
st.markdown("Enter your details to get a **personalized health plan** tailored for you.")

col1, col2, col3 = st.columns(3)
with col1:
    age = st.slider("Age", 10, 100, 30, 1)
with col2:
    weight = st.slider("Weight (kg)", 30.0, 200.0, 70.0, 0.1)
with col3:
    height_cm = st.slider("Height (cm / ft)", 100.0, 250.0, 170.0, 0.1)
    feet, inches = cm_to_feet_inches(height_cm)
    st.markdown(f"**{height_cm} cm / {feet}'{inches}\"**")

# --- BMI Gauge ---
bmi = calculate_bmi(weight, height_cm)
bmi_category = "🔵 Underweight" if bmi < 18.5 else "🟢 Healthy" if bmi < 25 else "🟠 Overweight" if bmi < 30 else "🔴 Obese"
bmi_class = "bmi-low" if bmi < 18.5 else "bmi-good" if bmi < 25 else "bmi-warning" if bmi < 30 else "bmi-danger"
st.markdown(f"""
    <div class="bmi-gauge {bmi_class}">
        <meter min="10" max="40" value="{bmi}" class="meter"></meter><br>
        <span>Your BMI: {bmi} ({bmi_category})</span>
    </div>
""", unsafe_allow_html=True)

# --- Disease Risk Based on BMI ---
st.header("⚠️ Health Risks Based on BMI")
if bmi < 18.5:
    st.warning("**Underweight Risks:** Malnutrition, osteoporosis, and weakened immunity.")
elif 18.5 <= bmi < 25:
    st.success("**Healthy Weight:** Low risk of chronic diseases. Continue your balanced lifestyle!")
elif 25 <= bmi < 30:
    st.warning("**Overweight Risks:** Elevated risk of heart disease, high blood pressure, and type 2 diabetes.")
else:
    st.error("**Obesity Risks:** High risk of heart disease, stroke, type 2 diabetes, sleep apnea, and joint issues.")

# --- Lifestyle & Goals ---
st.header("🏃 Lifestyle & Goals")
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
fitness_goal = st.selectbox("Fitness Goal", ["Lose Weight", "Maintain Weight", "Gain Muscle"])
daily_calories = calculate_caloric_needs(age, weight, height_cm, activity_level, fitness_goal)
st.markdown(f"**Estimated Daily Calories:** {daily_calories} kcal")

# --- Personalized Diet Plan ---
st.header("🍽️ Your Personalized Diet Plan")
diet_choice = st.selectbox("Select Your Diet Preference", list(detailed_diet_plans.keys()))
plan = detailed_diet_plans[diet_choice]
st.markdown(f"**Breakfast:** {plan['Breakfast']}")
st.markdown(f"**Lunch:** {plan['Lunch']}")
st.markdown(f"**Dinner:** {plan['Dinner']}")

# --- Detailed Workout Plan ---
st.header("💪 Detailed Workout Plan")
workout_choice = fitness_goal  # using the selected fitness goal
workout = detailed_workout_plans[workout_choice]
st.markdown(f"**Morning Workout:** {workout['Morning']}")
st.markdown(f"**Afternoon Workout:** {workout['Afternoon']}")
st.markdown(f"**Evening Workout:** {workout['Evening']}")

# --- Yoga & Pranayama Plan ---
st.header("🧘 Yoga & Pranayama Plan")
for time_of_day, plan in detailed_yoga_plans.items():
    st.markdown(f"**{time_of_day}:** {plan}")

# --- Personalized Advice ---
st.header("💡 Personalized Advice")
advice = personalized_advice(bmi, calculate_healthy_weight(height_cm))
st.info(advice)

# --- Weight Progress Tracking ---
st.header("📊 Weight Tracking")
weight_today = st.number_input("Log Today's Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
if st.button("Log Weight"):
    st.session_state.progress_data.append({"date": datetime.today().strftime('%Y-%m-%d'), "weight": weight_today})
    st.success("Weight logged successfully!")
if st.session_state.progress_data:
    df = pd.DataFrame(st.session_state.progress_data)
    st.line_chart(df.set_index("date"))

# --- Footer Disclaimer ---
st.markdown("""
    <div class="footer">
        ⚠️ This tool provides general health insights and personalized advice but <strong>is not a substitute for professional medical advice</strong>. 
        Always consult your doctor or a healthcare provider before making major health decisions.
    </div>
""", unsafe_allow_html=True)

st.success("Your comprehensive health plan is ready! 🎯")
