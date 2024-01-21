import load
import pandas as pd
import os


def incremental_facts(date_list, type):
    print(f"Adding the following dates to {type}: {date_list}")
    dfs_to_union = [
        pd.read_csv(load.get_csv_filename(type, date)) for date in date_list
    ]

    return pd.concat(dfs_to_union, ignore_index=True)
