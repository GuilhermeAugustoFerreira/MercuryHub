from rest_framework import serializers
from Governance.models import MaterialCreationRequest


class MaterialCreationRequestListSerializer(serializers.ModelSerializer):
    stage_name = serializers.SerializerMethodField()

    class Meta:
        model = MaterialCreationRequest
        fields = ['id', 'cr_number', 'status', 'stage_name', 'created_at']

    def get_stage_name(self, obj):
        return obj.get_status_display()
