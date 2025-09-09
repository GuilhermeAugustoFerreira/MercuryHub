from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DecisionTable(models.Model):
    """
    Representa uma tabela de decisão (tipo DMN simplificado).
    Ex: 'route_create_material' ou 'required_fields_create_material'
    """
    # NEW: identifica o cliente/tenant. Use um código curto estável (ex.: "ACME", "GLOBEX").
    # Para regras "globais" (fallback), deixe em branco (null).
    client_code = models.CharField(max_length=40, null=True, blank=True, db_index=True)  # NEW

    key = models.CharField(max_length=60)  # identificador técnico (deixa de ser unique isolado)  # CHANGED
    name = models.CharField(max_length=120)  # nome legível
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'decision_table'
        verbose_name = 'Decision Table'
        verbose_name_plural = 'Decision Tables'
        # NEW: a combinação (cliente, key) é única. Permite mesma 'key' para clientes diferentes.
        unique_together = (('client_code', 'key'),)  # NEW
        indexes = [
            models.Index(fields=['client_code', 'key']),  # NEW (acelera lookup)
            models.Index(fields=['is_active']),           # NEW (filtro comum)
        ]

    def __str__(self):
        tenant = self.client_code or 'GLOBAL'
        return f"[{tenant}] {self.key} - {self.name}"


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
        indexes = [
            models.Index(fields=['status', 'valid_from', 'valid_to']),  # NEW (seleção de versão vigente)
        ]

    def __str__(self):
        tenant = self.table.client_code or 'GLOBAL'
        return f"[{tenant}] {self.table.key} v{self.version} ({self.status})"


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
