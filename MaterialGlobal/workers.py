# app: MaterialGlobal/workers.py
from pyzeebe import ZeebeWorker, create_insecure_channel
from django.db import transaction
from django.utils import timezone
from MaterialGlobal.models import GlobalMaterial, MaterialDescription
from Governance.models import MaterialCreationRequest

channel = create_insecure_channel("zeebe:26500")
worker = ZeebeWorker(channel)

@worker.task(task_type="materials.create")
def create_material(
    cr_id: str,
    material_number: str,
    material_type: str,
    industry_sector: str,
    material_group: str,
    base_unit_of_measure: str,
    language: str,
    description: str,
    **_
):
    with transaction.atomic():
        mat, created = GlobalMaterial.objects.get_or_create(
            material_number=material_number,
            defaults=dict(
                material_type=material_type,
                industry_sector=industry_sector,
                material_group=material_group,
                base_unit_of_measure=base_unit_of_measure
            )
        )
        if not created:
            mat.material_type = material_type
            mat.industry_sector = industry_sector
            mat.material_group = material_group
            mat.base_unit_of_measure = base_unit_of_measure
            mat.save()

        MaterialDescription.objects.update_or_create(
            material=mat, language=language,
            defaults={"description": description[:40]}
        )

        mcr = MaterialCreationRequest.objects.select_for_update().get(cr_number=cr_id)
        mcr.status = "APPROVED"
        mcr.approved_at = timezone.now()
        mcr.save()

    return {"persisted": True}

def run_workers():
    worker.work()
