import pandas as pd
import re, os, json
from utils import get_root_path, join_path


def get_json_filename(date_yyyymmdd):
    filepath = join_path(
        join_path(get_root_path(), "resource-json"), f"{date_yyyymmdd}.json"
    )

    return filepath


def get_json(date_yyyymmdd, section):
    filepath = get_json_filename(date_yyyymmdd)
    with open(filepath, "r") as file:
        data = json.load(file)

    return data[section]


def get_mp_name(x):
    if pd.notna(x) and "SPEAKER" in x:
        temp = re.search(r"\(([^()]+)\(", x)
        if temp:
            match = re.sub(r"^(?:Mr|Mrs|Miss|Mdm|Ms|Dr|Prof)\s+", "", temp.group(1))
            return match.strip()
        else:
            return ""
    elif pd.notna(x):
        match = re.search(r"(?:Mr|Mrs|Miss|Mdm|Ms|Dr|Prof)\s+([\w\s-]+)", x)
        if match:
            return match.group(1).strip()
        else:
            return ""
    else:
        return ""
