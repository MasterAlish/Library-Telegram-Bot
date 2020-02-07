from django.forms import Form, forms


class LoadBooksForm(Form):
    file = forms.FileField(label="Excel файл")