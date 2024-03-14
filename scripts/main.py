from utils import get_root_path, join_path
import extract
import extract.check_new_date as check_new_date
import extract.parl_json as parl_json
import transform
import load
import load.sittings as load_sittings
import load.attendance as load_attendance
import load.topics as load_topics
import load.speeches as load_speeches
import os
import sys

# set environ for token
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="token/gcp_token.json"

# 1.
# Check for new dates


def check_new_dates(seed_dates_path):
    check_new_date.process(seed_dates_path)

    return 0


# 2.
# Get dates to be processed


def dates_to_process(seed_dates_path):
    date_df = extract.get_dates_file(seed_dates_path)
    date_list = extract.dates_to_process(date_df)

    print(f"Dates to be processed: {date_list}\n")

    return date_list


# 3.
# Get JSON files for dates


def get_json(date_list):
    for date in date_list:
        url = parl_json.parliament_url(parl_json.date_yyyymmdd_to_ddmmyyyy(date))

        response = parl_json.get_json(url)

        filepath = join_path(
            join_path(get_root_path(), "resource-json"), f"{date}.json"
        )

        parl_json.save_json(response.json(), filepath)

    return 0


# 4.
# Create sittings by date


def sittings(date_list, debug=True):
    for date in date_list:
        metadata = transform.get_json(date, "metadata")
        sittings_df = load_sittings.dataframe(metadata)

        if debug == True:
            load.save_df("sittings", date, sittings_df)

        if debug == False:
            load.save_incremental_model_gbq("raw", "sittings", sittings_df)

    return sittings_df


# 5.
# Create attendance by date


def attendance(date_list, debug=True):
    for date in date_list:
        attendance_list = transform.get_json(date, "attendanceList")
        attendance_df = load_attendance.dataframe(date, attendance_list)

        if debug == True:
            load.save_df("attendance", date, attendance_df)

        if debug == False:
            load.save_incremental_model_gbq("raw", "attendance", attendance_df)

    return attendance_df


# 6.
# Create topics by date


def topics(date_list, debug=True):
    for date in date_list:
        topics_list = transform.get_json(date, "takesSectionVOList")
        topics_df = load_topics.dataframe(date, topics_list)

        if debug == True:
            load.save_df("topics", date, topics_df)

        if debug == False:
            load.save_incremental_model_gbq("raw", "topics", topics_df)

    return topics_df


# 7.
# Create speeches by date


def speeches(date_list, debug=True):
    for date in date_list:
        topics_list = transform.get_json(date, "takesSectionVOList")
        speeches_df = load_speeches.dataframe(date, topics_list)

        if debug == True:
            load.save_df("speeches", date, speeches_df)

        if debug == False:
            load.save_incremental_model_gbq("raw", "speeches", speeches_df)

    return speeches_df


# 8.
# Run all the above in production.

# Main Run

root_path = get_root_path()

seed_dates_path = join_path(join_path(root_path, "seeds"), "dates.csv")

""" while True:
    try:
        choice = int(
            input("Enter the part of the code to execute (1, 2, 3, 4, 5, 6, 7, 8): ")
        )
        if choice == 0:
            break
        elif choice == 1:
            check_new_dates(seed_dates_path)
        elif choice == 2:
            dates_to_process(seed_dates_path)
        elif choice == 3:
            get_json(dates_to_process(seed_dates_path))
        elif choice == 4:
            sittings(dates_to_process(seed_dates_path), debug=True)
        elif choice == 5:
            attendance(dates_to_process(seed_dates_path), debug=True)
        elif choice == 6:
            topics(dates_to_process(seed_dates_path), debug=True)
        elif choice == 7:
            speeches(dates_to_process(seed_dates_path), debug=True)
        elif choice == 8:
            process_dates = dates_to_process(seed_dates_path)
            get_json(process_dates)
            sittings(process_dates, debug=False)
            attendance(process_dates, debug=False)
            topics(process_dates, debug=False)
            speeches(process_dates, debug=False)
        else:
            continue

    except ValueError:
        print("Invalid input. Please enter a number.") """

try:
    process_dates = dates_to_process(seed_dates_path)
    get_json(process_dates)
    sittings(process_dates, debug=False)
    attendance(process_dates, debug=False)
    topics(process_dates, debug=False)
    speeches(process_dates, debug=False)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit("Stopping the script due to an error.")
