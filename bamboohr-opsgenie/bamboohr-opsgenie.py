import requests
import json
import xmltodict
import logging

# Configure logging
logging.basicConfig(filename='script.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# BambooHR API Details
api_key = "de2096afaad0257b7eb13296d985b096d9d9534c"
subdomain = "castai"

# Opsgenie API Details
opsgenie_api_key = "564ac153-b565-48ae-955d-14292fbb077c"
opsgenie_base_url = "https://api.opsgenie.com/v2/schedules"

# BambooHR base URL
base_url = f"https://{subdomain}.bamboohr.com/api/gateway.php/castai/v1/time_off/requests/"

# Set the parameters
params = {
    "start": "2023-10-13",
    "end": "2023-12-31",
    "employeeId": "118"
}

# Set the authentication credentials
auth = (api_key, 'x')

# Make the GET request
response = requests.get(base_url, params=params, auth=auth)

logging.info(f"Response Code: {response.status_code}")
logging.info(f"Response Content: {response.text}")

# Define employees_dict mapping
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
logging.info(f"Filtered JSON Response: {json_response}")

# Print the content of employees_dict
logging.info(f"Employees Dictionary: {employees_dict}")

# Iterate over filtered_data and update Opsgenie on-call schedule
for item in filtered_data:
    opsgenie_payload = {
        "user": item['name'],
        "type": "add",
        "start_date": item['start_date'],
        "end_date": item['end_date']
    }
    headers = {
        'Authorization': f"GenieKey {opsgenie_api_key}",
        'Content-Type': 'application/json'
    }
    opsgenie_schedule_id = "601ccdc8-7615-4edc-bebf-bfe731da9177"  # Replace with the actual Opsgenie schedule ID

    update_url = f"{opsgenie_base_url}/{opsgenie_schedule_id}/overrides"
    logging.info(f"Opsgenie Update URL: {update_url}")
    print(f"Opsgenie Update URL: {update_url}")
    try:
        update_response = requests.post(update_url, headers=headers, data=json.dumps(opsgenie_payload))
        update_response.raise_for_status()
        if update_response.status_code == 200:
            logging.info(f"Data successfully updated for {item['name']} in Opsgenie on-call schedule.")
            print(f"Data successfully updated for {item['name']} in Opsgenie on-call schedule.")
        else:
            logging.warning(f"Error occurred while updating data for {item['name']}. Status code: {update_response.status_code}")
            print(f"Error occurred while updating data for {item['name']}. Status code: {update_response.status_code}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Request failed for {item['name']}: {err}")
        print(f"Request failed for {item['name']}: {err}")
