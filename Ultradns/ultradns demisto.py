register_module_line('Ultradns:Zone Checker -v1', 'start', __line__())
### pack version = 3.0.15'
'''IMPORTS'''
import requests
import json

'''ENPOINTS/PARAMS'''
# API endpoints
login_url = demisto.params().get('login_url')
api_url = demisto.params().get('api_url')

# Credentials
username = demisto.params().get('username')
password = demisto.params().get('password')
grant_type = "password"

# Function to get auth token
def get_auth_token(login_url, username, password):
    try:
        response = requests.post(login_url, json={"username": username, "password": password})
        response.raise_for_status()
        return response.json().get("token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting auth token: {e}")
        return None

# Function to check zone records within zone and return response
def get_zone_props(api_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
# Function to check domain records within zone and return response
def get_domain_props():
    headers = {"Authorization": f"Bearer {token}"}
    api_url = api_url + domain
        #Define args
    args = set_args()
    domain = args[0]

# Function to make authenticated API call and collect zone response
def get_ip_props():
    headers = {"Authorization": f"Bearer {token}"}
    api_url = api_url + ip
    #Define args
    args = set_args()
    ip = args[0]

# Function to store data in a JSON file
def store_data(data, filename="api_response.json"):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    token = get_auth_token(LOGIN_URL, USERNAME, PASSWORD)
    if token:
        data = fetch_data(API_URL, token)
        if data:
            store_data(data)

def test_module():
    api_token = generate_auth_token()

    params = {'clusterId': clusterId}
    headers = {'authorization': f"Bearer {api_token}"}
    endpointURL = api_url + "orgSafeList?"

    response = requests.get(endpointURL, params=params, headers=headers, verify=False)

    if response.status_code == 200:
        return_results('ok')
    else:
        error_msg = f'Error in API call [{response.status_code}] - {response.reason}'
        return_error(error_msg)

''' COMMANDS MANAGER / SWITCH PANEL '''

try:
    if demisto.command() == 'get_domain_props':
        get_domain_props()
    elif demisto.command() == 'get_zone_props':
        get_zone_props()
    elif demisto.command() == 'get_ip_props':
        get_ip_props()
    elif demisto.command() == 'test-module':
        # This is the call made when pressing the integration test button.
        test_module()

except Exception as err:
    return_error(str(err))

register_module_line('Ultradns:Zone Checker -v1', 'end', __line__())
