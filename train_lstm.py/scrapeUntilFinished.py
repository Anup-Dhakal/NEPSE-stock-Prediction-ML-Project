import requests
from bs4 import BeautifulSoup
import csv


Company_Symbol = input("Enter the company symbol: ").upper()
url = f"https://www.sharesansar.com/company/{Company_Symbol}"
Company_Id = input("Enter the company id: ")

# session to manage the cookies
session = requests.Session()

# Make a GET request to the URL
initial_response = session.get(url)

# Parse the initial response using BeautifulSoup
initial_soup = BeautifulSoup(initial_response.content, "html.parser")

# Find the CSRF token input field and extract its value
token_input = initial_soup.find("input", {"name": "_token"})
token_value = token_input["value"]

# Define the URL for the AJAX request
api_url = "https://www.sharesansar.com/company-price-history"

# Define the headers required for the POST request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": url,
    "X-Csrf-Token": token_value,
    "X-Requested-With": "XMLHttpRequest",
}

# Define the filename for the CSV file
filename = f"{Company_Symbol}_price_history.csv"

# Define the payload data for the POST request
payload = {
    "draw": 1,
    "start": 0,
    "length": 50,
    "search[value]": "",
    "search[regex]": "false",
    "company": Company_Id
}

# Define the headers for the CSV file
csv_headers = [
    "published_date",
    "open",
    "high",
    "low",
    "close",
    "per_change",
    "traded_quantity",
    "traded_amount",
    "status",
    "DT_Row_Index"
]

# Write the header row to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()

# Initialize variables for pagination
start = 0
length = 50

# Continue fetching data until the "Next" button is enabled
while True:
    # Update the payload with the current start value
    payload["start"] = start

    # Make a POST request with the payload data and headers
    response = session.post(api_url, data=payload, headers=headers)

    # Extract the data from the response
    response_data = response.json()
    data = response_data.get("data", [])

    # Check if the record finished
    if len(data) == 0:
        break

    # Write the data to the CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        for item in data:
            writer.writerow(item)

    # Increment the start value for the next iteration
    start += length

print(f"Data has been saved to {filename}")
