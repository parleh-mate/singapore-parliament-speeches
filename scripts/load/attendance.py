import pandas as pd
import transform.attendance as transform_attendance

def dataframe(date_yyyymmdd, attendance_list):

    cleaned_member_names = [transform_attendance.clean_mp_name(attendance["mpName"]) for attendance in attendance_list]
    original_member_names = [attendance["mpName"] for attendance in attendance_list]
    attendance_bool = [attendance["attendance"] for attendance in attendance_list]

    attendance_df = pd.DataFrame(
        {
            "Date": [date_yyyymmdd] * len(attendance_list),
            "MP_Name": cleaned_member_names,
            "Original_MP_Name": original_member_names,
            "Attendance": attendance_bool
        }
    )

    return attendance_df
    