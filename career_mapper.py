import json
import csv

# Adjust these paths as needed
csv_file_path = "career_data.csv"
json_file_path = "career_data.json"

career_dict = {}

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        career_name = row['career'].strip()
        career_dict[career_name] = {
            "overview": row['overview'].strip(),
            "core_skills": [skill.strip() for skill in row['skills'].split(',')],
            "ideal_for": [trait.strip() for trait in row['ideal_for'].split(',')],
            "salary_in_india": row['salary_in_india'].strip()
        }

# Write to JSON file
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(career_dict, jsonfile, indent=4, ensure_ascii=False)

print(f"✅ Career data written to {json_file_path}")
