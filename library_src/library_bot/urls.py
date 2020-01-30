from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url('search_books/', views.search_books),
    url('find_user/(?P<telegram_id>\\d+)', views.find_user),
    url('register_user/', csrf_exempt(views.register_user)),
    url('register_book/', csrf_exempt(views.register_book)),
    url('get_book/(?P<book_id>\\d+)', views.get_book),
    url('register_return_book/', csrf_exempt(views.register_return_book))
]