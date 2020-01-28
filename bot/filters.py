from telegram.ext import BaseFilter


class TextFilter(BaseFilter):
    name = 'Filters.text'

    def __init__(self, text):
        super().__init__()
        self.text = text

    def filter(self, message):
        return bool(message.text and message.text == self.text)