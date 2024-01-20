import requests
import json
import datetime
import pandas as pd

### Methods ###

def date_yyyymmdd_to_ddmmyyyy(date_yyyymmdd):
    date_obj = datetime.datetime.strptime(date_yyyymmdd, "%Y-%m-%d")
    return date_obj.strftime('%d-%m-%Y')

def parliament_url(date_ddmmyyyy):
    return f"https://sprs.parl.gov.sg/search/getHansardReport/?sittingDate={date_ddmmyyyy}"

def get_json(url):
    print(f"Trying: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Success!")
    else:
        print(f"Reponse Code: {response.status_code}")

    return response

def save_json(response_json, filepath):
    with open(filepath, 'w') as file:
        json.dump(response_json, file)
        print(f"JSON saved to: {filepath}\n")

    return 0

