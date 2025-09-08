import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

urls = [
    "https://www.litres.ru/genre/nauchpop-prochee-279724/",
    "https://www.litres.ru/genre/nauchpop-prochee-279724/?page=2"
]

def get_text(tag, default=""):
    return tag.text.strip() if tag else default

def get_attr(tag, attr, default=""):
    return tag.get(attr, default).strip() if tag and tag.has_attr(attr) else default

books = []

for url in urls:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    book_blocks = soup.select("div[data-testid='art__wrapper']")

    for block in book_blocks:
        title_tag = block.find("a", class_="Art-module__3wrtfG__content__link")

        book = {
            "title": get_attr(title_tag, "aria-label"),
            "cover": get_attr(block.find("img"), "src"),
            "author": get_text(block.find("a", attrs={"data-testid": "art__authorName--link"})),
            "type": get_text(block.find("div", class_="ArtFormat-module__3tSBaG__format")) or "PDF",
            "rating": get_text(block.find("span", attrs={"data-testid": "art__ratingAvg"})),
            "rating_count": 0,
            "price": get_text(block.find("div", attrs={"data-testid": "art__finalPrice"})),
            "links": urljoin("https://www.litres.ru", get_attr(title_tag, "href"))
        }

        try:
            book["rating_count"] = int(get_text(
                block.find("span", attrs={"data-testid": "art__ratingCount"})
            ).replace(" ", ""))
        except ValueError:
            book["rating_count"] = 0

        books.append(book)

with open("books_data.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)
