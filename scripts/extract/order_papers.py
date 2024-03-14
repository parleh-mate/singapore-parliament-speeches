from dataclasses import dataclass

from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag


class OrderPaperParsingError(Exception):
    pass


@dataclass
class OrderPaperData:
    pdf_link: str
    title: str
    description: str


def get_order_papers_html(html: str):
    with open("scripts/extract/order_papers.html", "r") as f:
        order_papers_page = f.read()
    print(type(order_papers_page))

    soup = BeautifulSoup(order_papers_page, "html.parser")
    vote_proceedings_html = soup.find("div", class_="votes-proceedings-wrap")
    order_papers_html = vote_proceedings_html.find_all(
        "div", class_="col-md-6 col-xs-12"
    )
    return order_papers_html


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
    pdf_link = get_order_paper_pdf_link(order_paper_html)
    title = get_order_paper_title(order_paper_html)
    description = get_order_paper_description(order_paper_html)

    return OrderPaperData(pdf_link=pdf_link, title=title, description=description)

with open("scripts/extract/order_papers.html", "r") as f:
    order_papers_page = f.read()

order_papers_html = get_order_papers_html(order_papers_page)
order_papers_data = [get_order_paper_data(order_paper_html) for order_paper_html in order_papers_html]
