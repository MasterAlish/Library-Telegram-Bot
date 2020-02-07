from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponse

from library_bot import models

SUCCESS = "SUCCESS"
ERROR = "ERROR"


def response(status, data, message=None, status_code=200):
    return JsonResponse({
        'status': status,
        'data': data,
        'message': message
    }, status=status_code)


def search_books(request):
    keyword = request.GET.get("keyword", "")
    books = models.Book.objects.all()
    if keyword:
        books = models.Book.objects.filter(Q(name__contains=keyword.title()) | Q(author__contains=keyword.title()))
    books_list = [{
        'id': book.id,
        'name': book.name,
        'author': book.author
    } for book in books]

    return response(SUCCESS, books_list)


def get_book(request, **kwargs):
    try:
        book = models.Book.objects.get(pk=kwargs['book_id'])
        book_data = {
            'id': book.id,
            'name': book.name,
            'author': book.author
        }
        return response(SUCCESS, book_data)
    except models.Book.DoesNotExist:
        return response(ERROR, None, f"Книга с номером {kwargs['book_id']} не найдена")


def find_user(request, *args, **kwargs):
    try:
        user = models.User.objects.get(telegram_id=kwargs["telegram_id"])
        return response(SUCCESS, {
            'fullname': user.fullname,
            'blocked': user.blocked
        })
    except models.User.DoesNotExist:
        return response(ERROR, None, "User not found")


def register_user(request, *args, **kwargs):
    if request.method == "POST":
        telegram_id = request.POST.get("telegram_id", "")
        fullname = request.POST.get("fullname", "")
        if telegram_id and fullname:
            users = models.User.objects.filter(telegram_id=telegram_id)
            if users.exists():
                models.User.objects.filter(telegram_id=telegram_id).update(fullname=fullname)
            else:
                models.User.objects.create(telegram_id=telegram_id, fullname=fullname)
            return response(SUCCESS, {})
        else:
            return response(ERROR, None, "Required params: telegram_id, fullname", 400)
    else:
        return HttpResponse(status=405)


def register_book(request, *args, **kwargs):
    if request.method == "POST":
        telegram_id = request.POST.get("telegram_id", "")
        book_id = request.POST.get("book_id", "")
        if telegram_id and book_id:
            users = models.User.objects.filter(telegram_id=telegram_id)
            books = models.Book.objects.filter(id=book_id)
            if users.exists() and books.exists():
                user = models.User.objects.get(telegram_id=telegram_id)
                book = models.Book.objects.get(id=book_id)
                models.UseLog.objects.create(
                    user_id=user,
                    book_id=book,
                    days=1,
                    book_name=book.name,
                    book_author=book.author,
                )
                return response(SUCCESS, {})
            else:
                return response(ERROR, None, "Пользователь или книга не найдены", 400)
        else:
            return response(ERROR, None, "Required params: telegram_id, fullname", 400)
    else:
        return HttpResponse(status=405)


def register_return_book(request, *args, **kwargs):
    if request.method == 'POST':
        telegram = request.POST.get("telegram_id", "")
        book = request.POST.get("book_id", "")
        date = request.POST.get("return_date", "")
        if telegram and book:
            book = models.Book.objects.filter(id=book)
            user = models.User.objects.filter(telegram_id=telegram)
            if book.exists() and user.exists():
                book = book.first()
                user = user.first()
                models.UseLog.objects.filter(
                    book_id=book,
                    user_id=user,
                    return_date__isnull=True
                ).update(
                    return_date=date
                )
                return response(SUCCESS, {})
            else:
                return response(ERROR, None, "На вас нет зарегистрированных книг", 400)
        else:
            return response(ERROR, None, "Required params: telegram_id, fullname", 400)
    else:
        return HttpResponse(status=405)
