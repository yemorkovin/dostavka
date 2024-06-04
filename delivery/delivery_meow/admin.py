from django.contrib import admin
from .models import User, Role, Order

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Order)