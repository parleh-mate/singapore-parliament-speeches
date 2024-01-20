from utils import get_root_path, join_path
import extract
from extract.check_last_date import check_last_date
import extract.parl_json as parl_json

# 1.
# Check for new dates

seed_dates_path = join_path(
    join_path(get_root_path(), "seeds"),
    "dates.csv")

check_last_date(seed_dates_path)

# 2.
# Get dates to be processed

date_df = extract.get_dates_file(seed_dates_path)
date_list = extract.dates_to_process(date_df)

print(f"Dates to be processed: {date_list}\n")

# 3.
# Get JSON files for dates

for date in date_list:
    url = parl_json.parliament_url(
        parl_json.date_yyyymmdd_to_ddmmyyyy(date)
        )
    
    response = parl_json.get_json(url)

    filepath = join_path(
        join_path(get_root_path(), "resource-json"),
        f"{date}.json")

    parl_json.save_json(response.json(), filepath)

# 4.
