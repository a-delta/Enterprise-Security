register_module_line('Ultradns:Zone Checker - Tesco -v1', 'start', __line__())
### pack version = 3.0.15'
'''IMPORTS'''
import requests
import json

# API endpoints
login_url = "https://api.ultradns.com/authorization/token"
api_url = "https://api.ultradns.com/zones"

# Credentials
USERNAME = "your_username"
PASSWORD = "your_password"
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

# Function to make authenticated API call and collect response
def fetch_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

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
