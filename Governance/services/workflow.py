# governance/services/workflow.py

from django.db import transaction
from django.utils import timezone
from django.db.models import Q

from WorkflowRules.models import DecisionTable, DecisionTableVersion
from Governance.models import MaterialCreationRequest
from MaterialGlobal.models import GlobalMaterial, MaterialDescription


# ---------- utilidades de normalização ----------

def _norm(s: str | None) -> str:
    return (s or "").strip().upper()

def _norm_action(s: str | None) -> str:
    """
    Aceita 'submit', 'approve', 'reject', 'success', 'failure', 'cancel'
    e variações de caixa/espaço.
    """
    return _norm(s)

def _norm_role(s: str | None) -> str:
    """
    Aceita REQUESTER/REQUESTOR, GLOBAL_ANALYST/GLOBAL_TEAM/SYSTEM etc.
    """
    x = _norm(s)
    if x in {"REQUESTOR", "REQUESTER"}:
        return "REQUESTER"
    if x in {"GLOBAL_TEAM", "GLOBALDATATEAM", "GLOBAL_ANALYST"}:
        return "GLOBAL_ANALYST"
    if x in {"SYS", "SYSTEM"}:
        return "SYSTEM"
    return x or "REQUESTER"


# ---------- busca de versão publicada (mantém seu comportamento) ----------

def get_published_version(client_code: str | None, key: str):
    """
    Busca a versão publicada e vigente da DecisionTable para um cliente (ou GLOBAL).
    """
    now = timezone.now()

    qs = DecisionTable.objects.filter(client_code=client_code, key=key, is_active=True)
    if not qs.exists():
        qs = DecisionTable.objects.filter(client_code__isnull=True, key=key, is_active=True)

    table = qs.first()
    if not table:
        return None

    return (
        DecisionTableVersion.objects
        .filter(table=table, status='PUBLISHED')
        .filter(Q(valid_from__isnull=True) | Q(valid_from__lte=now))
        .filter(Q(valid_to__isnull=True)   | Q(valid_to__gte=now))
        .order_by('-version')
        .first()
    )


# ---------- avaliação de regra ----------

def eval_next_status(definition: dict, current_status: str, role: str, action: str) -> str | None:
    """
    Procura na lista de regras a que bate com (status atual, role, action) e retorna o next_status.
    Aceita tanto 'role' quanto 'role_responsible' no JSON.
    """
    cur = _norm(current_status)
    rl  = _norm_role(role)
    act = _norm_action(action)

    for r in definition.get("rules", []):
        r_status = _norm(r.get("current_status"))
        # suporta 'role' OU 'role_responsible'
        r_role   = _norm_role(r.get("role") or r.get("role_responsible"))
        r_act    = _norm_action(r.get("action"))

        if r_status == cur and r_role == rl and r_act == act:
            return _norm(r.get("next_status"))
    return None


# ---------- criação do material (passo especial) ----------

def _try_create_material(payload: dict) -> tuple[bool, str | None]:
    """
    Tenta criar/atualizar GlobalMaterial e MaterialDescription a partir do payload.
    Regras mínimas de obrigatórios para teste.
    """
    required = [
        "material_number",
        "material_type",
        "industry_sector",
        "material_group",
        "base_unit_of_measure",
        "language",
        "description",
    ]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return False, f"Campos obrigatórios ausentes: {', '.join(missing)}"

    try:
        with transaction.atomic():
            mat, _ = GlobalMaterial.objects.update_or_create(
                material_number=str(payload["material_number"])[:18],
                defaults=dict(
                    material_type=str(payload["material_type"])[:4],
                    industry_sector=str(payload["industry_sector"])[:1],
                    material_group=str(payload["material_group"])[:9],
                    base_unit_of_measure=str(payload["base_unit_of_measure"])[:3],
                ),
            )
            MaterialDescription.objects.update_or_create(
                material=mat,
                language=str(payload["language"])[:2].upper(),
                defaults={"description": str(payload["description"])[:40]},
            )
        return True, None
    except Exception as e:
        return False, str(e)


# ---------- motor do workflow (mantém client_code; adiciona passo CREATE_MATERIAL) ----------

@transaction.atomic
def advance_request_by_rule(
    cr: MaterialCreationRequest,
    role: str,
    action: str,
    client_code: str | None = None,
    table_key: str = "route_create_material",
):
    """
    Avança o request conforme a DecisionTable (por cliente).
    role: REQUESTER | GLOBAL_ANALYST | SYSTEM
    action: SUBMIT | APPROVE | REJECT | SUCCESS | FAILURE | CANCEL
    - Se a transição levar a CREATE_MATERIAL:
        -> tenta criar; se ok: APPROVED; se falha: volta DRAFT e grava last_error no payload.
    """
    role_n  = _norm_role(role)
    action_n = _norm_action(action)

    # prioridade: argumento > payload > None
    if client_code is None:
        client_code = (cr.payload or {}).get("client_code")

    dv = get_published_version(client_code, table_key)
    if not dv:
        raise ValueError(f"Nenhuma DecisionTable publicada para cliente={client_code} key={table_key}")

    next_status = eval_next_status(dv.definition, cr.status, role_n, action_n)
    if not next_status:
        raise ValueError(f"Sem regra para status={cr.status} role={role_n} action={action_n}")

    # Atalho: cancelamento explícito
    if action_n == "CANCEL" or next_status == "CANCELLED":
        cr.status = "CANCELLED"
        cr.save(update_fields=["status"])
        return cr

    # Passo especial: criação de material
    if next_status == "CREATE_MATERIAL":
        ok, err = _try_create_material(cr.payload or {})
        if ok:
            cr.status = "APPROVED"
            cr.approved_at = timezone.now()
            cr.save(update_fields=["status", "approved_at"])
        else:
            p = cr.payload or {}
            p["last_error"] = err or "erro desconhecido"
            cr.payload = p
            cr.status = "DRAFT"   # volta para o solicitante ajustar
            cr.save(update_fields=["payload", "status"])
        return cr

    # Transição “normal”
    cr.status = next_status
    cr.save(update_fields=["status"])
    return cr
