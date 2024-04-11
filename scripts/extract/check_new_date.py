import requests
import pandas as pd
import datetime
from datetime import date
import pandas_gbq

### Variables ###

version = 2

### Methods ###

def last_date_checked(list_of_dates):
    last_date = datetime.datetime.strptime(max(list_of_dates), "%Y-%m-%d")
    print(f"Last date read: {last_date.strftime('%Y-%m-%d')}")
    return last_date


def unchecked_dates(last_date_checked):
    start_date = last_date_checked + datetime.timedelta(days=1)
    return pd.date_range(start_date, date.today())


def new_parliament_sitting_dates(unchecked_dates):
    new_dates = []
    print("Checking for dates:")
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


def process():

    # read from gbq instead of from filepath

    df = pandas_gbq.read_gbq(query_or_table = """
                                    SELECT *
                                    FROM `singapore-parliament-speeches.raw.dates`
                                    """)

    unchecked_dates_df = unchecked_dates(last_date_checked(df["Sitting_Date"]))

    new_sitting_dates_list = new_parliament_sitting_dates(unchecked_dates_df)

    append_df = prepare_df_to_append(new_sitting_dates_list, version)

    new_dates_df = pd.concat([df, append_df], ignore_index = True)

    # check for duplicates
    new_dates_df = new_dates_df.drop_duplicates(subset='Sitting_Date')

    # reupload to gbq
    pandas_gbq.to_gbq(
        new_dates_df,
        destination_table="singapore-parliament-speeches.raw.dates",
        if_exists="replace",
    )

    return append_df['Sitting_Date']
