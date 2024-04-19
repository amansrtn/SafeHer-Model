import requests
import pickle
# Define the URL of your FastAPI endpoint
url = "https://safeher-model.onrender.com/safety_checker"

# Define the input text
text = "help help"
# Send a POST request with the input text
response = requests.post(
    url, json={"text": text}, headers={"Content-Type": "application/json"}
)

# Check if the request was successful
if response.status_code == 200:
    # Print the output
    print("Generated output:")
    print(response.text)
else:
    print("Error:", response.status_code)
