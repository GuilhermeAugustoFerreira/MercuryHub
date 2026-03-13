from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from MaterialGlobal.models import SapCheckTableEntry
from MaterialGlobal.serializers import SapCheckTableEntrySerializer
from django.db import connection


class SapCheckTableListView(APIView):
    def get(self, request):
        domains_param = request.query_params.get('domains', '')
        domains = [item.strip().upper() for item in domains_param.split(',') if item.strip()]

        table_map = {
            'T134': 'T134',    # Material Types
            'T137': 'T137',    # Industry Sectors
            'T023': 'T023',    # Material Groups
            'T179': 'T179',    # Product Hierarchy
            'T006': 'T006',    # Units of Measure
            'T438M': 'T438M',  # MRP Groups
        }

        grouped: dict[str, list[dict]] = {}

        for domain in domains or table_map.keys():
            table_name = table_map.get(domain)
            if table_name:
                with connection.cursor() as cur:
                    cur.execute(f"SELECT code, description FROM {table_name} ORDER BY code")
                    rows = cur.fetchall()
                grouped[domain] = [
                    {'code': code, 'description': desc, 'sort_order': idx}
                    for idx, (code, desc) in enumerate(rows, start=1)
                ]
            else:
                queryset = SapCheckTableEntry.objects.filter(is_active=True, domain=domain).order_by('sort_order', 'code')
                data = SapCheckTableEntrySerializer(queryset, many=True).data
                grouped[domain] = [
                    {'code': item['code'], 'description': item['description'], 'sort_order': item['sort_order']}
                    for item in data
                ]

        return Response(grouped, status=status.HTTP_200_OK)
