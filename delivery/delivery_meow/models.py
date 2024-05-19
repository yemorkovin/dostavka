from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование роли')

    def __str__(self):
        return self.name


class User(models.Model):
    email = models.EmailField(verbose_name='EMail: ', null=False)
    password = models.CharField(max_length=200, verbose_name='Пароль')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    login = models.CharField(max_length=200, verbose_name='Login', null=True)
    phone = models.CharField(max_length=200, verbose_name='Phone', null=True)
    level = models.IntegerField(default=0)
    token = models.TextField()
    suc = models.IntegerField(default=0)


class Order(models.Model):
    description = models.TextField(verbose_name='Описание заказа')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    courier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='courier')
    datetime = models.DateTimeField()
    date_create = models.DateTimeField(auto_now=True)
    address = models.TextField()


class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=200, verbose_name='Text')
    score = models.IntegerField()

