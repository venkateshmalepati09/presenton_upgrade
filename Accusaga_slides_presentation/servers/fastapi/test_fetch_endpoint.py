"""
Test script to verify the data fetching logic in create_presentation endpoint.
This sends a JSON payload with user_id and list_of_queries to the /create endpoint.
"""
import requests
import json

# The sample payload provided by the user
payload_data = {
    "reportname": "visa dataset report",
    "user_id": "e23221ad-85f0-4fc6-88ec-1aad756a93e3",
    "list_of_queries": [
        "95c31c12-eb34-4693-83d2-26dcd2052add",
        "9ef79582-149a-4674-bc51-b0348d9991dd",
        "50277736-0662-4a76-9437-51d1ac2f51dd",
        "8322d846-fb00-49c3-9ca9-8af23ab684dd",
        "2bf48d89-67e2-45f8-8c3d-6e83ea696add"
    ],
    "template_filename": "Untitled design (1).docx",
    "Description": "Generate comprehensive data analysis report."
}

# Convert to JSON string (this is what the backend expects in the 'content' field)
content_json = json.dumps(payload_data)

# The request body for the /create endpoint
request_body = {
    "content": content_json,  # JSON string goes here
    "n_slides": 10,
    "language": "English"
}

# Send the request
url = "http://127.0.0.1:8000/api/v1/ppt/presentation/create"
print(f"Sending request to: {url}")
print(f"Request body content field: {content_json[:100]}...")

try:
    response = requests.post(url, json=request_body)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
