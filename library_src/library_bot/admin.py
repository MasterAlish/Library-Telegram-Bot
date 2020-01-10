from django.contrib import admin

from library_bot.models import User
from library_bot.models import Book
from library_bot.models import UseLog


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'year', 'count']
    list_filter = ['author']
    search_fields = ['name', 'author']
    fields = ['name', 'author', 'year', 'count']


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'fullname', 'blocked', 'created_at', 'updated_at']
    list_filter = ['fullname']
    search_fields = ['fullname']
    fields = ['telegram_id', 'fullname', 'blocked']


class UseLogAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'book_name', 'book_author', 'book_id', 'days', 'take_date', 'return_date']
    list_filter = ['book_author', 'book_name']
    search_fields = ['book_author', 'book_name']
    fields = ['user_id', 'book_name', 'book_author', 'book_id', 'days']


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(UseLog, UseLogAdmin)
