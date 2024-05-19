from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
import random
def index(request):
    return render(request, 'index.html')

def reg(request):
    error = ''
    if request.method == 'POST':
        if 'reg' in request.POST:
            email = request.POST['email']
            phone = request.POST['phone']
            role = request.POST['role']
            password = make_password(request.POST['password'])
            token = generateToken()
            if not User.objects.filter(email=email).exists():
                user = User()
                user.email = email
                user.password = password
                user.role = Role.objects.filter(name=role).first()
                user.phone = phone
                user.token = token
                user.save()
                url = f'http://127.0.0.1:8000/suc/{token}'
                send_mail(subject='Активация учетной записи', message=url, from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[email])
                return render(request, 'suc.html', {'suc': 'Успешная регистрация'})
            else:
                error = 'Такой логин уже существует!'
                return render(request, 'suc.html', {'error': error})
        elif 'auth' in request.POST:
            error = ''
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                if check_password(password, user.password):
                    request.session['user'] = email
                else:
                    error += 'Пароль введен не корректно!'
            else:
                error += 'Такого пользователя не существует!'
            return render(request, 'suc.html', {'error': error})


def generateToken():
    s = 'asdfklewjtw;ogkassdklgfnmsdklgnwjklegnweklfg'
    return ''.join([s[random.randint(0, len(s) - 1)] for i in range(32)])


def sucuser(request, token):
    if User.objects.filter(token=token).exists():
        User.objects.filter(token=token).update(suc=1, token='')
        return HttpResponse('Вы успешно активировали свою учетную запись! <a href="/">Перейти на сайт</a>')
    else:
        return HttpResponse('Token не верный!')
