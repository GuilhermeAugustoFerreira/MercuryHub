from django.contrib import admin
from django.db import models
from .models import DecisionTable, DecisionTableVersion, RuleTestCase

# Um editor maior para JSONField (sem depender de libs externas)
from django.contrib.admin.widgets import AdminTextareaWidget


class DecisionTableVersionInline(admin.TabularInline):
    model = DecisionTableVersion
    extra = 0
    fields = ("version", "status", "valid_from", "valid_to", "created_by", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True
    ordering = ("-version",)


@admin.register(DecisionTable)
class DecisionTableAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "is_active", "versions_count")
    search_fields = ("key", "name", "description")
    list_filter = ("is_active",)
    inlines = [DecisionTableVersionInline]

    @admin.display(description="Versions")
    def versions_count(self, obj):
        return obj.versions.count()


@admin.action(description="Mark selected as PUBLISHED")
def publish_selected(modeladmin, request, queryset):
    queryset.update(status="PUBLISHED")


@admin.action(description="Mark selected as DRAFT")
def draft_selected(modeladmin, request, queryset):
    queryset.update(status="DRAFT")


@admin.register(DecisionTableVersion)
class DecisionTableVersionAdmin(admin.ModelAdmin):
    list_display = (
        "table",
        "version",
        "status",
        "valid_from",
        "valid_to",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "valid_from", "valid_to", "created_at")
    search_fields = ("table__key", "table__name")
    ordering = ("table", "-version")
    readonly_fields = ("created_at",)
    actions = [publish_selected, draft_selected]

    # deixa o JSON confortável de editar (sem plugin)
    formfield_overrides = {
        models.JSONField: {"widget": AdminTextareaWidget(attrs={"rows": 20, "cols": 120})},
    }


@admin.register(RuleTestCase)
class RuleTestCaseAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "last_run_ok", "last_run_at")
    list_filter = ("last_run_ok", "last_run_at")
    search_fields = (
        "name",
        "version__table__key",
        "version__table__name",
    )
    autocomplete_fields = ("version",)
