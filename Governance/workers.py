# app: Governance/workers.py
from pyzeebe import ZeebeWorker, create_insecure_channel
from django.db import transaction
from Governance.models import MaterialCreationRequest

channel = create_insecure_channel("zeebe:26500")
worker = ZeebeWorker(channel)

@worker.task(task_type="status.sync")
def sync_status(cr_id: str, requester_action: str = None, approval_decision: str = None, **_):
    with transaction.atomic():
        mcr = MaterialCreationRequest.objects.select_for_update().get(cr_number=cr_id)
        # Cancelamento em qualquer mão
        if requester_action == "cancel" or approval_decision == "cancel":
            mcr.status = "CANCELLED"
        # Rejeição do aprovador devolve ao solicitante
        elif approval_decision == "reject":
            mcr.status = "REJECTED"
        # Submissão do solicitante volta a pendente de aprovação
        elif requester_action == "submit":
            mcr.status = "PENDING_APPROVAL"
        mcr.save()
    return {"synced": True}

def run_status_worker():
    worker.work()
