import requests
import os

# Set up the API endpoint URL with the token as a parameter
url = "https://www.ncei.noaa.gov/cdo-web/api/v2/datasets"
#url = "https://www.ncei.noaa.gov/cdo-web/api/v2/datatypes"

# Set up the request headers with the token included
headers = {"token": os.environ.get('NOAA_TOKEN')}

# Make the GET request with the headers included
response = requests.get(url, headers=headers)

# print the response content as a string
res = response.json()
for result in res['results']:
    print(result)