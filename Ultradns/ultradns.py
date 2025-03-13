
### pack version = 3.0.15'
'''IMPORTS'''
import requests
import json

'''ENDPOINTS/PARAMS'''
# API endpoints
login_url = "https://api.ultradns.com/authorization/token"
api_url = "https://api.ultradns.com/v3/zones/?limit=1000"

# Credentials
username = ""
password = ""
grant_type = "password"

# Function to get auth token
def get_auth_token(login_url, username, password, grant_type):
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": username, "password": password, "grant_type": grant_type}
        response = requests.post(login_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting auth token: {e}")
        return None

# if __name__ == "__main__":
#     token = get_auth_token(login_url, username, password, grant_type)
#     if token:
#         print(f"Authentication successful! Token: {token}")
#         exit()

# Function to make authenticated API call and collect response
def fetch_data(api_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(api_url, headers=headers)
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
    token = get_auth_token(login_url, username, password, grant_type)
    if token:
        data = fetch_data(api_url, token)
        if data:
            store_data(data)
