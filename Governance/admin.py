# governance/admin.py
from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import AdminTextareaWidget
from .models import MaterialCreationRequest


@admin.register(MaterialCreationRequest)
class MaterialCreationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "cr_number",
        "requester",
        "status",
        "created_at",
        "approved_by",
        "approved_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("cr_number", "requester__username", "requester__email")
    readonly_fields = ("created_at", "approved_at")

    # para editar/ver o JSON payload de forma mais confortável
    formfield_overrides = {
        models.JSONField: {
            "widget": AdminTextareaWidget(attrs={"rows": 12, "cols": 120})
        },
    }
