import pandas as pd
import transform.attendance as attendance


def dataframe(date_yyyymmdd, attendance_list):
    attendance_df = pd.DataFrame(
        {
            "date": [date_yyyymmdd] * len(attendance_list),
            "member_name": [
                attendance.clean_mp_name(obj["mpName"]) for obj in attendance_list
            ],
            "is_present": [obj["attendance"] for obj in attendance_list],
        }
    )

    return attendance_df
