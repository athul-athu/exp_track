import requests
import json

# API endpoint
url = 'http://localhost:8000/api/v1/get_all_users/'

# Make the GET request
response = requests.get(url)

# Print the response
print("\nGetting all users:")
print("\nResponse Status:", response.status_code)
print("\nResponse Body:", json.dumps(response.json(), indent=2)) 