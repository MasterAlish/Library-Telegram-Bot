import json
import requests
from datetime import date, datetime
from config import API_BASE_URL


class Api(object):
    @staticmethod
    def get_books_from_api(keyword):
        response = requests.get(API_BASE_URL + "/api/search_books/?keyword=" + keyword)
        if response.status_code == 200:
            books = json.loads(response.text)["data"]
            return books
        return []

    @staticmethod
    def find_book_by_id(book_id):
        response = requests.get(API_BASE_URL + "/api/get_book/" + str(book_id))
        if response.status_code == 200:
            book = json.loads(response.text)["data"]
            return book
        return None

    @staticmethod
    def register_book_taking(name, telegram_id):
        response = requests.post(API_BASE_URL + "/api/register_book/", {
            "telegram_id": telegram_id,
            "book_name": name,
        })
        return response.status_code == 200

    @staticmethod
    def register_return_book(book_id, telegram_id):
        response = requests.post(API_BASE_URL + "/api/register_return_book/", {
            "return_date": datetime.now(),
            "telegram_id": telegram_id,
            "book_id": book_id
        })
        return response.status_code == 200
