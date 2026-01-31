from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(unsafe_hash=True, kw_only=True)
class Companies:
    class Meta:
        name = "companies"

    company: list[Companies.Company] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Company:
        isin: str = field(
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        conid: None | str = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        symbol: str = field(
            metadata={
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
        tax_number: str = field(
            metadata={
                "name": "taxNumber",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        address: str = field(
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        country: str = field(
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
