import os
import pytest
import requests
import json
import pandas as pd

def get_rocket_launches(rocket_name):
    url = f"https://api.spacexdata.com/v3/launches?rocket_id={rocket_name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_launch_info(launch):
    return {
        "Mission Name": launch["mission_name"],
        "Launch Date": launch["launch_date_utc"],
        "Launch Site": launch["launch_site"]["site_name"],
        "Launch Success": launch["launch_success"],
    }

def get_rocket_launch_data(rocket_name):
    try:
        launches = get_rocket_launches(rocket_name)
        if not launches:
            print(f"No launch data available for {rocket_name.upper()}")
            return None

        launch_data = [extract_launch_info(launch) for launch in launches]
        return pd.DataFrame(launch_data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching rocket launch data: {e}")
        return None

def print_rocket_launch_data(rocket_name, df):
    if df is not None:
        print(f"Rocket: {rocket_name.upper()}")
        print(df)
        print()

def export_rocket_launch_data(rocket_name, df):
    if df is not None:
        directory = "launch_data"
        os.makedirs(directory, exist_ok=True)
        json_filename = f"{directory}/{rocket_name}_launches.json"
        df_json = df.to_json(orient="records")
        with open(json_filename, "w") as file:
            file.write(df_json)
        print(f"Exported {rocket_name.upper()} launch data to {json_filename}")
        print("------------------------------------------------------")

def test_space_x_rockets():
    rocket_names = ["falcon1", "falcon9", "falconheavy"]
    for rocket_name in rocket_names:
        df = get_rocket_launch_data(rocket_name)
        print_rocket_launch_data(rocket_name, df)
        export_rocket_launch_data(rocket_name, df)

test_space_x_rockets()
