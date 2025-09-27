from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from Classification.models import ClassHeader, Characteristic, CharacteristicValue
from .serializers import ClassHeaderSerializer, CharacteristicSerializer, CharacteristicValueSerializer

class ClassHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassHeader.objects.all()
    serializer_class = ClassHeaderSerializer

class CharacteristicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer

class CharacteristicValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CharacteristicValue.objects.all()
    serializer_class = CharacteristicValueSerializer
