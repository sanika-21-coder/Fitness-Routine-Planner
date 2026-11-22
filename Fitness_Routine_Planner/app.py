import streamlit as st
import pandas as pd
import os
from openai import OpenAI

st.set_page_config(page_title="Fitness Routine Planner", page_icon="💪", layout="wide")

st.title("💪 Fitness Routine Planner")
st.caption("Create a beginner-friendly home workout plan based on your goal, fitness level, time, and equipment.")

with st.sidebar:
    st.header("Your preferences")
    goal = st.selectbox("Fitness goal", ["General fitness", "Weight loss", "Muscle gain", "Flexibility"])
    level = st.selectbox("Fitness level", ["Beginner", "Intermediate", "Advanced"])
    minutes = st.selectbox("Time available per day", [15, 20, 30, 45, 60], index=2)
    equipment = st.multiselect(
        "Equipment available",
        ["None", "Yoga mat", "Dumbbells", "Resistance bands", "Jump rope"],
        default=["None"]
    )
    generate = st.button("Generate my weekly plan", type="primary", use_container_width=True)

def make_prompt(goal, level, minutes, equipment):
    return f"""
You are a careful, supportive fitness coach. Generate a practical 7-day home workout plan.

User preferences:
- Goal: {goal}
- Fitness level: {level}
- Available time per day: {minutes} minutes
- Equipment: {', '.join(equipment) if equipment else 'None'}

Requirements:
- Include warm-up and cool-down in each workout day's time estimate.
- Keep each session within {minutes} minutes.
- Include recovery/rest days.
- Do not prescribe unavailable equipment.
- Use exercises appropriate to the user's level.
- Include sets, reps or duration, rest between sets, and brief form cues.
- Avoid extreme volume and make the plan safe and adaptable.
- For each day, return a row in a Markdown table with columns:
  Day, Focus, Exercises (sets × reps/duration), Rest, Total time.
- Include a short safety note and a motivational message.
"""

def fallback_plan(goal, level, minutes, equipment):
    rows = [
        ["Monday", "Full body", "Chair squats 3×10; wall push-ups 3×8; glute bridges 3×12; marching 3×45 sec", "30–45 sec", f"{minutes} min"],
        ["Tuesday", "Cardio", "Brisk walk 15–20 min; step-touch 3×1 min; standing knee raises 3×12", "30 sec", f"{minutes} min"],
        ["Wednesday", "Recovery", "Gentle mobility and stretching 15–20 min", "As needed", "15–20 min"],
        ["Thursday", "Strength", "Reverse lunges 3×8/side; incline push-ups 3×8; bird-dog 3×10/side; plank 3×20 sec", "45 sec", f"{minutes} min"],
        ["Friday", "Full body", "Squats 3×10; hip hinges 3×12; wall push-ups 3×10; dead bug 3×10/side", "30–45 sec", f"{minutes} min"],
        ["Saturday", "Cardio & mobility", "Low-impact cardio 15 min; stretching 10 min", "As needed", f"{minutes} min"],
        ["Sunday", "Rest", "Rest or relaxed walk", "—", "Recovery"],
    ]
    return pd.DataFrame(rows, columns=["Day", "Focus", "Exercises (sets × reps/duration)", "Rest", "Total time"])

if generate:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "Return a concise, safe workout plan. Use a Markdown table and include safety guidance."},
                    {"role": "user", "content": make_prompt(goal, level, minutes, equipment)}
                ],
                temperature=0.7
            )
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.warning(f"AI generation failed ({e}). Showing a sample plan instead.")
            st.dataframe(fallback_plan(goal, level, minutes, equipment), use_container_width=True, hide_index=True)
    else:
        st.info("No API key detected. Showing a sample plan. Add an OpenAI API key to enable AI-generated plans.")
        st.dataframe(fallback_plan(goal, level, minutes, equipment), use_container_width=True, hide_index=True)
        st.markdown("**Warm-up:** 3–5 minutes of easy marching and joint circles. **Cool-down:** 3–5 minutes of gentle stretching.")
        st.markdown("**Safety:** Stop if you experience pain, dizziness, or unusual shortness of breath. Adjust exercises to your ability.")
        st.success("You can still use the app without an API key—the sample plan is available.")

st.markdown("---")
st.caption("This planner provides general fitness guidance, not medical advice. If you have an injury, health condition, or are unsure whether exercise is appropriate, consult a qualified healthcare professional.")
