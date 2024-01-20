from datetime import datetime


def cid(metadata):
    return f"{metadata['parlimentNO']:03}-{metadata['sessionNO']:03}-{metadata['volumeNO']:03}-{metadata['sittingNO']:03}"


def datetime_str(metadata):
    datetime_string = f"{metadata['sittingDate']} {metadata['startTimeStr']}"
    datetime_string = datetime_string.replace("noon", "PM")

    datetime_format = "%d-%m-%Y %I:%M %p"

    datetime_object = datetime.strptime(datetime_string, datetime_format)

    return datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
