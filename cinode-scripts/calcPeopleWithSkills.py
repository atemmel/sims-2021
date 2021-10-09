#
# Creates a json file that looks like:
#
#   [
#       {
#           "Skill": "Python"
#           "Amount": 1
#       },
#       {
#           "Skill": "Professional egg eater"
#           "Amount": 583
#       },
#       ...
#       ...
#   ]
#


import json

skill_amount = []


def find_skill(skill):
    global skill_amount
    for i, obj in enumerate(skill_amount):
        if obj["Skill"] == skill:
            return i
    return -1


def create_skill_amount():
    global skill_amount
    with open("../datasets/cinode-data/BetterCompanyUserSkills.json", "r", encoding="UTF-8") as file:
        company_users = json.loads(file.read())
        for company_user_skills in company_users:
            for user_skill in company_user_skills:
                if "keyword" in user_skill:
                    if user_skill["keyword"]["masterSynonym"]:
                        skill = user_skill["keyword"]["masterSynonym"]
                        index = find_skill(skill)
                        if index != -1:
                            skill_amount[index]["Amount"] += 1
                        else:
                            skill_amount.append({
                                "Skill": skill,
                                "Amount": 1
                            })

    with open("../datasets/cinode-data/CompanyUserSkillsAmount.json", "w", encoding="utf8") as outfile:
        json.dump(skill_amount, outfile, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


create_skill_amount()