from datetime import datetime


def date_str(metadata):
    date_string = metadata["sittingDate"]
    date_format = "%d-%m-%Y"

    date_object = datetime.strptime(date_string, date_format)

    return date_object.strftime("%Y-%m-%d")


def datetime_str(metadata):
    datetime_string = f"{metadata['sittingDate']} {metadata['startTimeStr']}"
    datetime_string = datetime_string.replace("noon", "PM")

    datetime_format = "%d-%m-%Y %I:%M %p"

    datetime_object = datetime.strptime(datetime_string, datetime_format)

    return datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
