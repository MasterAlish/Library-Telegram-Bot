from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField()
    fullname = models.CharField(max_length=3000, verbose_name='ФИО сотрудника')
    blocked = models.BooleanField(default=False, verbose_name='Статус сотрудника(Активен/Заблокирован)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return "{}. {}".format(self.telegram_id, self.fullname, self.blocked, self.created_at, self.updated_at)


class Book(models.Model):
    name = models.TextField(max_length=100, verbose_name='Название книги')
    author = models.TextField(max_length=100, verbose_name='Автор книги')
    year = models.IntegerField(verbose_name='Год издания')
    count = models.CharField(max_length=1000, verbose_name='Количество экземпляров')

    def __str__(self):
        return "{}. {}".format(self.name, self.author, self.year, self.count)


class UseLog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book_name = models.TextField(max_length=100, verbose_name='Название книги')
    book_author = models.TextField(max_length=100, verbose_name='Автор книги')
    book_id = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)
    take_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации книги')
    days = models.IntegerField(verbose_name='Количество дней')
    return_date = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name='Дата возврата книги:')

    def __str__(self):
        return "{}. {}".format(self.user_id, self.book_name, self.book_author, self.book_id, self.take_date, self.days, self.return_date)
