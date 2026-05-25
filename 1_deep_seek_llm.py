import requests

"""
Do a simple request to our local service to see if we have any models running.
"""

url = "http://127.0.0.1:1234/v1/models"

try:
    response = requests.get(url)
    # Raise an error for bad status codes
    response.raise_for_status()
    # Parse the JSON response
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f"Error accessing local API: {e}")
