import requests
import json

# Test data for login
test_credentials = {
    "phone_number": "+919876543210",  # Use the phone number from a previously created user
    "password": "SecurePass123!"
}

# Test login
print("\nTesting login with correct credentials:")
response = requests.post('http://127.0.0.1:8000/api/login/', json=test_credentials)
print("\nResponse Status:", response.status_code)
print("\nResponse Body:", json.dumps(response.json(), indent=2))

# Test with wrong password
print("\nTesting login with wrong password:")
wrong_password = test_credentials.copy()
wrong_password["password"] = "WrongPassword123!"
response = requests.post('http://127.0.0.1:8000/api/login/', json=wrong_password)
print("\nResponse Status:", response.status_code)
print("\nResponse Body:", json.dumps(response.json(), indent=2))

# Test with non-existent phone number
print("\nTesting login with non-existent phone number:")
wrong_phone = test_credentials.copy()
wrong_phone["phone_number"] = "+919999999999"
response = requests.post('http://127.0.0.1:8000/api/login/', json=wrong_phone)
print("\nResponse Status:", response.status_code)
print("\nResponse Body:", json.dumps(response.json(), indent=2)) 