import os

import requests
from datetime import datetime
APP_ID = "3a5ac4de"
API_KEY = "097da4ce7f7b5a1718e1955554c0edcb"

GENDER = "male"
WEIGHT_KG = 50
HEIGHT_CM = 165
AGE = 21
exercise_text = "Running for 20 minutes"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers ={
    'Content-Type': 'application/json',
    'x-app-id': APP_ID,
    'x-app-key':API_KEY
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}


response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

sheety_endpoint = "https://api.sheety.co/bd1db5a230564cdd6948cd387f11b9d4/workoutTracking/workouts"

MY_USERNAME = os.environ["Auth_username"]
MY_PASSWORD = os.environ["Auth_password"]
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }


sheet_response = requests.post(
    sheety_endpoint,
    json=sheet_inputs,
    auth=(MY_USERNAME, MY_PASSWORD)
)
print(sheet_response.text)
