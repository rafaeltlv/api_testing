import pytest
import requests
import json
import pandas as pd

def get_response_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        return {
            "URL": url,
            "Status Code": response.status_code,
            "Location Header": response.headers.get("location", "Not Found"),
            "Response Headers": dict(response.headers)
        }
    except requests.exceptions.RequestException as e:
        return {
            "URL": url,
            "Error": str(e)
        }

def test_urls():
    URLS = [
        "https://www.google.com/",
        "https://www.facebook.com/",
        "https://www.twitter.com/"
    ]
    response_data = [get_response_info(url) for url in URLS]
    df = pd.DataFrame(response_data, columns=["URL", "Status Code", "Location Header", "Response Headers"])
    json_data = df.to_json(orient="records")
    with open("response_info.json", "w") as file:
        file.write(json_data)
    print("Response information exported to response_info.json")

test_urls()
