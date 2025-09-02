from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DecisionTable(models.Model):
    """
    Representa uma tabela de decisão (tipo DMN simplificado).
    Ex: 'route_create_material' ou 'required_fields_create_material'
    """
    key = models.CharField(max_length=60, unique=True)  # identificador técnico
    name = models.CharField(max_length=120)  # nome legível
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'decision_table'
        verbose_name = 'Decision Table'
        verbose_name_plural = 'Decision Tables'

    def __str__(self):
        return f"{self.key} - {self.name}"


class DecisionTableVersion(models.Model):
    """
    Versões de uma tabela de decisão.
    Permite manter histórico e publicar versões válidas em períodos diferentes.
    """
    table = models.ForeignKey(
        DecisionTable,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version = models.PositiveIntegerField()  # 1, 2, 3...
    status = models.CharField(
        max_length=12,
        choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published')],
        default='DRAFT'
    )
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    definition = models.JSONField(default=dict)  # a tabela em si (linhas/condições/ações)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'decision_table_version'
        unique_together = ('table', 'version')
        ordering = ['table', '-version']

    def __str__(self):
        return f"{self.table.key} v{self.version} ({self.status})"


class RuleTestCase(models.Model):
    """
    Permite validar se uma versão de tabela funciona conforme esperado.
    Ex: input -> output esperado
    """
    version = models.ForeignKey(
        DecisionTableVersion,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    name = models.CharField(max_length=120)
    input_ctx = models.JSONField(default=dict)   # ex: {"cr_type": "CREATE_MAT", "class_type": "001"}
    expected_output = models.JSONField(default=dict)  # ex: {"role_next": "GOV", "required_fields": ["BRAND_NAME"]}
    last_run_ok = models.BooleanField(null=True, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'rule_test_case'
        verbose_name = 'Rule Test Case'
        verbose_name_plural = 'Rule Test Cases'

    def __str__(self):
        return f"Test {self.name} on {self.version}"
