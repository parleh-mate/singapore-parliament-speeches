import os
import argparse

import extract
import extract.check_new_date as check_new_date
import extract.parl_json as parl_json
import load
import load.sittings as load_sittings
import load.attendance as load_attendance
import load.topics as load_topics
import load.speeches as load_speeches
import utils
from utils import join_path, get_root_path

# set environ for project and token
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "token/gcp_token.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "singapore-parliament-speeches"


# for usual run
def check_new_dates():
    new_dates = check_new_date.process()
    return new_dates


# for backfilling
def dates_to_process(seed_dates_path):
    date_df = extract.get_dates_file(seed_dates_path)
    date_list = extract.dates_to_process(date_df)
    return date_list


def get_json(date):
    url = parl_json.parliament_url(parl_json.date_yyyymmdd_to_ddmmyyyy(date))

    response = parl_json.get_json(url)
    response_json = response.json()
    filename = f"{date}.json"
    parl_json.upload_json(response_json, filename)

    return response_json


def sittings(json_responses, date, debug=True):
    metadata = json_responses["metadata"]
    sittings_df = load_sittings.dataframe(metadata)
    print(f"processed sittings: {date}")

    if debug == True:
        load.save_df("sittings", date, sittings_df)

    if debug == False:
        load.save_incremental_model_gbq("raw", "sittings", sittings_df)

    return sittings_df


def attendance(json_responses, date, debug=True):
    attendance_list = json_responses["attendanceList"]
    attendance_df = load_attendance.dataframe(date, attendance_list)
    print(f"processed attendance: {date}")

    if debug == True:
        load.save_df("attendance", date, attendance_df)

    if debug == False:
        load.save_incremental_model_gbq("raw", "attendance", attendance_df)

    return attendance_df


def topics(json_responses, date, debug=True):
    topics_list = json_responses["takesSectionVOList"]
    topics_df = load_topics.dataframe(date, topics_list)
    print(f"processed topics: {date}")

    if debug == True:
        load.save_df("topics", date, topics_df)

    if debug == False:
        load.save_incremental_model_gbq("raw", "topics", topics_df)

    return topics_df


def speeches(json_responses, date, debug=True):
    topics_list = json_responses["takesSectionVOList"]
    speeches_df = load_speeches.dataframe(date, topics_list)
    print(f"processed speeches: {date}")

    if debug == True:
        load.save_df("speeches", date, speeches_df)

    if debug == False:
        load.save_incremental_model_gbq("raw", "speeches", speeches_df)

    return speeches_df


# Main Run


# For information on the arguments, refer to:
# https://github.com/jeremychia/singapore-parliament-speeches/pull/10
def run():
    parser = argparse.ArgumentParser(description="Process Singapore Parliament data.")
    parser.add_argument(
        "date_source",
        type=str,
        choices=["local", "seeds_dates", "check_new_dates"],
        default="check_new_dates",
        help="Source of dates to process (default: check_new_dates)",
    )
    parser.add_argument(
        "tables",
        type=str,
        nargs="*",
        default=["sittings", "attendance", "topics", "speeches"],
        help="Tables to refresh (default: all)",
    )
    parser.add_argument(
        "--date",
        type=str,
        nargs="+",
        help="Specific dates to process (required if date_source is 'local')",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    print(f"Debug mode: {args.debug}")

    if args.date_source == "local" and not args.date:
        parser.error("--date is required when date_source is 'local'")

    print(f"Date source: {args.date_source}")
    if args.date_source == "local":
        process_dates = args.date
    elif args.date_source == "seeds_dates":
        seed_dates_path = join_path(join_path(get_root_path(), "seeds"), "dates.csv")
        process_dates = dates_to_process(seed_dates_path)
    elif args.date_source == "check_new_dates":
        process_dates = check_new_dates()
    else:
        raise ValueError("Invalid date source")

    print(f"Dates to be processed: {process_dates}")

    status = []
    for process_date in process_dates:
        try:
            json_out = get_json(process_date)
            print(f"Tables to refresh: {args.tables}")
            if "sittings" in args.tables:
                sittings(json_out, process_date, debug=args.debug)
            if "attendance" in args.tables:
                attendance(json_out, process_date, debug=args.debug)
            if "topics" in args.tables:
                topics(json_out, process_date, debug=args.debug)
            if "speeches" in args.tables:
                speeches(json_out, process_date, debug=args.debug)
            status.append(f"Scrape successful for {process_date} for {args.tables}!")

        except Exception as e:
            status.append(f"An error occurred with {process_date}: {e}")

    if not process_dates:  # check if dates list is empty
        status.append("Nothing was processed. No new dates.")
    status_message = "\n".join(status)
    print(status_message)

    if args.date_source == "check_new_dates":
        utils.send_telebot(status_message)


# For information on the arguments, refer to:
# https://github.com/jeremychia/singapore-parliament-speeches/pull/10
if __name__ == "__main__":
    run()
