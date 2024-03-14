import csv
from dataclasses import dataclass
from datetime import datetime
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


def get_sitting_dates(dates_csv: List[DatesCsv]) -> List[datetime]:
    return [datetime.strptime(i.sitting_date, "%Y-%m,%d") for i in dates_csv]


def filter_dates(dates: List[datetime], start_date: datetime) -> List[datetime]:
    return [date for date in dates if date > start_date]
