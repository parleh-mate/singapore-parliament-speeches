from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

ORDER_PAPERS_DEFAULT_URL = "https://www.parliament.gov.sg/parliamentary-business/order-paper?parliament=&displayType=All&fromDate=&toDate=&page=1&pageSize=10"
PARLIAMENT_BASE_URL = "https://www.parliament.gov.sg"


class OrderPaperParsingError(Exception):
    pass


class OrderPaperAPIRequestError(Exception):
    pass


@dataclass
class OrderPaperData:
    pdf_link: str
    pdf_title: str
    pdf_description: str
    sitting_description: str
    parliament_description: str


def get_order_papers_full_html(order_papers_url: str = ORDER_PAPERS_DEFAULT_URL) -> str:
    try:
        response = requests.get(order_papers_url)
        return response.text
    except Exception:
        raise OrderPaperAPIRequestError


def get_order_papers_html_elements(order_papers_full_html: str) -> List:
    soup = BeautifulSoup(order_papers_full_html, "html.parser")
    order_papers_html_elements = soup.find_all("div", class_="indv-votes")
    return order_papers_html_elements


def get_order_paper_pdf_link(order_paper_html: Tag) -> str:
    pdf_link_tag = order_paper_html.find("a")
    if pdf_link_tag is None:
        raise OrderPaperParsingError

    pdf_link = pdf_link_tag.get("href")

    if pdf_link_tag is None:
        raise OrderPaperParsingError
    return pdf_link


def get_order_paper_title(order_paper_html: Tag) -> str:
    title_tag = order_paper_html.find("a")
    if title_tag is None:
        raise OrderPaperParsingError

    title = title_tag.get("title")

    if title_tag is None:
        raise OrderPaperParsingError
    return title


def get_order_paper_description(order_paper_html: Tag) -> str:
    span_tag = order_paper_html.find("span")
    if span_tag is None:
        return ""

    description = span_tag.text.strip()
    return " ".join(description.split())


def get_order_paper_data(order_paper_html: Tag) -> OrderPaperData:
    _, _, sitting_description_html, parliament_description_html = (
        order_paper_html.find_all("div")
    )

    pdf_link = get_order_paper_pdf_link(order_paper_html)
    pdf_title = get_order_paper_title(order_paper_html)
    pdf_description = get_order_paper_description(order_paper_html)

    return OrderPaperData(
        pdf_link=pdf_link,
        pdf_title=pdf_title,
        pdf_description=pdf_description,
        sitting_description=sitting_description_html.text.strip(),
        parliament_description=parliament_description_html.text.strip(),
    )


def download_order_paper(order_paper_url_path: str, save_path: str):
    try:
        response = requests.get(f"{PARLIAMENT_BASE_URL}{order_paper_url_path}")
        with open(save_path, "wb") as f:
            f.write(response.content)
    except Exception:
        raise OrderPaperAPIRequestError


# def test():
#     with open("scripts/extract/order_papers.html", "r") as f:
#         order_papers_html = f.read()

#     order_papers_html = get_order_papers_html_elements(order_papers_html)
#     order_papers_pdf_data = [
#         get_order_paper_data(order_paper_html) for order_paper_html in order_papers_html
#     ]


order_papers_full_html = get_order_papers_full_html()
order_papers_html = get_order_papers_html_elements(order_papers_full_html)
order_papers_data = [
    get_order_paper_data(order_paper_html) for order_paper_html in order_papers_html
]
for order_paper_data in order_papers_data:
    download_order_paper(
        order_paper_data.pdf_link, f"test/{order_paper_data.pdf_title}"
    )


# test()
