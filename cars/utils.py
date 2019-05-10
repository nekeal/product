from .models import Car


def models_import():
    print(Car.objects.all())