import pandas as pd
from utils import get_root_path, join_path
import extract
import extract.check_new_date as check_new_date
import extract.parl_json as parl_json
import transform
import transform.members as transform_members
import load
import load.sittings as load_sittings
import load.attendance as load_attendance
import load.topics as load_topics
import load.speeches as load_speeches
import load.models as load_models

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


def sittings(date_list):
    for date in date_list:
        metadata = transform.get_json(date, "metadata")
        sittings_df = load_sittings.dataframe(metadata)

        load.save_df("sittings", date, sittings_df)

    return 0


# 5.
# Create attendance by date


def attendance(date_list):
    for date in date_list:
        attendance_list = transform.get_json(date, "attendanceList")
        attendance_df = load_attendance.dataframe(date, attendance_list)

        load.save_df("attendance", date, attendance_df)

    return 0


# 6.
# Create topics by date


def topics(date_list):
    for date in date_list:
        topics_list = transform.get_json(date, "takesSectionVOList")

        topics_df = load_topics.dataframe(date, topics_list)
        load.save_df("topics", date, topics_df)

    return 0


# 7.
# Create speeches by date


def speeches(date_list):
    for date in date_list:
        topics_list = transform.get_json(date, "takesSectionVOList")

        speeches_df = load_speeches.dataframe(date, topics_list)
        load.save_df("speeches", date, speeches_df)

    return 0


# 8.
# Create facts/dim incrementally


def incrementals(date_list):
    type_model = [
        ("sittings", "fact_sittings"),
        ("attendance", "fact_attendance"),
        ("topics", "dim_topics"),
        ("speeches", "fact_speeches"),
    ]

    for type, model in type_model:
        new_df = load_models.incremental_facts(date_list, type)
        load.save_incremental_model(model, new_df)

    return 0

# 9.
# Create dim_members (aggregated dim)

def aggregated():

    seed_members_path = join_path(join_path(root_path, "seeds"), "member.csv")

    dim_members_df = transform_members.transform(
        pd.read_csv(load.get_model_filename('fact_attendance')),
        pd.read_csv(seed_members_path)
    )

    transform_members.validate(dim_members_df)
    load.save_aggregated_model('dim_members', dim_members_df)

    return 0


# Main Run

root_path = get_root_path()

seed_dates_path = join_path(join_path(root_path, "seeds"), "dates.csv")

while True:
    try:
        choice = int(
            input("Enter the part of the code to execute (1, 2, 3, 4, 5, 6, 7, 8, 9): ")
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
            sittings(dates_to_process(seed_dates_path))
        elif choice == 5:
            attendance(dates_to_process(seed_dates_path))
        elif choice == 6:
            topics(dates_to_process(seed_dates_path))
        elif choice == 7:
            speeches(dates_to_process(seed_dates_path))
        elif choice == 8:
            incrementals(dates_to_process(seed_dates_path))
        elif choice == 9:
            aggregated()
        else:
            continue

    except ValueError:
        print("Invalid input. Please enter a number.")
