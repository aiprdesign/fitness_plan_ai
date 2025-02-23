import streamlit as st
from datetime import datetime
import pandas as pd
import requests  # For API calls

# Function to convert height from cm to feet and inches
def cm_to_feet_inches(height_cm):
    inches = height_cm / 2.54
    feet = int(inches // 12)
    inches = int(inches % 12)
    return feet, inches

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
    ideal_weight = 50 + 0.9 * (height - 152)  # Adjusted for age
    if age > 40:
        ideal_weight *= 0.95  # Slightly lower ideal weight for older adults
    return ideal_weight

# Function to generate a comprehensive plan
def generate_comprehensive_plan(profile):
    age = profile.get("age", 45)
    weight = profile.get("weight", 90)
    height = profile.get("height", 167.64)
    sex = profile.get("sex", "Male")
    activity_level = profile.get("activity_level", "Moderately Active")
    dietary_preferences = profile.get("dietary_preferences", "Vegetarian")
    fitness_goals = profile.get("fitness_goals", "Gain Muscle")

    # Dietary Plan
    if dietary_preferences == "Vegetarian":
        meal_plan = """
        **Breakfast**: Greek yogurt with honey, nuts, and fresh berries.
        **Lunch**: Quinoa salad with chickpeas, avocado, and feta cheese.
        **Dinner**: Vegetable stir-fry with tofu and brown rice.
        **Snacks**: Hummus with carrot sticks and a handful of almonds.
        """
    elif dietary_preferences == "Vegan":
        meal_plan = """
        **Breakfast**: Smoothie bowl with almond milk, bananas, and chia seeds.
        **Lunch**: Lentil curry with basmati rice and steamed broccoli.
        **Dinner**: Vegan Buddha bowl with quinoa, roasted veggies, and tahini dressing.
        **Snacks**: Apple slices with peanut butter and a handful of walnuts.
        """
    elif dietary_preferences == "Meat Free":
        meal_plan = """
        **Breakfast**: Scrambled eggs with spinach and whole-grain toast.
        **Lunch**: Caprese salad with mozzarella, tomatoes, and basil.
        **Dinner**: Eggplant parmesan with a side of garlic bread.
        **Snacks**: Cottage cheese with pineapple and a handful of cashews.
        """
    else:
        meal_plan = """
        **Breakfast**: Scrambled eggs with spinach and avocado.
        **Lunch**: Grilled chicken salad with quinoa and olive oil dressing.
        **Dinner**: Baked salmon with steamed broccoli and sweet potatoes.
        **Snacks**: Greek yogurt with berries and a handful of almonds.
        """

    # Workout Plan
    if fitness_goals == "Lose Weight":
        workout_plan = """
        **Warm-up**: 10 minutes of dynamic stretching.
        **Workout**:
        - Cardio: 30 minutes of running or cycling.
        - Strength Training: 3 sets of 12 reps (squats, lunges, push-ups).
        - Core: 3 sets of 1-minute planks.
        **Cool-down**: 5 minutes of static stretching.
        """
    elif fitness_goals == "Gain Muscle":
        workout_plan = """
        **Warm-up**: 10 minutes of dynamic stretching.
        **Workout**:
        - Strength Training: 4 sets of 8-10 reps (deadlifts, bench press, pull-ups).
        - Isolation Exercises: 3 sets of 12 reps (bicep curls, tricep extensions).
        - Core: 3 sets of 1-minute planks.
        **Cool-down**: 5 minutes of static stretching.
        """
    elif fitness_goals == "Endurance":
        workout_plan = """
        **Warm-up**: 10 minutes of dynamic stretching.
        **Workout**:
        - Cardio: 45 minutes of running, cycling, or swimming.
        - Circuit Training: 3 rounds of (jump squats, burpees, mountain climbers).
        - Core: 3 sets of 1-minute planks.
        **Cool-down**: 5 minutes of static stretching.
        """
    else:
        workout_plan = """
        **Warm-up**: 10 minutes of dynamic stretching.
        **Workout**:
        - Full-body workout: 3 sets of 12 reps (squats, push-ups, rows).
        - Core: 3 sets of 1-minute planks.
        **Cool-down**: 5 minutes of static stretching.
        """

    # Medication Plan (General Recommendations)
    medication_plan = """
    **General Recommendations**:
    - Consult a healthcare provider before starting any medication.
    - Stay hydrated and maintain a balanced diet.
    - Consider supplements like Vitamin D, Omega-3, and Multivitamins if needed.
    """

    return {
        "why_this_plan_works": f"Tailored for a {age}-year-old {sex} weighing {weight}kg and {height}cm tall.",
        "meal_plan": meal_plan,
        "workout_plan": workout_plan,
        "medication_plan": medication_plan,
        "important_considerations": """
        - Hydration: Drink plenty of water throughout the day.
        - Electrolytes: Monitor sodium, potassium, and magnesium levels.
        - Fiber: Ensure adequate intake through vegetables and fruits.
        - Listen to your body: Adjust portion sizes as needed.
        """
    }

# Initialize session state
if 'dietary_plan' not in st.session_state:
    st.session_state.dietary_plan = {}
if 'fitness_plan' not in st.session_state:
    st.session_state.fitness_plan = {}
if 'medication_plan' not in st.session_state:
    st.session_state.medication_plan = {}
if 'progress_data' not in st.session_state:
    st.session_state.progress_data = []
if 'qa_pairs' not in st.session_state:
    st.session_state.qa_pairs = []
if 'plans_generated' not in st.session_state:
    st.session_state.plans_generated = False

# Custom CSS for dark theme and compact layout
st.markdown("""
    <style>
    .main {
        padding: 0.5rem;
        background-color: #1e1e1e;
        color: #ffffff;
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
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stNumberInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
        padding: 10px;
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .info-box {
        padding: 0.5rem;
        border-radius: 0.5rem;
        background-color: #2d2d2d;
        border: 1px solid #87CEEB;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .warning-box {
        padding: 0.5rem;
        border-radius: 0.5rem;
        background-color: #4d2d2d;
        border: 1px solid #fbd38d;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .success-box {
        padding: 0.5rem;
        border-radius: 0.5rem;
        background-color: #2d4d2d;
        border: 1px solid #9ae6b4;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .modern-container {
        background-color: #2d2d2d;
        padding: 0.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .modern-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #87CEEB;
        margin-bottom: 0.5rem;
    }
    .large-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #87CEEB;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #87CEEB;
    }
    .stMarkdown p {
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API Key and Navigation
with st.sidebar:
    st.title("⚙️ Settings")
    use_ai = st.checkbox("Enable AI Features (Requires API Key)", value=False)
    if use_ai:
        api_provider = st.selectbox(
            "Choose API Provider",
            options=["Gemini", "DeepSeek"],
            help="Select the AI API provider for generating plans."
        )
        api_key = st.text_input(
            f"Enter {api_provider} API Key",
            type="password",
            help=f"Required for {api_provider} functionality."
        )
        if not api_key:
            st.warning(f"Please enter your {api_provider} API key to use AI features.")
            if api_provider == "Gemini":
                st.markdown("[Get your Gemini API key here](https://aistudio.google.com/apikey)")
            else:
                st.markdown("[Get your DeepSeek API key here](https://platform.deepseek.com)")
        else:
            st.success("API Key accepted!")

    st.title("📊 Progress Tracker")
    weight_today = st.number_input("Today's Weight (kg)", min_value=20.0, max_value=300.0, step=0.1, value=90.0)
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
    <div style='background-color: #2d2d2d; padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 1rem; color: #ffffff;'>
    Get personalized dietary, fitness, and medication plans tailored to your goals and preferences.
    </div>
""", unsafe_allow_html=True)

# User Profile Input
st.header("👤 Your Profile")

# Age, Weight, and Height Sliders
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
    st.markdown("<div class='modern-header'>🎂 Age</div>", unsafe_allow_html=True)
    age = st.slider("", min_value=10, max_value=100, value=45, step=1, help="Adjust your age using the slider.")
    st.markdown(f"<div class='large-number'>{age} years</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
    st.markdown("<div class='modern-header'>⚖️ Weight (kg)</div>", unsafe_allow_html=True)
    weight = st.slider("", min_value=20.0, max_value=300.0, value=90.0, step=0.1, help="Adjust your weight using the slider.")
    st.markdown(f"<div class='large-number'>{weight} kg</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
    st.markdown("<div class='modern-header'>📏 Height</div>", unsafe_allow_html=True)
    height_cm = st.slider("", min_value=100.0, max_value=250.0, value=170.0, step=0.1, help="Adjust your height using the slider.")
    feet, inches = cm_to_feet_inches(height_cm)
    st.markdown(f"<div class='large-number'>{height_cm:.1f} cm ({feet}'{inches}\")</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Calculate BMI and Health Metrics
bmi = calculate_bmi(weight, height_cm)
healthy_weight_lower, healthy_weight_upper = calculate_healthy_weight(height_cm)
ideal_weight = calculate_ideal_weight(height_cm, age)
overweight_status = weight - ideal_weight

# Health Metrics Section
st.markdown("---")
st.markdown("### 📊 Health Metrics")

# Display Ideal Weight Range
st.markdown(f"""
    <div class='info-box'>
        <strong>🎯 Ideal Weight Range:</strong> {healthy_weight_lower:.1f} kg - {healthy_weight_upper:.1f} kg
    </div>
""", unsafe_allow_html=True)

# Display Overweight Status
if overweight_status > 0:
    st.markdown(f"""
        <div class='warning-box'>
            <strong>⚠️ You are {overweight_status:.1f} kg over your ideal weight.</strong>
        </div>
    """, unsafe_allow_html=True)
elif overweight_status < 0:
    st.markdown(f"""
        <div class='success-box'>
            <strong>✅ You are {abs(overweight_status):.1f} kg under your ideal weight.</strong>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class='success-box'>
            <strong>🎉 You are at your ideal weight!</strong>
        </div>
    """, unsafe_allow_html=True)

# Display BMI Status
st.markdown("### 📈 BMI Status")
if bmi < 18.5:
    st.markdown(f"""
        <div class='warning-box'>
            <strong>😟 Underweight:</strong> Your BMI is {bmi:.1f}. Consider gaining weight for better health.
        </div>
    """, unsafe_allow_html=True)
elif 18.5 <= bmi < 25:
    st.markdown(f"""
        <div class='success-box'>
            <strong>😊 Healthy Weight:</strong> Your BMI is {bmi:.1f}. Keep up the good work!
        </div>
    """, unsafe_allow_html=True)
elif 25 <= bmi < 30:
    st.markdown(f"""
        <div class='warning-box'>
            <strong>😕 Overweight:</strong> Your BMI is {bmi:.1f}. Consider losing weight for better health.
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class='error-box'>
            <strong>😨 Obese:</strong> Your BMI is {bmi:.1f}. It's important to take steps to improve your health.
        </div>
    """, unsafe_allow_html=True)

# Gender Radio Button
st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
st.markdown("<div class='modern-header'>👫 Gender</div>", unsafe_allow_html=True)
sex = st.radio("", options=["Male", "Female", "Other"], index=0, help="Select your gender.")
st.markdown("</div>", unsafe_allow_html=True)

# Additional Inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
    st.markdown("<div class='modern-header'>🏃‍♂️ Activity Level</div>", unsafe_allow_html=True)
    activity_level = st.selectbox(
        "",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
        index=2,  # Default: Moderately Active
        help="Select your typical activity level."
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
    st.markdown("<div class='modern-header'>🥗 Dietary Preferences</div>", unsafe_allow_html=True)
    dietary_preferences = st.selectbox(
        "",
        options=["Vegetarian", "Vegan", "Meat Free", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
        index=0,  # Default: Vegetarian
        help="Select your dietary preference."
    )
    st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='modern-container'>", unsafe_allow_html=True)
    st.markdown("<div class='modern-header'>🎯 Fitness Goals</div>", unsafe_allow_html=True)
    fitness_goals = st.selectbox(
        "",
        options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
        index=1,  # Default: Gain Muscle
        help="What do you want to achieve?"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Generate Plans
if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
    user_profile = {
        "age": age,
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
                # Mock AI-generated plans (replace with actual API calls)
                st.session_state.dietary_plan = {
                    "why_this_plan_works": f"Tailored for a {age}-year-old {sex} weighing {weight}kg and {height_cm}cm tall.",
                    "meal_plan": "Sample meal plan based on your preferences.",
                    "important_considerations": "Stay hydrated and listen to your body."
                }
                st.session_state.fitness_plan = {
                    "goals": "Achieve your fitness goals with this plan.",
                    "routine": "Sample workout routine based on your goals.",
                    "tips": "Stay consistent and track your progress."
                }
                st.session_state.medication_plan = {
                    "recommendations": "Consult a healthcare provider before starting any medication."
                }
                st.session_state.plans_generated = True

                st.success("AI-generated plans created successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        with st.spinner("Creating your basic health and fitness routine..."):
            try:
                # Generate comprehensive plans
                comprehensive_plan = generate_comprehensive_plan(user_profile)
                st.session_state.dietary_plan = {
                    "why_this_plan_works": comprehensive_plan["why_this_plan_works"],
                    "meal_plan": comprehensive_plan["meal_plan"],
                    "important_considerations": comprehensive_plan["important_considerations"]
                }
                st.session_state.fitness_plan = {
                    "goals": "Achieve your fitness goals with this plan.",
                    "routine": comprehensive_plan["workout_plan"],
                    "tips": "Stay consistent and track your progress."
                }
                st.session_state.medication_plan = {
                    "recommendations": comprehensive_plan["medication_plan"]
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
        st.write(st.session_state.dietary_plan["important_considerations"])

    with st.expander("💪 Fitness Plan", expanded=True):
        st.markdown("### 🎯 Goals")
        st.success(st.session_state.fitness_plan["goals"])
        st.markdown("### 🏋️‍♂️ Exercise Routine")
        st.write(st.session_state.fitness_plan["routine"])
        st.markdown("### 💡 Pro Tips")
        st.write(st.session_state.fitness_plan["tips"])

    with st.expander("💊 Medication Plan", expanded=True):
        st.markdown("### 🎯 Recommendations")
        st.info(st.session_state.medication_plan["recommendations"])

# Q&A Section (Limited to Fitness Plan)
if st.session_state.plans_generated:
    st.header("❓ Questions about your Fitness Plan?")
    
    # Check if AI features are enabled and API key is provided
    if use_ai:
        if not api_key:
            st.warning("Please enter your API key in the sidebar to ask questions.")
        else:
            question_input = st.text_input("Ask a question about your fitness plan")
            if st.button("Get Answer"):
                if question_input:
                    with st.spinner("Finding the best answer for you..."):
                        try:
                            # Mock AI response (replace with actual API call)
                            answer = "Sample answer based on your question."
                            st.session_state.qa_pairs.append((question_input, answer))
                            st.success("Answer generated!")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                else:
                    st.warning("Please enter a question.")
            
            # Add a note about the API key
            st.markdown("""
                <div class='info-box'>
                    <strong>Note:</strong> To ask questions, ensure you have entered a valid API key in the sidebar.
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("AI features are disabled. Enable AI features in the sidebar to ask questions.")

    if st.session_state.qa_pairs:
        st.header("💬 Q&A History")
        for q, a in st.session_state.qa_pairs:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
        
        if st.button("Clear Q&A History"):
            st.session_state.qa_pairs = []
            st.success("Q&A history cleared!")
