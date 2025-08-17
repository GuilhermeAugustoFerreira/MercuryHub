from django.db import models


class ClassHeader(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    internal_class_number = models.CharField(max_length=10, primary_key=True)  # CLINT (PK)
    class_type = models.CharField(max_length=3)  # KLART
    class_number = models.CharField(max_length=18)  # CLASS
    class_status = models.CharField(max_length=1, blank=True, null=True)  # STATU
    class_group = models.CharField(max_length=10, blank=True, null=True)  # KLAGR
    characteristics_table = models.CharField(max_length=20, blank=True, null=True)  # LEIST
    usage_in_superior_classes = models.CharField(max_length=1, blank=True, null=True)  # VERWE
    multiple_selection_allowed = models.BooleanField(default=False)  # CLMUL

    class Meta:
        db_table = 'class_header'
        verbose_name = 'Class Header'
        verbose_name_plural = 'Class Headers'

    def __str__(self):
        return f"{self.class_number} ({self.class_type})"


class Characteristic(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    internal_characteristic = models.CharField(max_length=10)  # ATINN (PK)
    archive_counter = models.CharField(max_length=4)  # ADZHL (PK)
    name = models.CharField(max_length=30)  # ATNAM
    data_type = models.CharField(max_length=4)  # ATFOR
    character_length = models.PositiveSmallIntegerField()  # ANZST
    case_sensitive = models.BooleanField(default=False)  # ATKLE (XFELD)
    entry_required = models.BooleanField(default=False)  # ATERF (ATXFE)
    single_value = models.BooleanField(default=False)  # ATEIN (XFELD)
    multilingual = models.BooleanField(default=False)  # ATAME (XFELD)
    display_allowed_values = models.CharField(max_length=1)  # ATWSO (ATSOR)
    display_assigned_values = models.CharField(max_length=1)  # ATBSO (ATSOR)

    class Meta:
        db_table = 'characteristic'
        verbose_name = 'Characteristic'
        verbose_name_plural = 'Characteristics'
        unique_together = (('internal_characteristic', 'archive_counter'),)

    def __str__(self):
        return f"{self.name} ({self.internal_characteristic})"


class CharacteristicValue(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    internal_characteristic = models.ForeignKey(
        'Characteristic',
        on_delete=models.CASCADE,
        db_column='internal_characteristic',
        to_field='internal_characteristic',
        related_name='values'
    )
    value_counter = models.CharField(max_length=4)  # ATZHL
    archive_counter = models.CharField(max_length=4)  # ADZHL
    value = models.CharField(max_length=30)  # ATWRT

    class Meta:
        db_table = 'characteristic_value'
        verbose_name = 'Characteristic Value'
        verbose_name_plural = 'Characteristic Values'
        unique_together = (('internal_characteristic', 'value_counter', 'archive_counter'),)

    def __str__(self):
        return f"{self.value} (ATINN: {self.internal_characteristic})"


class ObjectLink(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    config_object = models.CharField(max_length=18, primary_key=True)  # CUOBJ
    material_number = models.CharField(max_length=18, blank=True, null=True)  # MATNR

    class Meta:
        db_table = 'object_link'
        verbose_name = 'Object Link'
        verbose_name_plural = 'Object Links'

    def __str__(self):
        return f"CUOBJ: {self.config_object} - MATNR: {self.material_number}"


class ClassificationValue(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    object_key = models.CharField(max_length=50)  # OBJEK
    characteristic = models.ForeignKey(
        'Characteristic',
        on_delete=models.CASCADE,
        db_column='characteristic_id',
        to_field='internal_characteristic',
        related_name='classification_values'
    )
    value_counter = models.CharField(max_length=3)  # ATZHL
    object_class_indicator = models.CharField(max_length=1)  # MAFID
    class_type = models.CharField(max_length=3)  # KLART
    archive_counter = models.CharField(max_length=4)  # ADZHL
    characteristic_value = models.CharField(max_length=30)  # ATWRT

    class Meta:
        db_table = 'classification_value'
        verbose_name = 'Classification Value'
        verbose_name_plural = 'Classification Values'

    def __str__(self):
        return f"{self.object_key} | {self.characteristic} = {self.characteristic_value}"


class ClassCharacteristic(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    class_header = models.ForeignKey(
        'ClassHeader',
        on_delete=models.CASCADE,
        db_column='class_internal_id',
        to_field='internal_class_number',
        related_name='class_characteristics'
    )
    item_number = models.CharField(max_length=3)  # POSNR
    archive_counter = models.CharField(max_length=4)  # ADZHL
    characteristic = models.ForeignKey(
        'Characteristic',
        on_delete=models.CASCADE,
        db_column='characteristic_id',
        to_field='internal_characteristic',
        related_name='class_links'
    )
    object_dependent_char = models.CharField(max_length=10)  # OMERK

    class Meta:
        db_table = 'class_characteristic'
        verbose_name = 'Class Characteristic'
        verbose_name_plural = 'Class Characteristics'

    def __str__(self):
        return f"Class {self.class_header} | Characteristic {self.characteristic}"


class CharacteristicValueText(models.Model):
    client = models.CharField(max_length=3)  # MANDT
    characteristic_value = models.ForeignKey(
        'CharacteristicValue',
        on_delete=models.CASCADE,
        db_column='characteristic_id',
        to_field='internal_characteristic',
        related_name='texts'
    )
    counter = models.CharField(max_length=4)  # ATZHL
    language = models.CharField(max_length=1)  # SPRAS
    archive_counter = models.CharField(max_length=4)  # ADZHL
    description = models.CharField(max_length=30)  # ATWTB

    class Meta:
        db_table = 'characteristic_value_text'
        verbose_name = 'Characteristic Value Text'
        verbose_name_plural = 'Characteristic Value Texts'
        unique_together = ('characteristic_value', 'counter', 'language')

    def __str__(self):
        return f"{self.description} ({self.language})"
