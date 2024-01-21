import pandas as pd
from utils import get_root_path, join_path
import os


def get_csv_filename(type, date_yyyymmdd):
    filepath = join_path(
        join_path(get_root_path(), f"resource-{type}"), f"{date_yyyymmdd}.csv"
    )

    return filepath


def get_model_filename(model):
    filepath = join_path(join_path(get_root_path(), f"models"), f"{model}.csv")

    return filepath


def save_df(type, date_yyyymmdd, df):
    filepath = get_csv_filename(type, date_yyyymmdd)

    df.to_csv(filepath, index=False, mode="w")

    print(f"CSV saved to: {filepath}\n")

    return 0


def save_aggregated_model(model, df):
    filepath = get_model_filename(model)

    df.to_csv(filepath, index=False, mode="w")

    print(f"CSV saved to: {filepath}\n")

    return 0


def save_incremental_model(model, new_df):
    filepath = get_model_filename(model)

    if os.path.exists(filepath):
        new_df.to_csv(filepath, index=False, mode="a")
        print(f"CSV saved to: {filepath} with {len(new_df)} rows added. \n")

    else:
        new_df.to_csv(filepath, index=False, mode="w")
        print(f"CSV saved (created) to: {filepath} with {len(new_df)} rows added. \n")

    return 0
