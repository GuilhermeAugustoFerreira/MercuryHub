from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Governance.models import MaterialCreationRequest
from Governance.serializers import MaterialCreationRequestListSerializer
from Governance.services.workflow import advance_request_by_rule

import uuid

# Create your views here.

User = get_user_model()


class MaterialCreationRequestCreateView(APIView):
    def get(self, request):
        queryset = MaterialCreationRequest.objects.order_by('-created_at')
        serializer = MaterialCreationRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data or {}
        requester = (
            User.objects.filter(is_active=True)
            .order_by("id")
            .first()
        )

        if requester is None:
            return Response(
                {'detail': 'Nenhum usuario ativo encontrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cr_number = f"CR-{timezone.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
        payload = {
            'material_data': data.get('material_data', {}),
            'description_data': data.get('description_data', {}),
            'class_name': data.get('class_name'),
            'classification_data': data.get('classification_data', {}),
            'client_code': data.get('client_code') or data.get('client')
        }

        cr = MaterialCreationRequest.objects.create(
            cr_number=cr_number,
            requester=requester,
            status='DRAFT',
            payload=payload
        )

        return Response(
            {'id': cr.id, 'cr_number': cr.cr_number, 'status': cr.status},
            status=status.HTTP_201_CREATED
        )


class MaterialCreationRequestSubmitView(APIView):
    def post(self, request, request_id: int):
        try:
            cr = MaterialCreationRequest.objects.get(id=request_id)
        except MaterialCreationRequest.DoesNotExist:
            return Response({'detail': 'Request nao encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            cr = advance_request_by_rule(
                cr,
                role='REQUESTER',
                action='SUBMIT',
                client_code=cr.payload.get('client_code'),
                allow_unpublished=True
            )
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'id': cr.id, 'status': cr.status, 'stage_name': cr.get_status_display()},
            status=status.HTTP_200_OK
        )
