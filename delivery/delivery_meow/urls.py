from django.urls import path
from .views import index, reg, sucuser

urlpatterns = [
    path('', index),
    path('reg', reg),
    path('suc/<str:token>', sucuser)
]
