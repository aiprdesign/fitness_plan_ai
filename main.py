import streamlit as st
from datetime import datetime
import pandas as pd

# Function to convert height from cm to feet and inches
def cm_to_feet_inches(height_cm):
    inches = height_cm / 2.54
    feet = int(inches // 12)
    inches = int(inches % 12)
    return feet, inches

# Mock AI Agents (replace with actual API integration)
class DietaryExpert:
    def generate_plan(self, profile):
        age = profile.get("age", 45)
        weight = profile.get("weight", 90)
        height = profile.get("height", 167.64)
        dietary_preferences = profile.get("dietary_preferences", "Vegetarian")
        fitness_goals = profile.get("fitness_goals", "Gain Muscle")

        # Dietary plans based on preferences
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

        return {
            "why_this_plan_works": f"Tailored for a {age}-year-old {profile.get('sex', 'Male')} weighing {weight}kg and {height}cm tall.",
            "meal_plan": meal_plan,
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
    dietary_preferences = profile.get("dietary_preferences", "Vegetarian")
    fitness_goals = profile.get("fitness_goals", "Gain Muscle")

    # Basic meal plan based on dietary preferences
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
    ideal_weight = 50 + 0.9 * (height - 152)  # Adjusted for age
    if age > 40:
        ideal_weight *= 0.95  # Slightly lower ideal weight for older adults
    return ideal_weight

# Function to create a custom BMI meter
def create_bmi_meter(bmi):
    st.markdown("### 📊 BMI Meter")
    if bmi < 18.5:
        st.error(f"BMI: {bmi:.1f} (Underweight)")
        st.progress(bmi / 40)
    elif 18.5 <= bmi < 25:
        st.success(f"BMI: {bmi:.1f} (Healthy)")
        st.progress(bmi / 40)
    elif 25 <= bmi < 30:
        st.warning(f"BMI: {bmi:.1f} (Overweight)")
        st.progress(bmi / 40)
    else:
        st.error(f"BMI: {bmi:.1f} (Obese)")
        st.progress(bmi / 40)

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
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f8ff;
        border: 1px solid #87CEEB;
    }
    .icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    .age-icon {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    .modern-container {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .modern-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .large-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .bmi-box {
        background-color: #00008B;
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 1rem;
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
            if validate_api_key(api_key, api_provider):
                st.success("API Key accepted!")
            else:
                st.error("Invalid API key. Please check and try again.")

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
    <div style='background-color: #00008B; padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
    Get personalized dietary and fitness plans tailored to your goals and preferences.
    Our AI-powered system considers your unique profile to create the perfect plan for you.
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
    age_icon = get_age_icon(age)
    st.markdown(f"<div class='large-number'>{age} years</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='age-icon'>{age_icon}</div>", unsafe_allow_html=True)
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

# BMI and Healthy Weight at the Top
bmi = calculate_bmi(weight, height_cm)
healthy_weight_lower, healthy_weight_upper = calculate_healthy_weight(height_cm)
ideal_weight = calculate_ideal_weight(height_cm, age)
weight_difference = weight - ideal_weight

# Custom BMI Meter
create_bmi_meter(bmi)

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
