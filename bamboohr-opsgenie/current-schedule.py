import requests
import json

opsgenie_api_key = "564ac153-b565-48ae-955d-14292fbb077c"
opsgenie_schedule_id = "601ccdc8-7615-4edc-bebf-bfe731da9177"
username = "anthony@cast.ai"

headers = {
    'Authorization': f"GenieKey {opsgenie_api_key}",
    'Content-Type': 'application/json'
}

get_url = f"https://api.opsgenie.com/v2/schedules/{opsgenie_schedule_id}"
response = requests.get(get_url, headers=headers)

if response.status_code == 200:
    schedule_data = response.json()
    for rotation in schedule_data['data']['rotations']:
        for participant in rotation['participants']:
            if participant.get('username') == username:
                print(json.dumps(rotation, indent=4))
else:
    print(f"Error occurred while fetching schedule for {username}. Status code: {response.status_code}")
