import boto3
import json

def botInf(string):
    with open(string) as file:
        return json.loads(file.read())

try:
    cfg = botInf("cfg.json")
    client = boto3.client('lexv2-runtime')
    response = client.recognize_text(
    botId=cfg["botId"],
    botAliasId = cfg["botAliasId"],
    localeId= cfg["localeId"],
    sessionId = "test",
    text= input("Ask me something:")
    )
    #print(response)
    print("Lex:",response["messages"][0]["content"]) 
            
except:
    print("Error blablabla ")
