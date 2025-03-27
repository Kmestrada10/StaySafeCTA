import requests
import json

url = "https://data.cityofchicago.org/resource/6zsd-86xi.json"
params = {"$limit": 5}  # Fetch just 5 rows for testing

response = requests.get(url, params=params)
data = response.json()

# Print the first item to see ALL fields/keys
print("Sample raw JSON record:")
print(json.dumps(data[0], indent=2))