from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(unsafe_hash=True, kw_only=True)
class Taxpayer:
    class Meta:
        name = "taxpayer"

    tax_number: str = field(
        metadata={
            "name": "taxNumber",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    taxpayer_type: str = field(
        metadata={
            "name": "taxpayerType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    address1: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    city: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    post_number: str = field(
        metadata={
            "name": "postNumber",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    post_name: str = field(
        metadata={
            "name": "postName",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    email: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    telephone_number: str = field(
        metadata={
            "name": "telephoneNumber",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    resident_country: str = field(
        metadata={
            "name": "residentCountry",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    is_resident: bool = field(
        metadata={
            "name": "isResident",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
