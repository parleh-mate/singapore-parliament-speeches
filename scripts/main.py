from utils import get_root_path, join_path
import extract
import extract.check_new_date as check_new_date
import extract.parl_json as parl_json
import transform
import load
import load.sittings as load_sittings
import load.attendance as load_attendance
import load.topics as load_topics

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
        url = parl_json.parliament_url(
            parl_json.date_yyyymmdd_to_ddmmyyyy(date)
            )
        
        response = parl_json.get_json(url)

        filepath = join_path(
            join_path(get_root_path(), "resource-json"),
            f"{date}.json")

        parl_json.save_json(response.json(), filepath)

    return 0

# 4.
# Create sittings by date

def sittings(date_list):

    for date in date_list:

        metadata = transform.get_json(date, 'metadata')
        sittings_df = load_sittings.dataframe(metadata)

        load.save_df('sittings', date, sittings_df)

    return 0

# 5.
# Create attendance by date

def attendance(date_list):

    for date in date_list:

        attendance_list = transform.get_json(date, 'attendanceList')
        attendance_df = load_attendance.dataframe(date, attendance_list)

        load.save_df('attendance', date, attendance_df)

    return 0

# 6. 
# Create topics by date
        
def topics(date_list):

    for date in date_list:
        topics_list = transform.get_json(date, 'takesSectionVOList')
        topics_df = load_topics.dataframe(date, topics_list)

        load.save_df('topics', date, topics_df)

    return 0

# Main Run

root_path = get_root_path()

seed_dates_path = join_path(
    join_path(root_path, "seeds"),
    "dates.csv")

while(True):
    try:
        choice = int(input("Enter the part of the code to execute (1, 2, 3, 4, 5, 6): "))
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
        else:
            continue

    except ValueError:
        print("Invalid input. Please enter a number.")