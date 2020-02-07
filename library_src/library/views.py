from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from xlrd import open_workbook

from library.forms import LoadBooksForm
from library_bot.models import Book


class LoadBooksXlsxView(TemplateView):
    template_name = "forms/load_books.html"

    def dispatch(self, request, *args, **kwargs):
        form = LoadBooksForm()
        context = {}
        if request.method == "POST":
            form = LoadBooksForm(request.POST, request.FILES)
            if form.is_valid():
                read_books_count, errors = self.read_books(form.files["file"])
                context["read_books_count"] = read_books_count
                context["errors"] = errors
        context["form"] = form
        return render(request, self.template_name, context)

    def read_books(self, file):
        book = open_workbook(file_contents=file.read())
        sheet = book.sheets()[0]
        errors = []
        read_books_count = 0
        for row in sheet.get_rows():
            try:
                name = str(row[1].value)
                author = str(row[2].value)
                year = int(row[3].value)
                count = int(row[4].value)
                Book.objects.get_or_create(name=name, author=author, defaults={
                    'year': year,
                    'count': count
                })
                read_books_count += 1
            except Exception as e:
                errors.append(repr(e))
        return read_books_count, errors