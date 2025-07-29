import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# Load career data from JSON file
def load_career_data(filepath: str) -> Dict[str, Any]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading career data: {e}")
        return {}

# Suggest careers based on user input
def suggest_careers_from_interest(user_input: str, career_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    user_input_lower = user_input.lower()
    matches = []

    for title, details in career_data.items():
        ideal_traits = [x.lower() for x in details.get("ideal_for", [])]
        overview = details.get("overview", "").lower()
        skills = [x.lower() for x in details.get("core_skills", [])]
        title_lower = title.lower()

        match_score = 0

        if title_lower in user_input_lower:
            match_score += 2

        for trait in ideal_traits:
            if trait in user_input_lower:
                match_score += 2

        for skill in skills:
            if skill in user_input_lower:
                match_score += 1

        if any(word in overview for word in user_input_lower.split()):
            match_score += 1

        if match_score > 0:
            matches.append({
                "title": title,
                "overview": details.get("overview", ""),
                "skills_required": details.get("core_skills", []),
                "salary_in_india": details.get("salary_in_india", "Not specified"),
                "match_score": match_score
            })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches


# Custom Action to suggest careers
class ActionSuggestCareers(Action):

    def name(self) -> Text:
        return "action_suggest_careers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text", "")
        career_data = load_career_data("career_data.json")
        suggestions = suggest_careers_from_interest(user_input, career_data)

        if suggestions:
            top_suggestions = suggestions[:3]  # Show top 3 matches
            response = "Based on your interest, here are some career suggestions:\n"
            for suggestion in top_suggestions:
                response += f"\n🔹 **{suggestion['title']}**\n"
                response += f"   - Overview: {suggestion['overview']}\n"
                response += f"   - Core Skills: {', '.join(suggestion['skills_required'])}\n"
                response += f"   - Salary (India): {suggestion['salary_in_india']}\n"
        else:
            response = "❗I couldn’t find any careers matching your input. Could you tell me more about your interests?"

        dispatcher.utter_message(text=response)
        return []
