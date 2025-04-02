register_module_line('Ultradns:Zone Checker -v1', 'start', __line__())
### pack version = 3.0.15'
"""This Integration allows a user to check DNS zone records for assets (domains/ips)
owned by organisations and managed within the Ultradns platform.

Requirements
To use this integration ther user will need the following
## Organisation account with Ultradns
## User account (API access only)
## Account passowrd

This credentials will be need to create an authorisation bearer token which will be
used for evry api call """

'''IMPORTS'''
import requests
import json


'''ENPOINTS/PARAMS'''
# API endpoints
login_url = demisto.params().get('login_url')
api_url = demisto.params().get('api_url')
status_url = demisto.params().get('status_url')

# Credentials
username = demisto.params().get('username')
password = demisto.params().get('password')
grant_type = "password"


# Function to get auth token
def get_auth_token():
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": username, "password": password, "grant_type": grant_type}
        response = requests.post(login_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting auth token: {e}")
        return None

# Function to check zone records within zone and return response
def ultradns_get_zone_props():
    api_token = get_auth_token()
    headers = {"Authorization": f"Bearer {api_token}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        j = response.json()
        command_results = CommandResults(outputs_prefix='DNS.Zones', outputs=j)
        return command_results

    else:
        error_msg = f'Error in API call [{response.status_code}] - {response.reason}'
        return_error(error_msg)

# Function to check domain records within zone and return response
def ultradns_get_domain_props():
    api_token = get_auth_token()
    domain = demisto.args().get('domain')
    domain_url = f"{api_url}/{domain}"
    headers = {"Authorization": f"Bearer {api_token}"}

    response = requests.get(domain_url, headers=headers)

    if response.status_code == 200:
        try:
            j = response.json()  # Parse JSON safely
            if not j:  # Ensure response is not empty
                return_error("Error: API returned an empty response.")

            command_results = CommandResults(outputs_prefix='Domains.Props', outputs=j)
            return command_results  # Return the result properly
        except json.JSONDecodeError:
            return_error("Error: API response is not valid JSON.")

    else:
        error_msg = f'Error in API call [{response.status_code}] - {response.reason}'
        return_error(error_msg)

# Function to make authenticated API call and collect zone response
def ultradns_get_ip_props():
    api_token = get_auth_token()
    ip = demisto.args().get('ip')
    headers = {"Authorization": f"Bearer {api_token}"}
    ip_url = f"{api_url}/{ip}"

    response = requests.get(ip_url, headers=headers)

    if response.status_code == 200:
        try:
            j = response.json()  # Parse JSON safely
            if not j:  # Ensure response is not empty
                return_error("Error: API returned an empty response.")

            command_results = CommandResults(outputs_prefix='Ip.Props', outputs=j)
            return command_results  # Return the result properly
        except json.JSONDecodeError:
            return_error("Error: API response is not valid JSON.")

    else:
        error_msg = f'Error in API call [{response.status_code}] - {response.reason}'
        return_error(error_msg)


# Test Ultradns connectivity status
def test_module():
    api_token = get_auth_token()

    # params = {'status_url': status_url}
    headers = {'authorization': f"Bearer {api_token}"}
    endpointURL = status_url

    response = requests.get(endpointURL, headers=headers, verify=False)

    if response.status_code == 200:
        return_results('ok')
    else:
        error_msg = f'Error in API call [{response.status_code}] - {response.reason}'
        return_error(error_msg)

''' COMMANDS MANAGER / SWITCH PANEL '''

try:
    if demisto.command() == 'ultradns_get_domain_props':
        return_results(ultradns_get_domain_props())  # Ensure return value is passed
    elif demisto.command() == 'ultradns_get_zone_props':
        return_results(ultradns_get_zone_props())
    elif demisto.command() == 'ultradns_get_ip_props':
        return_results(ultradns_get_ip_props())
    elif demisto.command() == 'test-module':
        test_module()

except Exception as err:
    return_error(str(err))

register_module_line('Ultradns:Zone Checker -v1', 'end', __line__())
