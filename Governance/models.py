# app: Governance/models.py
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class MaterialCreationRequest(models.Model):
    STATUS = [
        ("PENDING_APPROVAL", "Pending approval"),
        ("REJECTED", "Rejected (back to requester)"),
        ("APPROVED", "Approved"),
        ("CANCELLED", "Cancelled"),
    ]
    cr_number = models.CharField(max_length=20, unique=True)
    requester = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING_APPROVAL")
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="material_approvals")
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cr_number} - {self.status}"
