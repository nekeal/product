
from rest_framework import serializers

from .models import Car, CarModel, Producer



class ProducerModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Producer
        fields = ('name','url')


class CarModelModelSerializer(serializers.HyperlinkedModelSerializer):
    producer = serializers.CharField(read_only=True)
    producer_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Producer.objects.all())

    def validate_type(self, value):
        return value.capitalize()

    class Meta:
        model = CarModel
        fields = ('name', 'producer', 'type', 'producer_id', 'url')


class CarModelSerializer(serializers.HyperlinkedModelSerializer):
    model = CarModelModelSerializer()
    category  = serializers.ChoiceField(source='get_category_display', choices=Car.CATEGORY_CHOICES, required=False)

    class Meta:
        model = Car
        fields = ('registration_number', 'people_capacity', 'manufacture_year', 'category', 'hybrid_or_electric', 'model', 'url')

    def update(self, instance, validated_data):
        car_model_data = validated_data.pop('model')
        car_model_data['producer'] = car_model_data.pop('producer_id')
        car_model_instance = instance.model
        car_model_serializer = self.fields['model']
        car_model_serializer.update(car_model_instance, car_model_data)
        return super(CarModelSerializer, self).update(instance, validated_data)


    def create(self, validated_data):
        car_model_data = validated_data.pop('model')
        car_model_data['producer'] = car_model_data.pop('producer_id')
        validated_data['category'] = validated_data.pop('get_category_display')
        car_model = CarModel.objects.create(**car_model_data)
        car = Car.objects.create(**validated_data, model=car_model)
        return car

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()