import pandas as pd
from utils import get_root_path, join_path

def get_csv_filename(type, date_yyyymmdd):
    filepath = join_path(
            join_path(get_root_path(), f'resource-{type}'),
            f"{date_yyyymmdd}.csv")

    return filepath

def save_df(type, date_yyyymmdd, df):
    filepath = get_csv_filename(type, date_yyyymmdd)
    
    df.to_csv(
        filepath,
        index=False,
        mode="w"
    )

    print(f"CSV saved to: {filepath}\n")

    return 0
