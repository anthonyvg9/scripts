import requests
import json
import xmltodict
import logging

# Configure logging
logging.basicConfig(filename='script.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
API_KEY_BAMBOOHR = "de2096afaad0257b7eb13296d985b096d9d9534c"
SUBDOMAIN_BAMBOOHR = "castai"
API_KEY_OPSGENIE = "564ac153-b565-48ae-955d-14292fbb077c"
BASE_URL_OPSGENIE = "https://api.opsgenie.com/v2/schedules"
SCHEDULE_ID_OPSGENIE = "601ccdc8-7615-4edc-bebf-bfe731da9177"
START_DATE = "2023-10-13"
END_DATE = "2023-12-31"
EMPLOYEE_ID = "118"

# BambooHR base URL
base_url_bamboohr = f"https://{SUBDOMAIN_BAMBOOHR}.bamboohr.com/api/gateway.php/castai/v1/time_off/requests/"

# Set the authentication credentials
auth = (API_KEY_BAMBOOHR, 'x')

# Make the GET request to BambooHR
response = requests.get(base_url_bamboohr, params={"start": START_DATE, "end": END_DATE, "employeeId": EMPLOYEE_ID}, auth=auth)

logging.info(f"BambooHR Response Code: {response.status_code}")
logging.info(f"BambooHR Response Content: {response.text}")

# Define employees dictionary mapping
employees_dict = {
    "118": "Anthony Velasco",
    # Add other employee mappings here
}

# Convert XML response to JSON and filter only requested and approved requests
xml_response = response.text
data_dict = xmltodict.parse(xml_response)
filtered_data = [
    {
        "name": employees_dict[req['employee']['@id']],
        "id": req['employee']['@id'],
        "status": req['status'],
        "start_date": req['start'],
        "end_date": req['end']
    } for req in data_dict['requests']['request'] if req['status'] in ['requested', 'approved']
]

json_response = json.dumps(filtered_data, indent=4)
logging.info(f"Filtered BambooHR JSON Response: {json_response}")

# Define the mapping between BambooHR employees and Opsgenie usernames
bamboohr_to_opsgenie_mapping = {
    "Anthony Velasco": {
        "username": "anthony@cast.ai",
        "rotation": "US West"  # Replace with the appropriate rotation name
    },
    # Add other mappings here
}

# Iterate over filtered_data and update Opsgenie on-call schedule
for item in filtered_data:
    if item['name'] in employees_dict:
        bamboo_hr_employee = employees_dict[item['name']]
        if bamboo_hr_employee in bamboohr_to_opsgenie_mapping:
            opsgenie_username = bamboohr_to_opsgenie_mapping[bamboo_hr_employee]['username']
            rotation_name = bamboohr_to_opsgenie_mapping[bamboo_hr_employee]['rotation']
            if opsgenie_username:
                opsgenie_payload = {
                    "user": {
                        "type": "none"
                    },
                    "startDate": item['start_date'],  # Modify here to use the start date from BambooHR
                    "endDate": item['end_date'],  # Modify here to use the end date from BambooHR
                    "rotations": [
                        {
                            "name": rotation_name
                        }
                    ]
                }
                headers = {
                    'Authorization': f"GenieKey {API_KEY_OPSGENIE}",
                    'Content-Type': 'application/json'
                }

                update_url = f"{BASE_URL_OPSGENIE}/{SCHEDULE_ID_OPSGENIE}/overrides"
                logging.info(f"Opsgenie Update URL: {update_url}")
                logging.info(f"Updating Opsgenie for {opsgenie_username} from {opsgenie_payload['startDate']} to {opsgenie_payload['endDate']} in rotation {rotation_name}.")

                try:
                    update_response = requests.post(update_url, headers=headers, json=opsgenie_payload)
                    update_response.raise_for_status()
                    if update_response.status_code == 200:
                        logging.info("Opsgenie override successful!")
                    else:
                        logging.error(f"Error occurred. Status code: {update_response.status_code}")
                except requests.exceptions.RequestException as err:
                    logging.error(f"Request failed for {opsgenie_username}: {err}")

# Fetch Opsgenie schedule data for the same timeframe
username = "anthony@cast.ai"
get_headers = {
    'Authorization': f"GenieKey {API_KEY_OPSGENIE}",
    'Content-Type': 'application/json'
}

get_url = f"{BASE_URL_OPSGENIE}/{SCHEDULE_ID_OPSGENIE}?startDate={START_DATE}&endDate={END_DATE}"
response = requests.get(get_url, headers=get_headers)

if response.status_code == 200:
    schedule_data = response.json()
    for rotation in schedule_data['data']['rotations']:
        for participant in rotation['participants']:
            if participant.get('username') == username:
                logging.info(f"Opsgenie schedule data fetched for {username}: {json.dumps(rotation, indent=4)}")
else:
    logging.error(f"Error occurred while fetching Opsgenie schedule for {username}. Status code: {response.status_code}")

# Update Opsgenie schedule with a specific override
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

url = f"{BASE_URL_OPSGENIE}/{SCHEDULE_ID_OPSGENIE}/overrides"
post_response = requests.post(url, headers=get_headers, json=data)

if post_response.status_code == 202:
    logging.info("Opsgenie override successful!")
else:   
    logging.error(f"Error occurred. Status code: {post_response.status_code}")
