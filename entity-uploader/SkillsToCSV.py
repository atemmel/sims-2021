import csv
import json

skills = []


def get_master_synonyms(company_users):
    global skills
    for company_user_skills in company_users:
        company_user_skills = json.loads(company_user_skills)
        for user_skill in company_user_skills:
            if "keyword" in user_skill:
                if user_skill["keyword"]["masterSynonym"]:
                    skill = "Skills, " + user_skill["keyword"]["masterSynonym"]

                    # Length is not allowed to be greater than 64 in watson entities
                    if len(skill) < 64:
                        if skill not in skills:
                            skills.append(skill)


def skills_to_csv(input_name, output_name):
    with open(input_name, "r", encoding="UTF-8") as file:
        company_users_json = json.loads(file.read())

    with open(output_name, "w", encoding="UTF-8", newline='') as file:
        writer = csv.writer(file, delimiter='|', quoting=csv.QUOTE_NONE)
        get_master_synonyms(company_users_json)
        for skill in skills:
            writer.writerow([skill])


skills_to_csv("../datasets/cinode-data/CompanyUserSkills.json", "skills.csv")
