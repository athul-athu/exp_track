import requests
import json

# Test data
test_user = {
    "name": "John Doe",
    "phone_number": "+919876543210",
    "age": 25,
    "bank_account_name": "John Doe Savings",
    "password": "SecurePass123!"
}

# Create user
print("\nCreating new user:")
response = requests.post('http://127.0.0.1:8000/api/v1/create_user/', json=test_user)
print("\nResponse Status:", response.status_code)
print("\nResponse Body:", json.dumps(response.json(), indent=2))

# Verify that token is returned and is 64 characters long
if response.status_code == 201:
    data = response.json()
    token = data['data']['token']
    print("\nToken length:", len(token))
    print("Token format is correct:", len(token) == 64 and all(c in '0123456789abcdef' for c in token.lower()))
    
    # Verify password is not returned in response
    print("Password is not in response:", 'password' not in data['data']) 