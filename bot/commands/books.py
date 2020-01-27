import json
import requests

from config import API_BASE_URL


def _get_books_from_api(keyword):
    response = requests.get(API_BASE_URL + "/api/search_books/?keyword=" + keyword)
    if response.status_code == 200:
        books = json.loads(response.text)["data"]
        return books
    return []


def search_books(bot, update, **kwargs):
    keyword = kwargs["keyword"]
    books = _get_books_from_api(keyword)

    books_list = [
        f"{i+1}. {books[i]['name']}: {books[i]['author']}"
        for i in range(len(books))
    ]
    books_str = "\n".join(books_list)
    if len(books):
        message = f"По ключевому слову '{keyword}' найдены следующие книги:\n" + books_str
        bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        message = f"По ключевому слову '{keyword}' ничего не найдено\n"
        bot.send_message(chat_id=update.message.chat_id, text=message)
    return True


