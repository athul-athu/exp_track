import requests
import json

# API endpoint
url = 'http://localhost:8000/api/v1/create_user/'

# Invalid data to test validation
invalid_data = {
    "name": "John Doe",
    "phone_number": "123",  # Invalid phone number
    "age": 200,  # Invalid age
    "bank_account_name": "John Doe Savings"
}

# Make the POST request
response = requests.post(url, json=invalid_data)

# Print the response
print("\nTesting with invalid data:")
print("\nResponse Status:", response.status_code)
print("\nResponse Body:", json.dumps(response.json(), indent=2)) 