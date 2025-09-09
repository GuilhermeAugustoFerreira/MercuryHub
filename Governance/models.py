# app: Governance/models.py
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class MaterialCreationRequest(models.Model):
    STATUS = [
        ("DRAFT", "Draft"),
        ("PENDING_APPROVAL", "Pending approval"),
        ("UNDER_REVIEW_Global_Team", "Global Data Review"),
        ("UNDER_REVIEW_Local_Team", "Local Data Review"),
        ("UNDER_REVIEW_Tax", "Tax Team Review"),
        ("UNDER_REVIEW_Accounting", "Accounting Review"),
        ("UNDER_REVIEW_QA", "QA Review"),
        ("UNDER_REVIEW_FIN", "Finance Review"),
        ("REJECTED", "Rejected (back to requester)"),
        ("APPROVED", "Approved"),
        ("CANCELLED", "Cancelled"),
    ]

    cr_number = models.CharField(max_length=20, unique=True)
    requester = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=40, choices=STATUS, default="DRAFT")
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="material_approvals")
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cr_number} - {self.status}"
