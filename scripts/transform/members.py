import pandas as pd


def transform(attendance_df, member_seeds):
    attendance_df["date"] = pd.to_datetime(attendance_df["date"], format="%Y-%m-%d")
    attendance_df = attendance_df[
        ~(
            (attendance_df["member_name"] == "")
            | (attendance_df["member_name"].isnull())
        )
    ]

    merged_df = pd.merge(
        attendance_df,
        member_seeds,
        left_on="member_name",
        right_on="mp_name",
        how="left",
    )

    dim_members = (
        merged_df.groupby(["member_name", "party", "gender"])
        .agg(
            earliest_sitting=("date", "min"),
            latest_sitting=("date", "max"),
            count_sittings_present=("is_present", lambda x: sum(x == True)),
            count_sittings_total=("date", "count"),
        )
        .reset_index()
    )

    return dim_members


def validate(members_df):
    errors = []
    for index, row in members_df.iterrows():
        # Check if party is blank or null
        if pd.isnull(row["party"]) or row["party"] == "":
            errors.append(
                f"{row['member_name']}'s party is null. Please fill in seeds."
            )

        # Check if gender is blank, null, or not 'M' or 'F'
        if (
            pd.isnull(row["gender"])
            or row["gender"] == ""
            or row["gender"] not in ["M", "F"]
        ):
            errors.append(
                f"{row['member_name']}'s gender is invalid. Please check seeds."
            )

        # Check if count_sittings_present is greater than count_sittings_total
        if row["count_sittings_present"] > row["count_sittings_total"]:
            errors.append(
                f"{row['member_name']}'s count of sittings is invalid. Sittings present ({row['count_sittings_present']}) is more than sittings total ({row['count_sittings_total']})."
            )

    if len(errors) > 0:
        for error in errors:
            print(error)
    else:
        print("No validation errors in dim_members")

    return errors
