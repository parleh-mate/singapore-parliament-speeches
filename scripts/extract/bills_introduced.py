from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

# BILLS_INTRODUCED_DEFAULT_URL = "https://www.parliament.gov.sg/parliamentary-business/bills-introduced?keyword=&title=&year=&page=1&pageSize=10000"
BILLS_INTRODUCED_DEFAULT_URL = "https://www.parliament.gov.sg/parliamentary-business/bills-introduced?keyword=&title=&year=&page=1&pageSize=10"
PARLIAMENT_BASE_URL = "https://www.parliament.gov.sg"


class BillsIntroducedParsingError(Exception):
    pass


class BillsIntroducedAPIRequestError(Exception):
    pass


@dataclass
class BillsIntroducedData:
    pdf_link: str
    title: str
    bill_no: str
    date_introduced: str
    date_of_2nd_reading: Optional[str]
    date_passed: Optional[str]


def _get_bills_introduced_full_html(
    order_papers_url: str = BILLS_INTRODUCED_DEFAULT_URL,
) -> str:
    try:
        response = requests.get(order_papers_url)
        return response.text
    except Exception:
        raise BillsIntroducedAPIRequestError


def _get_bills_introduced_html_elements(order_papers_full_html: str) -> List:
    soup = BeautifulSoup(order_papers_full_html, "html.parser")
    order_papers_html_elements = soup.find_all("div", class_="indv-bill")
    return order_papers_html_elements


def _get_bills_introduced_pdf_link(order_paper_html: Tag) -> str:
    pdf_link_tag = order_paper_html.find("a")
    if pdf_link_tag is None:
        raise BillsIntroducedParsingError

    pdf_link = pdf_link_tag.get("href")

    if pdf_link is None:
        raise BillsIntroducedParsingError
    return pdf_link


def _get_bills_introduced_title(order_paper_html: Tag) -> str:
    span_tag = order_paper_html.find("span")
    if span_tag is None:
        return ""

    description = span_tag.text.strip()
    return " ".join(description.split())


def _get_bill_no(bill_no_html: Tag) -> str:
    _, bill_no = bill_no_html.text.strip().split(": ")
    return bill_no


def _get_date_introduced(date_introduced_html: Tag) -> str:
    _, raw_date_introduced = date_introduced_html.text.strip().split(": ")
    date_introduced = raw_date_introduced.strip()
    return date_introduced


def _get_date_of_2nd_reading(date_of_2nd_reading_html: Tag) -> Optional[str]:
    try:
        _, date_of_2nd_reading_raw = date_of_2nd_reading_html.text.strip().split(": ")
        date_of_2nd_reading = date_of_2nd_reading_raw.strip()
        return date_of_2nd_reading
    except ValueError:
        return None


def _get_date_passed(date_passed_html: Tag) -> Optional[str]:
    try:
        _, date_passed_raw = date_passed_html.text.strip().split(": ")
        return date_passed_raw.strip()
    except ValueError:
        return None


def _has_corrigenda(order_paper_html: Tag) -> bool:
    return len(order_paper_html.find_all("div")) == 8


def _get_bills_introduced_data(order_paper_html: Tag) -> BillsIntroducedData:
    pdf_link = _get_bills_introduced_pdf_link(order_paper_html)
    title = _get_bills_introduced_title(order_paper_html)
    (
        _,
        _,
        bill_no_html,
        _,
        date_introduced_html,
        date_of_2nd_reading_html,
        date_passed_html,
    ) = order_paper_html.find_all("div")
    bill_no = _get_bill_no(bill_no_html)
    date_introduced = _get_date_introduced(date_introduced_html)
    date_of_2nd_reading = _get_date_of_2nd_reading(date_of_2nd_reading_html)
    date_passed = _get_date_passed(date_passed_html)
    return BillsIntroducedData(
        pdf_link=pdf_link,
        title=title,
        bill_no=bill_no,
        date_introduced=date_introduced,
        date_of_2nd_reading=date_of_2nd_reading,
        date_passed=date_passed,
    )


def get_all_bills_introduced_data() -> List[BillsIntroducedData]:
    full_html = _get_bills_introduced_full_html()
    bills_introduced_html_elements = _get_bills_introduced_html_elements(full_html)
    return [
        _get_bills_introduced_data(bills_introduced_html_element)
        for bills_introduced_html_element in bills_introduced_html_elements
    ]


def download_bills_introduced(bills_introduced_full_url: str, save_path: str) -> None:
    try:
        response = requests.get(f"{bills_introduced_full_url}")
        with open(save_path, "wb") as f:
            f.write(response.content)
    except Exception:
        raise BillsIntroducedAPIRequestError


def download_all_bills_introduced_data() -> None:
    all_bills_introduced_data = get_all_bills_introduced_data()
    download_counter = 0
    for bills_introduced_data in all_bills_introduced_data:
        download_bills_introduced(
            bills_introduced_data.pdf_link,
            f"scripts/extract/resource-bills-introduced/{bills_introduced_data.title}.pdf",
        )
        download_counter += 1
        print(f"{download_counter}/{len(all_bills_introduced_data)}")


download_all_bills_introduced_data()
