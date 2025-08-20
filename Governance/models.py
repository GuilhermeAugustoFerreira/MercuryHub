# app: Governance (novo)
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangeRequest(models.Model):
    TYPE_CHOICES = [
        ('CREATE_MAT', 'Create Material'),
        ('CHANGE_MAT', 'Change Material'),
        ('DEACTIVATE_MAT', 'Deactivate Material'),
    ]
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('IN_PROGRESS', 'In Progress'),
        ('REWORK', 'Rework'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]
    cr_number = models.CharField(max_length=20, unique=True)
    cr_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    requester = models.ForeignKey(User, on_delete=models.PROTECT, related_name='crs_opened')
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    # ponte para material alvo (pode ser null no início)
    target_material = models.ForeignKey(
        'MaterialGlobal.GlobalMaterial',
        to_field='material_number',
        db_column='material_number',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='change_requests'
    )

    # classe selecionada para classificação inicial
    class_header = models.ForeignKey(
        'Classification.ClassHeader',
        to_field='internal_class_number',
        db_column='class_internal_id',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='change_requests'
    )

    def __str__(self):
        return f"{self.cr_number} [{self.cr_type}] - {self.status}"

class ChangeRequestItem(models.Model):
    cr = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name='items')
    key = models.CharField(max_length=60)   # ex.: 'BASIC_DATA', 'SALES', 'PURCH'
    payload = models.JSONField(default=dict)  # dados propostos/alterados

class ApprovalStep(models.Model):
    ROLE_CHOICES = [
        ('GOV', 'Governance'),
        ('FIS', 'Fiscal'),
        ('ACC', 'Accounting'),
        ('QAS', 'Quality'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REWORK', 'Rework Requested'),
        ('SKIPPED', 'Skipped'),
    ]
    cr = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveSmallIntegerField()
    role = models.CharField(max_length=3, choices=ROLE_CHOICES)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ('cr', 'order')
        ordering = ['order']

class WorkflowEvent(models.Model):
    cr = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name='events')
    step = models.ForeignKey(ApprovalStep, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=40)  # ex.: 'TASK_CREATED', 'APPROVE', 'REJECT', 'VALIDATION_FAIL'
    who = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    when = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

class ValidationIssue(models.Model):
    cr = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name='issues')
    characteristic = models.ForeignKey('Classification.Characteristic', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=200)
    level = models.CharField(max_length=10, default='ERROR')  # ERROR|WARN|INFO
    created_at = models.DateTimeField(auto_now_add=True)
