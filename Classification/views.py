from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from Classification.models import ClassHeader, Characteristic, CharacteristicValue, ClassCharacteristic
from .serializers import (
    ClassHeaderSerializer,
    CharacteristicSerializer,
    CharacteristicValueSerializer,
    ClassCharacteristicSerializer,
    ClassHeaderDetailSerializer,
    AvailableCharacteristicSerializer
)
from django.db import transaction
from django.db.models import Max
from django.core.paginator import Paginator

class ClassHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassHeader.objects.all()
    serializer_class = ClassHeaderSerializer

class CharacteristicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer

class CharacteristicValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CharacteristicValue.objects.all()
    serializer_class = CharacteristicValueSerializer

class ClassCharacteristicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassCharacteristic.objects.all()
    serializer_class = ClassCharacteristicSerializer

class ClassHeaderDetailView(generics.RetrieveAPIView):
    queryset = ClassHeader.objects.all().prefetch_related('class_characteristics__characteristic')
    serializer_class = ClassHeaderDetailSerializer
    lookup_field = 'internal_class_number'

class ClassCharacteristicBulkLinkView(APIView):
    def post(self, request):
        client = request.data.get('client')
        class_name = request.data.get('class_name')
        order = request.data.get('order')

        if not client or not class_name or not isinstance(order, list) or not order:
            return Response(
                {'detail': 'client, class_name e order (lista) sao obrigatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_header = ClassHeader.objects.get(client=client, class_name=class_name)
        except ClassHeader.DoesNotExist:
            return Response(
                {'detail': 'Classe nao encontrada para o client informado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        created = []
        updated = []
        missing = []

        with transaction.atomic():
            for idx, name in enumerate(order, start=1):
                try:
                    characteristic = Characteristic.objects.get(client=client, name=name)
                except Characteristic.DoesNotExist:
                    missing.append(name)
                    continue

                link, was_created = ClassCharacteristic.objects.get_or_create(
                    client=client,
                    class_header=class_header,
                    characteristic=characteristic,
                    defaults=dict(
                        item_number=f"{idx:03d}",
                        archive_counter="0000",
                        object_dependent_char="0",
                    ),
                )
                if was_created:
                    created.append(name)
                else:
                    if link.item_number != f"{idx:03d}":
                        link.item_number = f"{idx:03d}"
                        link.save(update_fields=["item_number"])
                        updated.append(name)

        return Response(
            {
                'class_name': class_header.class_name,
                'created': created,
                'updated': updated,
                'missing': missing
            },
            status=status.HTTP_200_OK
        )

class ClassAvailableCharacteristicsView(APIView):
    def get(self, request, internal_class_number):
        search = request.query_params.get('search', '').strip()
        page_number = request.query_params.get('page', '1')

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        try:
            class_header = ClassHeader.objects.get(internal_class_number=internal_class_number)
        except ClassHeader.DoesNotExist:
            return Response(
                {'detail': 'Classe nao encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )

        queryset = Characteristic.objects.exclude(class_links__class_header=class_header).distinct()
        if search:
            queryset = queryset.filter(name__icontains=search)

        paginator = Paginator(queryset.order_by('name'), 20)
        page = paginator.get_page(page_number)
        serializer = AvailableCharacteristicSerializer(page.object_list, many=True)

        return Response(
            {
                'count': paginator.count,
                'page': page.number,
                'page_size': 20,
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )

class ClassCharacteristicAddView(APIView):
    def post(self, request):
        class_id = request.data.get('class_internal_id')
        characteristic_ids = request.data.get('characteristic_ids')

        if not class_id or not isinstance(characteristic_ids, list) or not characteristic_ids:
            return Response(
                {'detail': 'class_internal_id e characteristic_ids (lista) sao obrigatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_header = ClassHeader.objects.get(internal_class_number=class_id)
        except ClassHeader.DoesNotExist:
            return Response(
                {'detail': 'Classe nao encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )

        existing_links = ClassCharacteristic.objects.filter(
            class_header=class_header,
            characteristic_id__in=characteristic_ids
        ).values_list('characteristic_id', flat=True)
        existing_set = set(existing_links)

        characteristics = Characteristic.objects.filter(internal_characteristic__in=characteristic_ids)
        found_ids = set(characteristics.values_list('internal_characteristic', flat=True))
        missing = [cid for cid in characteristic_ids if cid not in found_ids]

        last_item = (
            ClassCharacteristic.objects.filter(class_header=class_header)
            .order_by('-item_number')
            .values_list('item_number', flat=True)
            .first()
        )
        last_number = int(last_item) if last_item else 0

        created = []
        with transaction.atomic():
            for characteristic in characteristics:
                if characteristic.internal_characteristic in existing_set:
                    continue
                last_number += 1
                ClassCharacteristic.objects.create(
                    client=characteristic.client,
                    class_header=class_header,
                    characteristic=characteristic,
                    item_number=f"{last_number:03d}",
                    archive_counter="0000",
                    object_dependent_char="0"
                )
                created.append(characteristic.internal_characteristic)

        return Response(
            {
                'class_internal_id': class_header.internal_class_number,
                'created': created,
                'missing': missing
            },
            status=status.HTTP_200_OK
        )
