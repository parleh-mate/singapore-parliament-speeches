import pandas as pd
import re


def get_mp_name(x):
    if pd.notna(x) and "SPEAKER" in x:
        temp = re.search(r"\(([^()]+)\(", x)
        if temp:
            match = re.sub(r"^(?:Mr|Mrs|Miss|Mdm|Ms|Dr|Prof)\s+", "", temp.group(1))
            return match
        else:
            return ""
    elif pd.notna(x):
        match = re.search(r"(?:Mr|Mrs|Miss|Mdm|Ms|Dr|Prof)\s+([\w\s-]+)", x)
        if match:
            return match.group(1)
        else:
            return ""
    else:
        return ""
