from rest_framework import serializers
from Classification.models import ClassHeader, Characteristic, CharacteristicValue, CharacteristicValueText, ClassCharacteristic

class ClassHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassHeader
        fields = ['internal_class_number', 'class_type', 'class_name', 'class_status', 'class_group']

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        #fields = ['internal_characteristic', 'characteristic_name', 'data_type', 'status']
        fields = [
            'internal_characteristic',
            'name',
            'data_type',
            'character_length',
            'case_sensitive',
            'entry_required',
            'single_value',
        ]

class CharacteristicValueSerializer(serializers.ModelSerializer):
    texts = serializers.StringRelatedField(many=True)

    class Meta:
        model = CharacteristicValue
        fields = ['characteristic', 'value', 'texts']

class ClassCharacteristicSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_header.class_name', read_only=True)
    class_type = serializers.CharField(source='class_header.class_type', read_only=True)
    characteristic_id = serializers.IntegerField(source='characteristic.internal_characteristic', read_only=True)
    characteristic_name = serializers.CharField(source='characteristic.name', read_only=True)

    class Meta:
        model = ClassCharacteristic
        fields = ['class_name', 'class_type', 'characteristic_id', 'characteristic_name']

class CharacteristicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = [
            'name',
            'data_type',
            'character_length',
            'case_sensitive',
            'entry_required',
            'single_value',
            'multilingual',
            'display_allowed_values',
            'display_assigned_values',
        ]

class ClassHeaderDetailSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()

    class Meta:
        model = ClassHeader
        fields = ['internal_class_number', 'class_name', 'class_group', 'class_type', 'characteristics']

    def get_characteristics(self, obj):
        characteristics = Characteristic.objects.filter(class_links__class_header=obj).distinct()
        return CharacteristicDetailSerializer(characteristics, many=True).data

class AvailableCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = [
            'internal_characteristic',
            'name',
            'data_type',
            'character_length',
        ]
