from rest_framework import serializers

from MaterialGlobal.models import SapCheckTableEntry


class SapCheckTableEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SapCheckTableEntry
        fields = ['domain', 'code', 'description', 'sort_order']
