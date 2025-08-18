from django.db import models

class GlobalMaterial(models.Model):
    material_number = models.CharField(max_length=18, unique=True)  # MATNR
    #material_number = models.CharField(max_length=18, blank=True, null=True) # MATNR
    deletion_indicator = models.CharField(max_length=1, blank=True, null=True)  # LVORM
    material_type = models.CharField(max_length=4)  # MTART
    industry_sector = models.CharField(max_length=1)  # MBRSH
    material_group = models.CharField(max_length=9)  # MATKL
    base_unit_of_measure = models.CharField(max_length=3)  # MEINS
    purchase_order_uom = models.CharField(max_length=3, blank=True, null=True)  # BSTME
    purchasing_value_key = models.CharField(max_length=4, blank=True, null=True)  # EKWSL
    gross_weight = models.DecimalField(max_digits=14, decimal_places=3, blank=True, null=True)  # BRGEW
    net_weight = models.DecimalField(max_digits=14, decimal_places=3, blank=True, null=True)  # NTGEW
    weight_unit = models.CharField(max_length=3, blank=True, null=True)  # GEWEI
    division = models.CharField(max_length=2, blank=True, null=True)  # SPART
    packaging_material_group = models.CharField(max_length=4, blank=True, null=True)  # MAGRV
    authorization_group = models.CharField(max_length=4, blank=True, null=True)  # BEGRU
    qm_in_procurement = models.BooleanField(default=False)  # QMPUR (interpretando CHAR 1 como booleano)
    cross_plant_status = models.CharField(max_length=2, blank=True, null=True)  # MSTAE

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'global_material'
        verbose_name = 'Global Material'
        verbose_name_plural = 'Global Materials'

    def __str__(self):
        return f"{self.material_number} - {self.material_type}"
    

class MaterialDescription(models.Model):
    material = models.ForeignKey(GlobalMaterial, on_delete=models.CASCADE, related_name='descriptions')  # MATNR
    language = models.CharField(max_length=2)  # SPRAS (Idioma, ex: 'EN', 'PT')
    description = models.CharField(max_length=40)  # MAKTL (Descrição do material)

    class Meta:
        db_table = 'material_description'
        unique_together = ('material', 'language')
        verbose_name = 'Material Description'
        verbose_name_plural = 'Material Descriptions'

    def __str__(self):
        return f"{self.material.material_number} ({self.language})"
