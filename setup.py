import json
import os
infoDictionary = {
    "High Score": 0, "Player Name": "Anonymous", "Window Name": "Snake", "X Border": 500, "Y Border": 500
}

infoJson = json.dumps(infoDictionary, sort_keys=True)

with open("config.json", "w") as configFile:
    configFile.write(infoJson)
