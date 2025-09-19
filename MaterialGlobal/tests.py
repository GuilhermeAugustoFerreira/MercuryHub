from django.test import TestCase

# Create your tests here.
from Classification.models import (
    ClassCharacteristic,
    ClassHeader,
    Characteristic,
    CharacteristicValue,
)
from Classification.services import create_material_with_classification
from MaterialGlobal.models import GlobalMaterial, MaterialDescription


class MaterialClassificationCreationTests(TestCase):
    """Integration tests for material creation with classification data."""

    CLIENT = "100"

    @classmethod
    def setUpTestData(cls):
        cls.class_definitions = {
            "DISJUNTOR_MERC": {
                "internal_class_number": "0000000001",
                "class_type": "001",
                "characteristics": {
                    "TIPO": ["Termomagnético", "Motor"],
                    "NUMERO POLOS": ["1P", "3P"],
                    "TENSAO NOMINAL": ["220V", "380V"],
                    "CAPACIDADE RUPTURA": ["6kA", "10kA"],
                    "CURVA DISPARO": ["B", "C"],
                    "CORRENTE NOMINAL": ["10A", "20A"],
                    "ACIONAMENTO": ["Manual", "Motorizado"],
                    "POSICAO COMANDO": ["Frontal", "Lateral"],
                    "CONTATO AUXILIAR": ["Sim", "Não"],
                    "TENSAO BOBINA ABERTURA": ["110V", "220V"],
                    "TENSAO BOBINA FECHAMENTO": ["110V", "220V"],
                    "NBI": ["6kV", "8kV"],
                    "NORMA": ["IEC 60947", "NBR NM 60898"],
                    "AJUSTE RELE": ["Fixo", "Regulável"],
                    "FIXACAO": ["Trilho DIN", "Painel"],
                    "DIMENSOES": ["45mm x 80mm x 70mm", "54mm x 90mm x 80mm"],
                    "DISTANCIA ENTRE POLOS": ["17.5mm", "27mm"],
                    "ACESSORIOS": ["Contato auxiliar", "Bobina shunt"],
                    "DADOS COMPLEMENTARES": ["Aplicação industrial", "Uso residencial"],
                    "FABRICANTE": ["Fabricante X", "Fabricante Y"],
                    "REFERENCIA": ["DISJ-001", "DISJ-002"],
                },
            },
            "PARAFUSO_MERC": {
                "internal_class_number": "0000000002",
                "class_type": "001",
                "characteristics": {
                    "TIPO": ["Allen", "Sextavado"],
                    "DISPOSITIVO APERTO": ["Chave Allen", "Chave Boca"],
                    "DIAMETRO": ["M6", "M8"],
                    "ROSCA": ["Métrica", "UNC"],
                    "COMPRIMENTO TOTAL": ["20mm", "40mm"],
                    "MATERIAL": ["Aço Carbono", "Inox"],
                    "TRATAMENTO SUPERFICIE": ["Zincado", "Fosfatizado"],
                    "DISPOSICAO ROSCA": ["Total", "Parcial"],
                    "COMPRIMENTO ROSCA": ["15mm", "35mm"],
                    "PASSO": ["1.0", "1.25"],
                    "NORMA": ["DIN 912", "DIN 933"],
                    "CLASSE RESISTENCIA": ["8.8", "10.9"],
                    "ACESSORIOS": ["Arruela Lisa", "Arruela Pressão"],
                    "DADOS COMPLEMENTARES": ["Uso geral", "Alta resistência"],
                    "FABRICANTE": ["Fabricante A", "Fabricante B"],
                    "REFERENCIA": ["PARA-001", "PARA-002"],
                },
            },
        }

        cls.class_headers = {}
        cls.characteristics = {}
        cls.reference_values = {}

        for class_name, data in cls.class_definitions.items():
            cls.class_headers[class_name] = ClassHeader.objects.create(
                client=cls.CLIENT,
                internal_class_number=data["internal_class_number"],
                class_type=data["class_type"],
                class_name=class_name,
                class_status="1",
                class_group="MERC",
                characteristics_table="CABN",
                usage_in_superior_classes="1",
                multiple_selection_allowed=False,
            )

            for characteristic_name, values in data["characteristics"].items():
                if characteristic_name not in cls.characteristics:
                    cls.characteristics[characteristic_name] = Characteristic.objects.create(
                        client=cls.CLIENT,
                        archive_counter="0000",
                        name=characteristic_name,
                        data_type="CHAR",
                        character_length=30,
                        case_sensitive=False,
                        entry_required=False,
                        single_value=True,
                        multilingual=False,
                        display_allowed_values="X",
                        display_assigned_values="X",
                    )

                cls.reference_values.setdefault(characteristic_name, set()).update(values)

        for characteristic_name, values in cls.reference_values.items():
            characteristic = cls.characteristics[characteristic_name]
            for counter, value in enumerate(sorted(values), start=1):
                CharacteristicValue.objects.create(
                    client=cls.CLIENT,
                    internal_characteristic=characteristic,
                    value_counter=f"{counter:04d}",
                    archive_counter="0000",
                    value=value,
                )

        for class_name, data in cls.class_definitions.items():
            class_header = cls.class_headers[class_name]
            for index, characteristic_name in enumerate(data["characteristics"], start=1):
                ClassCharacteristic.objects.create(
                    client=cls.CLIENT,
                    class_header=class_header,
                    item_number=f"{index:03d}",
                    archive_counter="0000",
                    characteristic=cls.characteristics[characteristic_name],
                    object_dependent_char="0",
                )

        cls.predefined_values = {
            "DISJUNTOR_MERC": {
                "TIPO": "Termomagnético",
                "NUMERO POLOS": "1P",
                "TENSAO NOMINAL": "220V",
                "CAPACIDADE RUPTURA": "6kA",
                "CURVA DISPARO": "B",
                "CORRENTE NOMINAL": "10A",
                "ACIONAMENTO": "Manual",
                "POSICAO COMANDO": "Frontal",
                "CONTATO AUXILIAR": "Sim",
                "TENSAO BOBINA ABERTURA": "110V",
                "TENSAO BOBINA FECHAMENTO": "110V",
                "NBI": "6kV",
                "NORMA": "IEC 60947",
                "AJUSTE RELE": "Fixo",
                "FIXACAO": "Trilho DIN",
                "DIMENSOES": "45mm x 80mm x 70mm",
                "DISTANCIA ENTRE POLOS": "17.5mm",
                "ACESSORIOS": "Contato auxiliar",
                "DADOS COMPLEMENTARES": "Aplicação industrial",
                "FABRICANTE": "Fabricante X",
                "REFERENCIA": "DISJ-001",
            },
            "PARAFUSO_MERC": {
                "TIPO": "Allen",
                "DISPOSITIVO APERTO": "Chave Allen",
                "DIAMETRO": "M6",
                "ROSCA": "Métrica",
                "COMPRIMENTO TOTAL": "20mm",
                "MATERIAL": "Aço Carbono",
                "TRATAMENTO SUPERFICIE": "Zincado",
                "DISPOSICAO ROSCA": "Total",
                "COMPRIMENTO ROSCA": "15mm",
                "PASSO": "1.0",
                "NORMA": "DIN 912",
                "CLASSE RESISTENCIA": "8.8",
                "ACESSORIOS": "Arruela Lisa",
                "DADOS COMPLEMENTARES": "Uso geral",
                "FABRICANTE": "Fabricante A",
                "REFERENCIA": "PARA-001",
            },
        }

        cls.new_values = {
            "DISJUNTOR_MERC": {
                "TIPO": "Residual",
                "NUMERO POLOS": "4P",
                "TENSAO NOMINAL": "440V",
                "CAPACIDADE RUPTURA": "15kA",
                "CURVA DISPARO": "D",
                "CORRENTE NOMINAL": "32A",
                "ACIONAMENTO": "Remoto",
                "POSICAO COMANDO": "Superior",
                "CONTATO AUXILIAR": "Opcional",
                "TENSAO BOBINA ABERTURA": "24V",
                "TENSAO BOBINA FECHAMENTO": "24V",
                "NBI": "12kV",
                "NORMA": "UL 489",
                "AJUSTE RELE": "Eletrônico",
                "FIXACAO": "Placa base",
                "DIMENSOES": "60mm x 100mm x 90mm",
                "DISTANCIA ENTRE POLOS": "45mm",
                "ACESSORIOS": "Bobina mínima tensão",
                "DADOS COMPLEMENTARES": "Inclui indicadores de estado",
                "FABRICANTE": "Fabricante Z",
                "REFERENCIA": "DISJ-900",
            },
            "PARAFUSO_MERC": {
                "TIPO": "Torx",
                "DISPOSITIVO APERTO": "Chave Torx",
                "DIAMETRO": "M10",
                "ROSCA": "BSP",
                "COMPRIMENTO TOTAL": "55mm",
                "MATERIAL": "Latão",
                "TRATAMENTO SUPERFICIE": "Galvanizado a fogo",
                "DISPOSICAO ROSCA": "Parcial longa",
                "COMPRIMENTO ROSCA": "50mm",
                "PASSO": "1.5",
                "NORMA": "ISO 14579",
                "CLASSE RESISTENCIA": "12.9",
                "ACESSORIOS": "Porca travante",
                "DADOS COMPLEMENTARES": "Fornecido com certificado",
                "FABRICANTE": "Fabricante C",
                "REFERENCIA": "PARA-900",
            },
        }

    def test_create_material_with_predefined_values(self):
        """First scenario: only reference values are used."""

        material_data = {
            "material_number": "MAT-PARA-001",
            "material_type": "ZPAR",
            "industry_sector": "M",
            "material_group": "000000001",
            "base_unit_of_measure": "UN",
        }

        description_data = {"language": "PT", "description": "Parafuso Allen zincado"}

        result = create_material_with_classification(
            material_data=material_data,
            description_data=description_data,
            class_name="PARAFUSO_MERC",
            classification_data=self.predefined_values["PARAFUSO_MERC"],
            client=self.CLIENT,
        )

        self.assertEqual(result.created_characteristic_values, {})

        material = GlobalMaterial.objects.get(material_number="MAT-PARA-001")
        self.assertEqual(material.material_type, "ZPAR")
        self.assertEqual(material.industry_sector, "M")

        description = MaterialDescription.objects.get(material=material, language="PT")
        self.assertEqual(description.description, "Parafuso Allen zincado")

        self.assertEqual(
            len(result.classification_entries),
            len(self.predefined_values["PARAFUSO_MERC"]),
        )

        for name in self.class_definitions["PARAFUSO_MERC"]["characteristics"].keys():
            count = CharacteristicValue.objects.filter(
                internal_characteristic=self.characteristics[name]
            ).count()
            expected = len(self.reference_values[name])
            self.assertEqual(
                count,
                expected,
                msg=f"Expected only the reference values for {name}",
            )

    def test_create_material_with_new_values(self):
        """Second scenario: new characteristic values are created on demand."""

        material_data = {
            "material_number": "MAT-DISJ-900",
            "material_type": "ZDIS",
            "industry_sector": "M",
            "material_group": "000000002",
            "base_unit_of_measure": "UN",
        }

        result = create_material_with_classification(
            material_data=material_data,
            description_data={"language": "PT", "description": "Disjuntor residual"},
            class_name="DISJUNTOR_MERC",
            classification_data=self.new_values["DISJUNTOR_MERC"],
            client=self.CLIENT,
        )

        created_values = result.created_characteristic_values
        self.assertEqual(
            set(created_values.keys()),
            set(self.new_values["DISJUNTOR_MERC"].keys()),
        )

        for key, value in self.new_values["DISJUNTOR_MERC"].items():
            self.assertIn(value, created_values[key])

        for name, values in created_values.items():
            characteristic = self.characteristics[name]
            self.assertTrue(
                CharacteristicValue.objects.filter(
                    internal_characteristic=characteristic,
                    value__in=values,
                ).exists()
            )

        material = GlobalMaterial.objects.get(material_number="MAT-DISJ-900")
        self.assertEqual(material.material_type, "ZDIS")

        description = MaterialDescription.objects.get(material=material, language="PT")
        self.assertEqual(description.description, "Disjuntor residual")