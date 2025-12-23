import json
import pathlib

def search(books_list: list, query: str) -> list:
    """
    Do searching by title or author in list
    """
    query = query.strip().lower()
    if not query:
        return books_list

    results = []
    for book in books_list:
        if query in book.get("title", "").lower() or query in book.get("author", "").lower():
            results.append(book)
    return results

def sort(data :list[dict], form_type: {"date", "title", "jenre"}) -> list[dict]:
    """
    Sorts list of dictionary by key
    """
    return sorted(data, key=lambda x: x[form_type])

def to_next_line(text: str, max_len: int = 10) -> str:
    """
    Goes to next after max_len and lentgh of each line less then max_len
    """
    words = text.strip().split()
    lines = []
    cur_line = ""
    for word in words:
        if len(cur_line) + len(word) + (1 if cur_line else 0) <= max_len:
            cur_line += (" " if cur_line else "") + word
        else:
            lines.append(cur_line)
            cur_line = word

    if cur_line:
        lines.append(cur_line)

    return "\n".join(lines)

def shorter(x: list, limit: int = 30) -> str:
    """
    Shorten text if text more than 30 letters and it doesnt shorten words
    """
    letter_count = 0
    result = []
    for word in x.split():
        if letter_count + len(word) > limit:
            result.append("...")
            break
        result.append(word)
        letter_count += len(word)
    return " ".join(result)

def load_books():
    """Загружает JSON файл. Сейчас это - books_data.json для главной странице"""
    try:
        BASE_DIR = pathlib.Path(__file__).parent
        file_path = BASE_DIR / "books_data.json"
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return []