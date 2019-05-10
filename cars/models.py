from django.db import models

# Create your models here.


class Producer(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):


    name = models.CharField(max_length=20)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)


    def __str__(self):
        return self.name


class Car(models.Model):
    CATEGORY_CHOICES = (
        ('eco', 'Economic'),
        ('buss', 'Business'),
        ('first', 'First class'),
    )
    registration_number = models.CharField(max_length=20)
    people_capacity = models.PositiveIntegerField()
    manufacture_year = models.PositiveIntegerField()
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    category = models.CharField(max_length=10,choices=CATEGORY_CHOICES, blank=True)
    hybrid_or_electric = models.BooleanField(default=False)

    def __str__(self):
        return self.registration_number
