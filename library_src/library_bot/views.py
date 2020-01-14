from django.http import JsonResponse
from library_bot import models
from django.db.models import Q


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

    answer = {
        'status': 'SUCCESS',
        'books': books_list
    }
    return JsonResponse(answer)
