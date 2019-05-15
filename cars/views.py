import csv
import io
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Car, CarModel, Producer
from .serializers import CarModelSerializer, CarModelModelSerializer, ProducerModelSerializer, FileSerializer


class CarModelViewset(ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = Car.objects.all()

    def get_serializer_class(self):
        if self.action == 'import_models':
            return FileSerializer
        return super(CarModelViewset, self).get_serializer_class()

    def get_serializer_context(self):
        context = super(CarModelViewset, self).get_serializer_context()
        if self.action == 'update':
            context['fields'] = ('registration_number', 'people_capacity', 'manufacture_year',\
                        'category', 'hybrid_or_electric', 'model_id')
        return context

    @action(detail=False, methods=['post',], url_path='importmodels')
    def import_models(self, request):
        file = request.FILES['file']
        text = file.read().decode('utf-8')
        for row in text.split('\n')[1:]:
            if len(row) < 3:
                continue
            row = row.split(', ')
            # producer_serializer = ProducerModelSerializer(data={'name':row[0]})
            producer,_ = Producer.objects.get_or_create(name=row[0])
            print(producer.id)
            car_model_serializer = CarModelModelSerializer(data={'producer_id': producer.id, 'name':row[1], 'type':row[2]})
            if car_model_serializer.is_valid():
                car_model_serializer.save()
            else:
                return Response(car_model_serializer.errors)

        return Response({'Succes':True})

class CarModelModelViewset(ModelViewSet):
    serializer_class = CarModelModelSerializer
    queryset = CarModel.objects.all()


class ProducerModelViewset(ModelViewSet):
    serializer_class = ProducerModelSerializer
    queryset = Producer.objects.all()