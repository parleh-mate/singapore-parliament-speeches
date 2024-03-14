import csv
from dataclasses import dataclass
from datetime import datetime
from time import strftime
from typing import List

import requests

ORDER_PAPER_BASEURL = "https://www.parliament.gov.sg/docs/default-source/default-document-library/orderpaper"
HANSARD_ANALYSIS_START_DATE = datetime(2012, 9, 10)


@dataclass
class DatesCsv:
    sitting_date: str
    version: str
    date_added: str


def get_dates_csv() -> List[DatesCsv]:
    dates_csv: list[DatesCsv] = []
    with open("scripts/seeds/dates.csv") as file:
        line_count = 0
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            sitting_date, version, date_added = row
            dates_csv.append(
                DatesCsv(
                    sitting_date=sitting_date, version=version, date_added=date_added
                )
            )

    return dates_csv


def get_parliament_sitting_dates(dates_csv: List[DatesCsv]) -> List[datetime]:
    return [datetime.strptime(i.sitting_date, "%Y-%m-%d") for i in dates_csv]


def get_filtered_dates(dates: List[datetime], start_date: datetime) -> List[datetime]:
    return [date for date in dates if date > start_date]


def get_order_paper_formatted_date(date: datetime) -> str:
    return date.strftime("%-d-%b-%Y").lower()


# dates_csv = get_dates_csv()
# sitting_dates = get_parliament_sitting_dates(dates_csv)
# filtered_parliament_sitting_dates = get_filtered_dates(
#     sitting_dates, HANSARD_ANALYSIS_START_DATE
# )
# print([get_order_paper_formatted_date(i) for i in filtered_parliament_sitting_dates])


def is_downloadable(url: str) -> bool:
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get("content-type")

    if not content_type:
        return False
    if "text" in content_type.lower():
        return False
    if "html" in content_type.lower():
        return False
    return True


def download_pdf(url: str, saved_path: str) -> None:
    response = requests.get(
        "https://www.parliament.gov.sg/docs/default-source/default-document-library/sup-no-7_7-mar-2013.pdf"
    )
    with open("./test.pdf", "wb") as f:
        f.write(response.content)
