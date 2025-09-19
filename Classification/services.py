"""Utilities to support classification-aware material creation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from django.db import transaction

from MaterialGlobal.models import GlobalMaterial, MaterialDescription

from .models import (
    ClassificationValue,
    ClassHeader,
    Characteristic,
    CharacteristicValue,
    ObjectLink,
)


@dataclass(frozen=True)
class MaterialClassificationResult:
    """Result payload returned by :func:`create_material_with_classification`."""

    material: GlobalMaterial
    object_link: ObjectLink
    classification_entries: Tuple[ClassificationValue, ...]
    created_characteristic_values: Dict[str, Tuple[str, ...]]


def _ensure_characteristic_value(
    *,
    characteristic: Characteristic,
    value: str,
    client: str,
    archive_counter: str,
) -> Tuple[CharacteristicValue, bool]:
    """Return an existing :class:`CharacteristicValue` or create a new one."""

    existing = characteristic.values.filter(value=value).first()
    if existing:
        return existing, False

    next_counter = characteristic.values.count() + 1
    characteristic_value = CharacteristicValue.objects.create(
        client=client,
        internal_characteristic=characteristic,
        value_counter=f"{next_counter:04d}",
        archive_counter=archive_counter,
        value=value,
    )
    return characteristic_value, True


@transaction.atomic
def create_material_with_classification(
    *,
    material_data: Dict[str, str],
    description_data: Dict[str, str] | None,
    class_name: str,
    classification_data: Dict[str, str],
    client: str = "100",
    object_class_indicator: str = "M",
    archive_counter: str = "0000",
) -> MaterialClassificationResult:
    """Create or update a material and assign classification data."""

    if "material_number" not in material_data:
        raise ValueError("material_data must include 'material_number'")

    class_header = ClassHeader.objects.get(class_name=class_name)

    material_defaults = {
        key: value for key, value in material_data.items() if key != "material_number"
    }
    material, _ = GlobalMaterial.objects.update_or_create(
        material_number=material_data["material_number"], defaults=material_defaults
    )

    if description_data:
        MaterialDescription.objects.update_or_create(
            material=material,
            language=description_data["language"],
            defaults={"description": description_data["description"][:40]},
        )

    config_object = f"{material.material_number}-{class_header.internal_class_number}"
    object_link, _ = ObjectLink.objects.update_or_create(
        config_object=config_object,
        defaults={"client": client, "material": material},
    )

    created_values: Dict[str, List[str]] = {}
    classification_entries: List[ClassificationValue] = []

    for characteristic_name, value in classification_data.items():
        characteristic = Characteristic.objects.get(name=characteristic_name)
        characteristic_value, created = _ensure_characteristic_value(
            characteristic=characteristic,
            value=value,
            client=client,
            archive_counter=archive_counter,
        )
        if created:
            created_values.setdefault(characteristic_name, []).append(value)

        classification_value, _ = ClassificationValue.objects.update_or_create(
            client=client,
            object_key=object_link.config_object,
            characteristic=characteristic,
            defaults={
                "value_counter": characteristic_value.value_counter,
                "object_class_indicator": object_class_indicator,
                "class_type": class_header.class_type,
                "archive_counter": archive_counter,
                "characteristic_value": value,
            },
        )
        classification_entries.append(classification_value)

    return MaterialClassificationResult(
        material=material,
        object_link=object_link,
        classification_entries=tuple(classification_entries),
        created_characteristic_values=
        {
            key: tuple(values) for key, values in created_values.items()
        },
    )