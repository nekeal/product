from django.contrib import admin

from .models import Car, CarModel, Producer
# Register your models here.

admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(Producer)