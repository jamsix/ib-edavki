from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(unsafe_hash=True, kw_only=True)
class Treaties:
    class Meta:
        name = "treaties"

    relief_statement: list[Treaties.ReliefStatement] = field(
        default_factory=list,
        metadata={
            "name": "reliefStatement",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class ReliefStatement:
        country: str = field(
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        statement: str = field(
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
