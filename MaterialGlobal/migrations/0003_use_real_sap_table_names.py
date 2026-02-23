from django.db import migrations


def forwards(apps, schema_editor):
    SapCheckTableEntry = apps.get_model('MaterialGlobal', 'SapCheckTableEntry')

    # Remove generic domains from previous seed (if present)
    SapCheckTableEntry.objects.filter(
        domain__in=[
            'material_type',
            'industry_sector',
            'material_group',
            'product_hierarchy',
            'base_unit_of_measure',
            'unit_of_measure',
            'weight_unit',
            'mrp_group',
        ]
    ).delete()

    rows = [
        # T134 - Material Types
        ('T134', 'ROH', 'Raw Material', 10),
        ('T134', 'HALB', 'Semi-Finished Product', 20),
        ('T134', 'FERT', 'Finished Product', 30),
        ('T134', 'HAWA', 'Trading Goods', 40),

        # T137 - Industry Sectors
        ('T137', 'M', 'Mechanical Engineering', 10),
        ('T137', 'A', 'Retail', 20),
        ('T137', 'P', 'Pharma', 30),

        # T023 - Material Groups
        ('T023', '000000001', 'Material Group 000000001', 10),
        ('T023', '000000002', 'Material Group 000000002', 20),
        ('T023', '000000003', 'Material Group 000000003', 30),

        # T179 - Product Hierarchy
        ('T179', '001', 'Corporate Level 001', 10),
        ('T179', '001001', 'Subgroup 001001', 20),
        ('T179', '001001001', 'Family 001001001', 30),

        # T006 - Units of Measure
        ('T006', 'EA', 'Each', 10),
        ('T006', 'KG', 'Kilogram', 20),
        ('T006', 'G', 'Gram', 30),
        ('T006', 'L', 'Liter', 40),
        ('T006', 'LB', 'Pound', 50),

        # T438M - MRP Group
        ('T438M', '0001', 'Default Planning Group', 10),
        ('T438M', '0002', 'High Rotation', 20),
        ('T438M', 'Z001', 'Project Materials', 30),
    ]

    for domain, code, description, sort_order in rows:
        SapCheckTableEntry.objects.update_or_create(
            domain=domain,
            code=code,
            defaults={
                'description': description,
                'sort_order': sort_order,
                'is_active': True,
            },
        )


def backwards(apps, schema_editor):
    SapCheckTableEntry = apps.get_model('MaterialGlobal', 'SapCheckTableEntry')
    SapCheckTableEntry.objects.filter(domain__in=['T134', 'T137', 'T023', 'T179', 'T006', 'T438M']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('MaterialGlobal', '0002_sapchecktableentry'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
