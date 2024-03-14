import pandas as pd
import pandas_gbq
import seeds
from utils import get_root_path, join_path
import os


def get_csv_filename(type, date_yyyymmdd):
    filepath = join_path(
        join_path(get_root_path(), "debug"), f"{type}-{date_yyyymmdd}.csv"
    )

    return filepath


def save_df(type, date_yyyymmdd, df):
    filepath = get_csv_filename(type, date_yyyymmdd)

    df.to_csv(filepath, index=False, mode="w")

    print(f"CSV saved to: {filepath}\n")

    return 0


def save_incremental_model_gbq(dataset, model, new_df):
    pandas_gbq.to_gbq(
        new_df,
        destination_table=f"{dataset}.test_{model}",
        project_id=seeds.project_id,
        if_exists="append",
    )

    print(f"Dataframe saved to: {dataset}.test_{model} with {len(new_df)} rows added.\n")

    return 0
