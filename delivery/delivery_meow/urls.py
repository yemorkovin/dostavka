from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('reg', reg),
    path('suc/<str:token>', sucuser),
    path('logout', logout),
    path('update', update),
    path('ajaxLoadAddress', ajaxLoadAddress),
    path('add_order', add_order),
    path('getJsonOrder', getJsonOrder),
    path('take_order', take_order),
]
