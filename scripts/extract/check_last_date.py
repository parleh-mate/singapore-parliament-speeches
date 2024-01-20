from utils import get_source_file_path

import requests
import pandas as pd
import datetime
from datetime import date
import os

### Variables ###

version = 2
filename = "dates.csv"

### Methods ###


def last_date_checked(list_of_dates):
    return datetime.datetime.strptime(max(list_of_dates), "%Y-%m-%d")


def unchecked_dates(last_date_checked):
    start_date = last_date_checked + datetime.timedelta(days=1)
    return pd.date_range(start_date, date.today())


def new_parliament_sitting_dates(unchecked_dates):
    new_dates = []

    for date in unchecked_dates:
        url = f"https://sprs.parl.gov.sg/search/getHansardReport/?sittingDate={date.strftime('%d-%m-%Y')}"
        response = requests.get(url)

        # Get responses
        if response.status_code == 200:
            new_dates.append(date.strftime("%Y-%m-%d"))
            print(date.strftime("%Y-%m-%d"), "ok")
        else:
            print(date.strftime("%Y-%m-%d"), "status code: ", str(response.status_code))

    return new_dates


def prepare_df_to_append(new_sitting_dates, version=2):
    return pd.DataFrame(
        {
            "Sitting_Date": new_sitting_dates,
            "Version": [version] * len(new_sitting_dates),
            "Date_Added": [date.today().strftime("%Y-%m-%d")] * len(new_sitting_dates),
        }
    )


### Main Run ###


def check_last_date():
    seeds_date = get_source_file_path()

    df = pd.read_csv(seeds_date)

    unchecked_dates_df = unchecked_dates(last_date_checked(df["Sitting_Date"]))
    new_sitting_dates_list = new_parliament_sitting_dates(unchecked_dates_df)

    append_df = prepare_df_to_append(new_sitting_dates_list, version)
    append_df.to_csv(seeds_date, mode="a", index=False, header=False)

    return 0
