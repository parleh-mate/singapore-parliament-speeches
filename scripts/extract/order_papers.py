from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

ORDER_PAPERS_DEFAULT_URL = "https://www.parliament.gov.sg/parliamentary-business/order-paper?parliament=&displayType=All&fromDate=&toDate=&page=1&pageSize=10000"
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
    is_order_paper_supplement: bool


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

    if pdf_link is None:
        raise OrderPaperParsingError
    return pdf_link


def get_order_paper_title(order_paper_html: Tag) -> str:
    title_tag = order_paper_html.find("a")
    if title_tag is None:
        raise OrderPaperParsingError

    title = title_tag.get("title")

    if title is None:
        raise OrderPaperParsingError
    return title


def get_order_paper_description(order_paper_html: Tag) -> str:
    span_tag = order_paper_html.find("span")
    if span_tag is None:
        return ""

    description = span_tag.text.strip()
    return " ".join(description.split())


def get_is_order_paper_supplement(pdf_title) -> bool:
    return "Sup." in pdf_title


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
        is_order_paper_supplement=get_is_order_paper_supplement(pdf_title),
    )


def download_order_paper(order_paper_url_path: str, save_path: str):
    try:
        response = requests.get(f"{PARLIAMENT_BASE_URL}{order_paper_url_path}")
        with open(save_path, "wb") as f:
            f.write(response.content)
    except Exception:
        raise OrderPaperAPIRequestError


def get_order_paper_pdf_file_name(order_paper_data: OrderPaperData) -> str:
    _, _, day, month, year = order_paper_data.sitting_description.split()
    sitting_date_string = " ".join([day, month, year])
    parsed_sitting_date = datetime.strptime(sitting_date_string, "%d %B %Y")
    pdf_file_name_prepend = parsed_sitting_date.strftime("%Y-%m-%d")

    return f'{pdf_file_name_prepend}{"-OPS" if order_paper_data.is_order_paper_supplement else ""}'


def download_all_order_papers() -> None:
    order_papers_full_html = get_order_papers_full_html()
    order_papers_html = get_order_papers_html_elements(order_papers_full_html)
    order_papers_data = [
        get_order_paper_data(order_paper_html) for order_paper_html in order_papers_html
    ]

    download_counter = 0
    for order_paper_data in order_papers_data:
        order_paper_pdf_file_name = get_order_paper_pdf_file_name(order_paper_data)
        download_order_paper(
            order_paper_data.pdf_link,
            f"scripts/resource-order-papers/{order_paper_pdf_file_name}.pdf",
        )
        download_counter += 1
        print(f"{download_counter}/{len(order_papers_data)}")


download_all_order_papers()
