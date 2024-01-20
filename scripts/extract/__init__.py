import requests
import json
import datetime
import pandas as pd

### Methods ###


def get_dates_file(seeds_date_filepath):
    return pd.read_csv(seeds_date_filepath)


def dates_to_process(date_df):
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    filtered_df = date_df.loc[date_df["Date_Added"] == current_date]
    date_list = list(filtered_df["Sitting_Date"])

    return date_list
