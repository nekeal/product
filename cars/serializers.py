
from rest_framework import serializers
from rest_framework.validators import ValidationError

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
    model = CarModelModelSerializer(required=False)
    category  = serializers.ChoiceField(source='get_category_display', choices=Car.CATEGORY_CHOICES, required=False)
    model_id = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), required=False, write_only=True)

    class Meta:
        model = Car
        fields = ('registration_number', 'people_capacity', 'manufacture_year', 'category', 'hybrid_or_electric', 'model', 'model_id', 'url')

    def __init__(self, *args, **kwargs):
        super(CarModelSerializer, self).__init__(*args, **kwargs)
        fields = kwargs['context'].pop('fields', None)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field in existing - allowed:
                self.fields.pop(field)

    def validate(self, attrs):
        if not(any([attrs.get('model'), attrs.get('model_id')])) or all([attrs.get('model'), attrs.get('model_id')]):
            raise ValidationError("Provide one of this: new model data, existing model id")
        return super(CarModelSerializer, self).validate(attrs)

    def update(self, instance, validated_data):
        return super(CarModelSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        car_model = validated_data.pop('model_id', None) or validated_data.pop('model', None)
        validated_data['category'] = validated_data.pop('get_category_display')
        if isinstance(car_model, CarModel):
            car = Car.objects.create(**validated_data, model_id=car_model.id)
        else:
            # car_model_data = validated_data.pop('model')
            car_model['producer'] = car_model.pop('producer_id')
            car_model_instance = CarModel.objects.create(**car_model)
            car = Car.objects.create(**validated_data, model=car_model_instance)
        return car


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()