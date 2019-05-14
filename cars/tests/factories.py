import factory

from ..models import Car, CarModel, Producer


class CarFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Car

    registration_number = "Siema"
    people_capacity = 5
    manufacture_year = 2005
    model_id = 1