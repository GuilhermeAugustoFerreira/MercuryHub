from django.db import models


class ClassHeader(models.Model): #KLAH  -> main for classes

# Função: Armazena os dados principais de uma classe no SAP.
# Campos-chave: CLINT (ID interno), CLASS (número da classe), KLART (tipo da classe).
# Uso: Define o agrupamento lógico de objetos com características comuns (por exemplo, materiais com propriedades semelhantes).

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


class Characteristic(models.Model):  #CABN  -> main for characteristics

# Função: Define as características (atributos) utilizadas para classificar objetos.
# Campos-chave: ATINN (ID interno da característica), ATNAM (nome).
# Uso: Uma característica pode ser, por exemplo, “Cor”, “Comprimento”, “Peso”. Está ligada à estrutura de classificação.

    client = models.CharField(max_length=3)  # MANDT
    #internal_characteristic = models.CharField(max_length=10)  # ATINN (PK)
    #internal_characteristic = models.CharField(max_length=10, primary_key=True)  # ATINN
    internal_characteristic = models.BigAutoField(primary_key=True) 
    archive_counter = models.CharField(max_length=4)  # ADZHL (PK)
    name = models.CharField(max_length=30, unique=True)  # ATNAM
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


class CharacteristicValue(models.Model): #CAWN

# Função: Armazena os valores possíveis atribuídos a uma característica.
# Campos-chave: ATINN, ATZHL, ATWRT.
# Uso: Para a característica “Cor”, os valores possíveis seriam “Vermelho”, “Azul”, etc.

    client = models.CharField(max_length=3)  # MANDT
    internal_characteristic = models.ForeignKey(
        'Characteristic',
        on_delete=models.CASCADE,
        db_column='internal_characteristic',
        to_field='internal_characteristic',
        related_name='values',
        # unique = True
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


class ObjectLink(models.Model): #INOB

# Função: Faz o vínculo entre um objeto do mundo real (ex: material) e a classe configurada.
# Campos-chave: CUOBJ, MATNR.
# Uso: Permite classificar materiais, equipamentos, etc., usando as classes definidas.

    client = models.CharField(max_length=3)  # MANDT
    config_object = models.CharField(max_length=18, primary_key=True)  # CUOBJ
    # material_number = models.CharField(max_length=18, blank=True, null=True)  # MATNR
    material = models.ForeignKey(
        'MaterialGlobal.GlobalMaterial',
        on_delete=models.SET_NULL,
        db_column='material_number',
        to_field='material_number',
        related_name='object_links',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'object_link'
        verbose_name = 'Object Link'
        verbose_name_plural = 'Object Links'

    def __str__(self):
        #return f"CUOBJ: {self.config_object} - MATNR: {self.material_number}"
        return f"CUOBJ: {self.config_object} - MATNR: {self.material.material_number if self.material else 'None'}"


class ClassificationValue(models.Model): #AUSP

# Função: Armazena os valores atribuídos a um objeto classificado.
# Campos-chave: OBJEK, ATINN, ATWRT.
# Uso: Exemplo: para o material MAT001, o valor da característica “Peso” é “10kg”.

    client = models.CharField(max_length=3)  # MANDT
    object_key = models.CharField(max_length=50)  # OBJEK
    characteristic = models.ForeignKey(
        'Characteristic',
        on_delete=models.CASCADE,
        db_column='characteristic_id',
        to_field='internal_characteristic',
        related_name='classification_values', 
    )
    value_counter = models.CharField(max_length=3)  # ATZHL
    object_class_indicator = models.CharField(max_length=1)  # MAFID
    class_type = models.CharField(max_length=3)  # KLART
    archive_counter = models.CharField(max_length=4)  # ADZHL
    characteristic_value = models.CharField(max_length=30, unique = True)  # ATWRT

    class Meta:
        db_table = 'classification_value'
        verbose_name = 'Classification Value'
        verbose_name_plural = 'Classification Values'

    def __str__(self):
        return f"{self.object_key} | {self.characteristic} = {self.characteristic_value}"


class ClassCharacteristic(models.Model): #KSML

# Função: Liga uma classe às suas características.
# Campos-chave: CLINT, IMERK.
# Uso: Define quais características estão disponíveis para uma determinada classe.

    client = models.CharField(max_length=3)  # MANDT
    class_header = models.ForeignKey(
        'ClassHeader',
        on_delete=models.CASCADE,
        db_column='class_internal_id',
        to_field='internal_class_number',
        related_name='class_characteristics',
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


class CharacteristicValueText(models.Model): #CAWNT

# Função: Descrição dos valores de características por idioma.
# Campos-chave: ATINN, ATZHL, SPRAS.
# Uso: Armazena o texto legível de ATWRT em diferentes idiomas (como "Red" para "ROT").

    client = models.CharField(max_length=3)  # MANDT
    characteristic_value = models.ForeignKey(
        'CharacteristicValue',
        on_delete=models.CASCADE,
        # db_column='characteristic_id',
        # to_field='internal_characteristic',
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


class ClassCharacteristicSettings(models.Model): #KSSL
    class_header = models.ForeignKey(
        'ClassHeader',  # da KLAH
        on_delete=models.CASCADE,
        related_name='characteristic_settings'
    )
    characteristic = models.ForeignKey(
        'Characteristic',  # da CABN
        on_delete=models.CASCADE,
        related_name='class_settings'
    )
    is_required = models.BooleanField(default=False, help_text="Se marcado, a característica é obrigatória nesta classe.")
    allow_multiple = models.BooleanField(default=False, help_text="Se marcado, permite múltiplos valores para essa característica na classe.")
    only_predefined_values = models.BooleanField(default=False, help_text="Se marcado, restringe aos valores cadastrados (CAWN).")
    default_value = models.CharField(max_length=30, blank=True, null=True, help_text="Valor padrão sugerido na classe.")

    class Meta:
        db_table = 'class_characteristic_settings'
        unique_together = ('class_header', 'characteristic')
        verbose_name = 'Class Characteristic Setting'
        verbose_name_plural = 'Class Characteristic Settings'

    def __str__(self):
        return f"{self.class_header.class_number} - {self.characteristic.name}"