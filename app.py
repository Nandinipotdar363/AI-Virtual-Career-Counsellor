import streamlit as st
from rasa.nlu.model import Interpreter
from career_mapper import load_career_data, suggest_careers_from_interest

# Load interpreter from trained model (update path as needed)
INTERPRETER_PATH = "./models/nlu"  # Or change to latest model folder
interpreter = Interpreter.load(INTERPRETER_PATH)

# Load career data
career_data = load_career_data("data/career_db.json")

# Title
st.title("🎓 Virtual Career Counsellor")
st.markdown("Ask me anything about your interests and I'll suggest a career!")

# User Input
user_input = st.text_input("🗨️ Type something like *I enjoy math* or *I want to become a robotics engineer*")

# Trigger processing
if st.button("Find Career"):
    if not user_input.strip():
        st.warning("Please enter your interests.")
    else:
        result = interpreter.parse(user_input)
        intent_name = result["intent"]["name"]
        st.markdown(f"**🔍 Detected intent:** `{intent_name}`")

        # Rule 1: Handle specific career intent
        if intent_name.startswith("interest_"):
            clean_intent = intent_name.replace("interest_", "").replace("_", " ").title()

            # Search all categories
            found = False
            for category, careers in career_data.items():
                for title, details in careers.items():
                    if title.lower() == clean_intent.lower():
                        st.success(f"🔹 **{title}**")
                        st.write(f"📝 {details.get('overview', 'No overview available')}")
                        st.write(f"💰 Salary in India: {details.get('salary_in_india', 'N/A')}")
                        st.write(f"🧠 Ideal For: {', '.join(details.get('ideal_for', []))}")
                        found = True
                        break
                if found:
                    break

            if not found:
                st.error("❌ Career not found in database.")

        # Rule 2: Handle keyword-based matching
        else:
            matched = suggest_careers_from_interest(user_input, career_data)
            if matched:
                st.markdown("📌 Based on your interests, here are some careers you may like:")
                for m in matched[:5]:
                    st.markdown(f"**🔹 {m['title']}** ({m['category']})")
                    st.write(f"🧠 Skills: {', '.join(m.get('skills_required', []))}")
                    st.write(f"💰 Salary: {m.get('salary_in_india', 'N/A')}")
                    st.write(f"📝 Overview: {m.get('overview', 'N/A')}")
            else:
                st.warning("I couldn't find a career match for your input. Try something like 'I love AI' or 'I enjoy biology'.")

