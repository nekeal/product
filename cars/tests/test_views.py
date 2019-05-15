import pytest
import json
from model_mommy import mommy
from django.shortcuts import reverse
from rest_framework import status
from ..views import CarModelViewSet
from ..serializers import CarModelSerializer
from ..models import Car, CarModel, Producer


class TestCarModelViewSet:

    @pytest.mark.django_db
    def test_list_car_view(self, api_rf):
        request = api_rf.get(reverse('car-list'))
        car = mommy.make(Car,2)
        response = CarModelViewSet.as_view({'get':'list'})(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == CarModelSerializer(car, context={'request': request}, many=True).data

    @pytest.mark.django_db
    def test_create_car_with_id(self, api_rf):
        car_model = mommy.make(CarModel)
        data =  {
            "registration_number": "1258",
            "people_capacity": 5,
            "manufacture_year": 2005,
            "category": "eco",
            "hybrid_or_electric": False,
            "model_id": car_model.id,
        }
        request = api_rf.post(reverse('car-list'), data=data)
        response = CarModelViewSet.as_view({'post':'create'})(request)
        car = Car.objects.first()
        serializer = CarModelSerializer(car, context={'request':request})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == serializer.data

    @pytest.mark.django_db
    def test_create_car_with_new_model(self, api_rf):
        producer = mommy.make(Producer, name='Ford')
        data =  {
            "registration_number": "1258",
            "people_capacity": 5,
            "manufacture_year": 2005,
            "category": "eco",
            "hybrid_or_electric": False,
            "model": {
                'name': 'Mustang',
                'producer_id': producer.id,
                'type': 'Sedan',
            },
        }
        request = api_rf.post(reverse('car-list'), data=data)
        response = CarModelViewSet.as_view({'post':'create'})(request)
        car = Car.objects.first()
        serializer = CarModelSerializer(car, context={'request':request})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == serializer.data
    @pytest.mark.django_db
    def test_create_car_with_bad_data(self, api_rf):
        producer = mommy.make(Producer, name='Ford')
        car_model = mommy.make(CarModel)
        bad_data = {
            "registration_number": "1258",
            "people_capacity": 5,
            "manufacture_year": 2005,
            "category": "eco",
            "hybrid_or_electric": False,
            "model": {
                'name': 'Mustang',
                'producer_id': 1,
                'type': 'Sedan',
            },
            "model_id": 1
        }
        request = api_rf.post(reverse('car-list'), data=bad_data)
        response = CarModelViewSet.as_view({'post': 'create'})(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert  "Provide one of this" in str(response.data)
        bad_data = {
            "registration_number": "1258",
            "people_capacity": 5,
            "manufacture_year": 2005,
            "category": "eco",
            "hybrid_or_electric": False,
            "model": {
                'name': 'Mustang',
                'producer_id': 1,
                'type': 'Sedan',
            },
            "model_id": 1
        }
        request = api_rf.post(reverse('car-list'), data=bad_data)
        response = CarModelViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Provide one of this" in str(response.data)

    @pytest.mark.django_db
    def test_update_car_with_model_id(self, api_rf):
        car = mommy.make(Car, people_capacity=3)
        car_model = mommy.make(CarModel)
        data = {
            "registration_number": "1258",
            "people_capacity": 5,
            "manufacture_year": 2005,
            "category": "eco",
            "hybrid_or_electric": False,
            "model_id": car_model.id
        }
        request = api_rf.put(reverse('car-detail', args=(car.id,)), data=data)
        response = CarModelViewSet.as_view({'put': 'update'})(request, pk=car.id)
        car.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert car.model_id == car_model.id

    @pytest.mark.django_db
    def test_delete_car_view(self, api_rf):
        car = mommy.make(Car)
        request = api_rf.delete(reverse('car-detail', args=(car.id,)))
        response = CarModelViewSet.as_view({'delete': 'destroy'})(request, pk=car.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        assert Car.objects.first() is None