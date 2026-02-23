from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from MaterialGlobal.models import SapCheckTableEntry
from MaterialGlobal.serializers import SapCheckTableEntrySerializer


class SapCheckTableListView(APIView):
    def get(self, request):
        domains_param = request.query_params.get('domains', '')
        domains = [item.strip().upper() for item in domains_param.split(',') if item.strip()]

        queryset = SapCheckTableEntry.objects.filter(is_active=True)
        if domains:
            queryset = queryset.filter(domain__in=domains)

        queryset = queryset.order_by('domain', 'sort_order', 'code')
        data = SapCheckTableEntrySerializer(queryset, many=True).data

        grouped: dict[str, list[dict]] = {}
        for item in data:
            domain = item['domain']
            grouped.setdefault(domain, []).append(
                {
                    'code': item['code'],
                    'description': item['description'],
                    'sort_order': item['sort_order'],
                }
            )

        return Response(grouped, status=status.HTTP_200_OK)
