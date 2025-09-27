from rest_framework import serializers
from Classification.models import ClassHeader, Characteristic, CharacteristicValue, CharacteristicValueText

class ClassHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassHeader
        fields = ['internal_class_number', 'class_type', 'class_name', 'class_status', 'class_group']

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['internal_characteristic', 'characteristic_name', 'data_type', 'status']

class CharacteristicValueSerializer(serializers.ModelSerializer):
    texts = serializers.StringRelatedField(many=True)

    class Meta:
        model = CharacteristicValue
        fields = ['characteristic', 'value', 'texts']
