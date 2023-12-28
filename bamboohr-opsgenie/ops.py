import requests
import json
import logging

opsgenie_api_key = "564ac153-b565-48ae-955d-14292fbb077c"
opsgenie_schedule_id = "601ccdc8-7615-4edc-bebf-bfe731da9177"
username = "anthony@cast.ai"
override_date = "2023-11-06T12:00:00Z"

# Configure logging
logging.basicConfig(filename='ops.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                participant['username'] = "No-one"
                participant['id'] = None
                participant['type'] = 'user'
                participant['start'] = override_date
                participant['end'] = override_date
                put_url = f"{get_url}/rotations/{rotation['id']}/participants"
                put_response = requests.put(put_url, headers=headers, data=json.dumps(participant))
                if put_response.status_code == 200:
                    logging.info(f"Successfully updated schedule for {username} on November 6th.")
                    print(f"Successfully updated schedule for {username} on November 6th.")
                else:
                    logging.error(f"Error occurred while updating schedule for {username}. Status code: {put_response.status_code}")
                    print(f"Error occurred while updating schedule for {username}. Status code: {put_response.status_code}")
else:
    logging.error(f"Error occurred while fetching schedule for {username}. Status code: {response.status_code}")
    print(f"Error occurred while fetching schedule for {username}. Status code: {response.status_code}")




