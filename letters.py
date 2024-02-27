import json
  
# Opening JSON file
def send_json():
    f = open('letters.json')
  
# returns JSON object as 
# a dictionary
    data = json.load(f)
    return data
