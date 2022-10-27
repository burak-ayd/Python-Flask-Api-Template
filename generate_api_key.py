import uuid
import json

def api_key():
    with open('api_key.json') as f:
        key = json.load(f)
    
    if key["api_key"] == "":
        key["api_key"] = str(uuid.uuid4())
        with open('api_key.json', 'w') as f:
            json.dump(key, f)
    else:
        return key["api_key"]
