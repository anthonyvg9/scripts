import requests

opsgenie_api_key = "564ac153-b565-48ae-955d-14292fbb077c"
opsgenie_schedule_id = "601ccdc8-7615-4edc-bebf-bfe731da9177"

headers = {
    "Authorization": f"GenieKey {opsgenie_api_key}",
    "Content-Type": "application/json",
}

data = {
    "user": {
        "type": "none"
    },
    "startDate": "2023-11-06T12:00:00-05:00",
    "endDate": "2023-11-06T21:00:00-05:00",
    "rotations": [
        {
            "name": "US West"
        }
    ]
}

url = f"https://api.opsgenie.com/v2/schedules/{opsgenie_schedule_id}/overrides"
response = requests.post(url, headers=headers, json=data)

if response.status_code == 202:
    print("Override successful!")
else:
    print(f"Error occurred. Status code: {response.status_code}")
