from django.http import JsonResponse
from django.http.response import HttpResponse

from library_bot import models
from django.db.models import Q

SUCCESS = "SUCCESS"
ERROR = "ERROR"


def response(status, data, message=None):
    return JsonResponse({
        'status': status,
        'data': data,
        'message': message
    })


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
            return response(ERROR, None, "Required params: telegram_id, fullname")
    else:
        return HttpResponse(status=405)
