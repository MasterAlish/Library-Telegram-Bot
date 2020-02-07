from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from library.views import LoadBooksXlsxView

urlpatterns = [
    path('', login_required(LoadBooksXlsxView.as_view())),
    path('admin/', admin.site.urls),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('jet/', include('jet.urls', 'jet')),
    path('api/', include('library_bot.urls')),
]
