from django.contrib import admin
from MaterialGlobal.models import GlobalMaterial, MaterialDescription, SapCheckTableEntry


@admin.register(GlobalMaterial)
class GlobalMaterialAdmin(admin.ModelAdmin):
    list_display = ('material_number', 'material_type', 'industry_sector', 'material_group', 'base_unit_of_measure')
    search_fields = ('material_number', 'material_type', 'material_group')


@admin.register(MaterialDescription)
class MaterialDescriptionAdmin(admin.ModelAdmin):
    list_display = ('material', 'language', 'description')
    search_fields = ('material__material_number', 'description')


@admin.register(SapCheckTableEntry)
class SapCheckTableEntryAdmin(admin.ModelAdmin):
    list_display = ('domain', 'code', 'description', 'sort_order', 'is_active')
    list_filter = ('domain', 'is_active')
    search_fields = ('domain', 'code', 'description')
