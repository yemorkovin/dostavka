from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from .models import *
import random
import  json
from .dadata import gDadata
def index(request):
    orders = []
    if 'user' in request.session:
        current_user = User.objects.filter(email=request.session['user']).first()
        if request.session['role'] == 'Клиент':
            orders = Order.objects.filter(client=current_user)

    else:
        current_user = False

    return render(request, 'index.html', {'current_user': current_user, 'orders': orders})

def reg(request):
    if 'user' in request.session:
        current_user = User.objects.filter(email=request.session['user']).first()
    else:
        current_user = False
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
                return render(request, 'suc.html', {'suc': 'Успешная регистрация', 'current_user': current_user})
            else:
                error = 'Такой логин уже существует!'
                return render(request, 'suc.html', {'error': error, 'current_user': current_user})
        elif 'auth' in request.POST:
            error = ''
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                if user.suc != 0:
                    if check_password(password, user.password):
                        request.session['user'] = email
                        request.session['role'] = user.role.name
                        return redirect('/')
                    else:
                        error += 'Пароль введен не корректно!'
                else:
                    error += 'Учетная запись не подтверждена!'
            else:
                error += 'Такого пользователя не существует!'
            return render(request, 'suc.html', {'error': error, 'current_user': current_user})


def generateToken():
    s = 'asdfklewjtw;ogkassdklgfnmsdklgnwjklegnweklfg'
    return ''.join([s[random.randint(0, len(s) - 1)] for i in range(32)])


def sucuser(request, token):
    if User.objects.filter(token=token).exists():
        User.objects.filter(token=token).update(suc=1, token='')
        return HttpResponse('Вы успешно активировали свою учетную запись! <a href="/">Перейти на сайт</a>')
    else:
        return HttpResponse('Token не верный!')

def logout(request):
    if request.method == 'POST' and 'user' in request.session:
        del request.session['user']
    if 'role' in request.session:
        del request.session['role']
    return redirect('/')


def update(request):
    if 'user' in request.session and request.method == 'POST':
        login = request.POST['login']
        email = request.POST['email']
        print(request.POST)
        User.objects.filter(email=request.session['user']).update(login=login, email=email)
    return redirect('/')


def ajaxLoadAddress(request):
    if request.method == 'POST':
        d = gDadata()
        query = request.POST['address']
        address = d.getAddress(query)
        res = '<div class="bl_location" style="width: 100%!important;padding: 10px;">'
        for i in address:
            res += f'<div data-lon="{i['data']['geo_lon']}" data-let="{i['data']['geo_lat']}" style="width: 100%!important; margin: 10px">{i['value']}</div>'
        res += '</div>'
        return HttpResponse(res)

def add_order(request):
    if 'user' in request.session and request.method == 'POST':
        print(request.POST)
        current_user = User.objects.filter(email=request.session['user']).first()
        address = request.POST['address']
        description = request.POST['description']
        lon = request.POST['lon']
        lat = request.POST['lat']
        datetime = request.POST['datetime']
        client = current_user


        order = Order()
        order.address = address
        order.description = description
        order.datetime = datetime
        order.client = client
        order.lat = lat
        order.lon = lon
        order.save()

        return redirect('/')


def getJsonOrder(request):
    orders = Order.objects.filter(status='Ожидает курьера')
    if 'user' in request.session:
        if request.session['role'] == 'Клиент':
            orders = Order.objects.filter(client=User.objects.filter(email=request.session['user']).first())
    res = {}
    res['type'] = 'FeatureCollection'
    res['features'] = []
    for order in orders:
        if 'user' in request.session:
            if request.session['role'] == 'Клиент':
                res['features'].append(
                    {
                        'type': 'Feature',
                        'id': order.id,
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [
                                order.lat,
                                order.lon

                            ]
                        },
                        'properties': {
                            "balloonContentBody": '<p><form action="/otmena" method="post"><input type="hidden" name="id_order" value="' + str(
                                order.id) + '"><button>Отменить заказ</button></form></p>',
                        }

                    }
                )
            else:
                res['features'].append(
                    {
                        'type': 'Feature',
                        'id': order.id,
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [
                                order.lat,
                                order.lon

                            ]
                        },
                        'properties': {
                            "balloonContentBody": '<p><form action="/take_order" method="post"><input type="hidden" name="id_order" value="'+str(order.id)+'"><button>Взять заказ</button></form></p>',
                        }

                    }
                )
    return JsonResponse(res)

@csrf_exempt
def take_order(request):
    if 'user' in request.session:
        if request.method == 'POST':
            current_user = User.objects.filter(email=request.session['user']).first()
            id_order = request.POST['id_order']
            Order.objects.filter(id=id_order).update(courier=current_user, status='Заказ принят')
    return redirect('/')
