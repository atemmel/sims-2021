#!/usr/local/bin/python3.7

import subprocess
from function import create_intent
from function import list_intents
from function import detect_intent_texts

subprocess.call(['sh', './export.sh'])

project_ID = "sims-326911"
intent_name = "test_intent1"
training_phrase = ["what weighs 300kg"]
message = ["your mum"]
session_ID = ["123456789"]
#print("tip something")
texts = ["what weighs 3000kg"]
#texts = input()

#intent1 = create_intent(project_ID,intent_name ,training_phrase ,message)

#list_intents = list_intents(project_ID)

detect_intent_texts(project_ID, session_ID, texts, language_code= "en-US")

