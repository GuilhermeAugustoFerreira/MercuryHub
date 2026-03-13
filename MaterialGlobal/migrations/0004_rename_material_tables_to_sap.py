from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('MaterialGlobal', '0003_use_real_sap_table_names'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='globalmaterial',
            table='MARA',
        ),
        migrations.AlterModelTable(
            name='materialdescription',
            table='MAKT',
        ),
    ]
