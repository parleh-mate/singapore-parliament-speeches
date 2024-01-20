import pandas as pd
import transform.attendance as attendance

def dataframe(date_yyyymmdd, attendance_list):

    cleaned_member_names = [attendance.clean_mp_name(obj["mpName"]) for obj in attendance_list]
    original_member_names = [obj["mpName"] for obj in attendance_list]
    attendance_bool = [obj["attendance"] for obj in attendance_list]

    attendance_df = pd.DataFrame(
        {
            "Date": [date_yyyymmdd] * len(attendance_list),
            "MP_Name": cleaned_member_names,
            "Original_MP_Name": original_member_names,
            "Attendance": attendance_bool
        }
    )

    return attendance_df
    