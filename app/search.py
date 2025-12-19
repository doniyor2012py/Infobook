import json
import requests
import base64
import sys
from multitool import load_books

sys.stdout.reconfigure(encoding='utf-8')
BOOKS_FILE = "books_data.json"
url = "https://www.googleapis.com/books/v1/volumes"

def total_books(query):
    url_scr=url+f"?q={query}"
    params={"q":query}
    responce=None

def get_cover_base64(url):
    """
    Load covers by base 64
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.content
        b64 = base64.b64encode(data).decode("utf-8").replace("\n", "")
        return b64
    except Exception as e:
        print(f"Error cover: {e}")
        return None


def parse_books(query=None, max_results=20):
    """Google Books API parse books with url"""
    print(f"🔍 Searching books for '{query or 'all books'}'...")


    params = {
        "q": query or "books",
        "maxResults": max_results,
        "printType": "books",
        "filter": "ebooks",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Error fetching books:", e)
        return []

    books = []

    def normalize_date(date_str: str) -> str:
        if not date_str:
            return "—"
        parts = date_str.split("-")
        if len(parts) == 1: return f"{parts[0]}-01-01"
        if len(parts) == 2: return f"{parts[0]}-{parts[1]}-01"
        return date_str

    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        sale = item.get("saleInfo", {})
        books.append({
            "title": info.get("title", "Без названия"),
            "author": ", ".join(info.get("authors", ["Неизвестен"])),
            "language": info.get("language", "-"),
            "description": info.get("description", "Описание отсутствует"),
            "rating": info.get("averageRating", 0),
            "rating_count": info.get("ratingsCount", 0),
            "cover": info.get("imageLinks", {}).get("thumbnail", "NotFound.jpg"),
            "type": info.get("printType", "Book"),
            "price": sale.get("listPrice", {}).get("amount", "—"),
            "currency": sale.get("listPrice", {}).get("currencyCode", ""),
            "links": info.get("previewLink", ""),
            "id": item.get("id", ""),
            "date": normalize_date(info.get("publishedDate", "")),
            "jenre": ", ".join(info.get("categories", ["—"]))
        })

    # ________________Saves if it is main page books______________
    if query is None:
        with open(BOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        print(f"{len(books)} books saved to {BOOKS_FILE}")

    return books


def clean_books():
    """Remove duplicate of books by author and title"""
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            books = json.load(f)

        seen = set()
        cleaned = []

        for b in books:
            key = (b["title"].lower().strip(), b["author"].lower().strip())
            if key not in seen:
                seen.add(key)
                cleaned.append(b)

        # clean books without cover
        # cleaned = [b for b in cleaned if b["cover"] != "NotFound.jpg"]

        with open(BOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)

        print(f"{len(cleaned)} books after cleaning")
    except Exception as e:
        print("Error in clean_books:", e)



def preload_covers(books = load_books()):
    """Loads books cover"""
    for book in books:
        if book["cover"] != "NotFound.jpg":
            book["cover_b64"] = get_cover_base64(book["cover"])
        else:
            book["cover_b64"] = None
    if books == load_books():
        with open(BOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    return books

#_________________Testing_________________________________
if __name__ == "__main__":
    parse_books(query=None)
    preload_covers(load_books())
    clean_books()
