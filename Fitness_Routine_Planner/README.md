# Fitness Routine Planner

A Streamlit app that generates a weekly home workout plan from:
- Fitness goal
- Fitness level
- Minutes available per day
- Equipment available

## Run locally

1. Install Python 3.9+.
2. Open a terminal in this folder.
3. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set your OpenAI API key to enable AI-generated plans.

   Windows PowerShell:
   ```powershell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```

   macOS/Linux:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

5. Run:

   ```bash
   streamlit run app.py
   ```

Without an API key, the app displays a sample weekly workout plan.

## Safety
General fitness guidance only. Stop if you feel pain, dizziness, or unusual shortness of breath. Consult a qualified professional for medical concerns.
