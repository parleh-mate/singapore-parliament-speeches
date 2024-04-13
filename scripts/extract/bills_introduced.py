from dataclasses import dataclass
from datetime import datetime
from typing import List

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
    pdf_title: str
    bill_no: str
    date_introduced: str
    date_of_2nd_reading: str
    date_passed: str


def get_bills_introduced_full_html(
    order_papers_url: str = BILLS_INTRODUCED_DEFAULT_URL,
) -> str:
    try:
        response = requests.get(order_papers_url)
        return response.text
    except Exception:
        raise BillsIntroducedAPIRequestError


def get_bills_introduced_html_elements(order_papers_full_html: str) -> List:
    soup = BeautifulSoup(order_papers_full_html, "html.parser")
    order_papers_html_elements = soup.find_all("div", class_="indv-bill")
    return order_papers_html_elements


def get_bills_introduced_pdf_link(order_paper_html: Tag) -> str:
    pdf_link_tag = order_paper_html.find("a")
    if pdf_link_tag is None:
        raise BillsIntroducedParsingError

    pdf_link = pdf_link_tag.get("href")

    if pdf_link is None:
        raise BillsIntroducedParsingError
    return pdf_link


def get_bills_introduced_title(order_paper_html: Tag) -> str:
    span_tag = order_paper_html.find("span")
    if span_tag is None:
        return ""

    description = span_tag.text.strip()
    return " ".join(description.split())


# def get_bills_introduced_data(order_paper_html: Tag) -> BillsIntroducedData:
#     _, _, sitting_description_html, parliament_description_html = (
#         order_paper_html.find_all("div")
#     )

#     pdf_link = get_bills_introduced_pdf_link(order_paper_html)
#     pdf_title = get_bills_introduced_title(order_paper_html)

#     return BillsIntroducedData(
#         pdf_link=pdf_link,
#         pdf_title=pdf_title,
#     bill_no=
#     date_introduced=
#     date_of_2nd_reading=
#     date_passed=
#     )


# def download_bills_introduced(bills_introduced_url_path: str, save_path: str):
#     try:
#         response = requests.get(f"{bills_introduced_url_path}")
#         with open(save_path, "wb") as f:
#             f.write(response.content)
#     except Exception:
#         raise BillsIntroducedAPIRequestError


# def get_order_paper_pdf_file_name(order_paper_data: BillsIntroducedData) -> str:
#     _, _, day, month, year = order_paper_data.sitting_description.split()
#     sitting_date_string = " ".join([day, month, year])
#     parsed_sitting_date = datetime.strptime(sitting_date_string, "%d %B %Y")
#     pdf_file_name_prepend = parsed_sitting_date.strftime("%Y-%m-%d")

#     return f'{pdf_file_name_prepend}{"-OPS" if order_paper_data.is_order_paper_supplement else ""}'


# def download_all_order_papers() -> None:
#     order_papers_full_html = get_bills_introduced_full_html()
#     order_papers_html = get_bills_introduced_html_elements(order_papers_full_html)
#     order_papers_data = [
#         get_bills_introduced_data(order_paper_html) for order_paper_html in order_papers_html
#     ]

#     download_counter = 0
#     for order_paper_data in order_papers_data:
#         order_paper_pdf_file_name = get_order_paper_pdf_file_name(order_paper_data)
#         download_bills_introduced(
#             order_paper_data.pdf_link,
#             f"scripts/resource-orderpaper-pdf/{order_paper_pdf_file_name}.pdf",
#         )
#         download_counter += 1
#         print(f"{download_counter}/{len(order_papers_data)}")


# download_all_order_papers()

full_html = get_bills_introduced_full_html()
html_elements = get_bills_introduced_html_elements(full_html)
for i in html_elements:
    pdf_link = get_bills_introduced_pdf_link(i)
    title = get_bills_introduced_title(i)
    print(pdf_link)
    print(title)
