from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate

from ib_edavki.generated.edp_common_1 import (
    AttachmentList,
    BodyContent,
    Header,
    Signatures,
)

__NAMESPACE__ = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"


@dataclass(unsafe_hash=True, kw_only=True)
class AttachmentHash:
    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    hash: None | str = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
        },
    )


class TypeGainType(Enum):
    """
    Properties
    ----------
    A
        vložek kapitala
    B
        nakup
    C
        povečanje kapitala družbe z lastnimi sredstvi zavezanca
    D
        povečanje kapitala družbe iz sredstev družbe
    E
        zamenjava kapitala ob statusnih spremembah družbe
    F
        dedovanje
    G
        darilo
    H
        drugo
    I
        povečanje kapitalskega deleža v osebni družbi zaradi pripisa dobička
        kapitalskemu deležu
    J
        pridobitev kapita​la v inovativnih zagonskih podjetjih
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"


class TypeInventory(Enum):
    """
    Properties
    ----------
    PLVP
        Popisni list vrednostnega papirja oziroma invecticijskega kupona
    PLVPSHORT
        Popisni list vrednostnega papirja oziroma invecticijskega kupona
        SHORT
    PLVPGB
        Popisni list vrednostnega papirja, ki je v gospodarjenju pri
        borznoposredniški družbi na podlagi pogodbe o gospodarjenju
    PLVPGBSHORT
        Popisni list vrednostnega papirja, ki je v gospodarjenju pri
        borznoposredniški družbi na podlagi pogodbe o gospodarjenju SHORT
    PLD
        Popisni list deleža v gospodarskih družbah, zadrugah in drugih
        oblikah organiziranja
    PLVPZOK
        Popisni list vrednostnega papirja za primer zmanjšanja osnovnega
        kapitala ob nespremenjeni količini vrednostnega papirja
    """

    PLVP = "PLVP"
    PLVPSHORT = "PLVPSHORT"
    PLVPGB = "PLVPGB"
    PLVPGBSHORT = "PLVPGBSHORT"
    PLD = "PLD"
    PLVPZOK = "PLVPZOK"


@dataclass(unsafe_hash=True, kw_only=True)
class Securities:
    """
    Popisni list vrednostnega papirja oziroma investicijskega kupona.

    Parameters
    ----------
    isin
        ISIN vrednostnega papirja
    code
        Oznaka vrednostnega papirja
    name
        Naziv vrednostnega papirja
    is_fond
        Indikator ali je vrednostni papir sklad. Če je sklad potem je
        vrednost 'true', drugače je 'false'.
    resolution
        Opravilna številka sklepa skupščine
    resolution_date
        Datum sklepa skupščine
    row
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "max_length": 12,
        },
    )
    code: None | str = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "max_length": 10,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 100,
        },
    )
    is_fond: bool = field(
        default=False,
        metadata={
            "name": "IsFond",
            "type": "Element",
            "required": True,
        },
    )
    resolution: None | str = field(
        default=None,
        metadata={
            "name": "Resolution",
            "type": "Element",
            "max_length": 100,
        },
    )
    resolution_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ResolutionDate",
            "type": "Element",
        },
    )
    row: list[Securities.Row] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Row:
        """
        Parameters
        ----------
        id
            Zap. št.
        purchase
            Pridobitev
        sale
            Odsvojitev
        f8
            Zaloga v.p.
        """

        id: int = field(
            metadata={
                "name": "ID",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            }
        )
        purchase: None | Securities.Row.Purchase = field(
            default=None,
            metadata={
                "name": "Purchase",
                "type": "Element",
            },
        )
        sale: None | Securities.Row.Sale = field(
            default=None,
            metadata={
                "name": "Sale",
                "type": "Element",
            },
        )
        f8: None | str = field(
            default=None,
            metadata={
                "name": "F8",
                "type": "Element",
                "pattern": r"[-]?\d{1,12}(\.\d{1,8})?",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Purchase:
            """
            Parameters
            ----------
            f1
                Datum pridobitve
            f2
                Način pridobitve
            f3
                Količina
            f4
                Nabavna vrednost ob pridobitvi (na enoto)
            f5
                Plačan davek na dediščine in darila
            f11
                Zmanjšana nabavna vrednost vrednostnega papirja (na enoto)
                zaradi zmanjšanja osnovnega kapitala ob nespremenjeni
                količini
            """

            f1: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F1",
                    "type": "Element",
                },
            )
            f2: None | TypeGainType = field(
                default=None,
                metadata={
                    "name": "F2",
                    "type": "Element",
                },
            )
            f3: None | str = field(
                default=None,
                metadata={
                    "name": "F3",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f4: None | str = field(
                default=None,
                metadata={
                    "name": "F4",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f5: None | str = field(
                default=None,
                metadata={
                    "name": "F5",
                    "type": "Element",
                    "pattern": r"\d{1,10}(\.\d{1,4})?",
                },
            )
            f11: None | str = field(
                default=None,
                metadata={
                    "name": "F11",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Sale:
            """
            Parameters
            ----------
            f6
                Datum odsvojitve
            f7
                Količina odsvojenega v.p.
            f9
                Vrednost ob odsvojitvi (na enoto)
            f10
                Pravilo iz drugega odstavka v povezavi s petim odstavkom
                97.člena ZDoh-2
            """

            f6: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F6",
                    "type": "Element",
                },
            )
            f7: None | str = field(
                default=None,
                metadata={
                    "name": "F7",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f9: None | str = field(
                default=None,
                metadata={
                    "name": "F9",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f10: None | bool = field(
                default=None,
                metadata={
                    "name": "F10",
                    "type": "Element",
                },
            )


@dataclass(unsafe_hash=True, kw_only=True)
class SecuritiesCapitalReduction:
    """
    Popisni list vrednostnega papirja za primer zmanjšanja osnovnega
    kapitala ob nespremenjeni količini vrednostnega papirja.

    Parameters
    ----------
    isin
        ISIN vrednostnega papirja
    code
        Oznaka vrednostnega papirja
    name
        Naziv vrednostnega papirja
    resolution
        Opravilna številka sklepa skupščine
    resolution_date
        Datum sklepa skupščine
    row
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "max_length": 12,
        },
    )
    code: None | str = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "max_length": 10,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 100,
        },
    )
    resolution: None | str = field(
        default=None,
        metadata={
            "name": "Resolution",
            "type": "Element",
            "max_length": 100,
        },
    )
    resolution_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ResolutionDate",
            "type": "Element",
        },
    )
    row: list[SecuritiesCapitalReduction.Row] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Row:
        """
        Parameters
        ----------
        id
            Zap. št.
        purchase
            Pridobitev
        sale
            Odsvojitev
        """

        id: int = field(
            metadata={
                "name": "ID",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            }
        )
        purchase: None | SecuritiesCapitalReduction.Row.Purchase = field(
            default=None,
            metadata={
                "name": "Purchase",
                "type": "Element",
            },
        )
        sale: None | SecuritiesCapitalReduction.Row.Sale = field(
            default=None,
            metadata={
                "name": "Sale",
                "type": "Element",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Purchase:
            """
            Parameters
            ----------
            f1
                Datum pridobitve
            f2
                Način pridobitve
            f3
                Količina
            f4
                Nabavna vrednost ob pridobitvi (na enoto)
            """

            f1: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F1",
                    "type": "Element",
                },
            )
            f2: None | TypeGainType = field(
                default=None,
                metadata={
                    "name": "F2",
                    "type": "Element",
                },
            )
            f3: None | str = field(
                default=None,
                metadata={
                    "name": "F3",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f4: None | str = field(
                default=None,
                metadata={
                    "name": "F4",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Sale:
            """
            Parameters
            ----------
            f5
                Datum odsvojitve
            f6
                % zmanjšanja osnovnega kapitala
            f7
                Izplačana vrednost na podlagi zmanjšanja osnovnega kapitala
            """

            f5: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F5",
                    "type": "Element",
                },
            )
            f6: None | str = field(
                default=None,
                metadata={
                    "name": "F6",
                    "type": "Element",
                    "min_inclusive": "0",
                    "max_inclusive": "100",
                    "pattern": r"\d{1,3}(\.\d{1,4})?",
                },
            )
            f7: None | str = field(
                default=None,
                metadata={
                    "name": "F7",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )


@dataclass(unsafe_hash=True, kw_only=True)
class SecuritiesShort:
    """
    Popisni list vrednostnega papirja oziroma investicijskega kupona (PLVP
    Short).

    Parameters
    ----------
    isin
        ISIN vrednostnega papirja
    code
        Oznaka vrednostnega papirja
    name
        Naziv vrednostnega papirja
    is_fond
        Indikator ali je vrednostni papir sklad. Če je sklad potem je
        vrednost 'true', drugače je 'false'.
    row
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "max_length": 12,
        },
    )
    code: None | str = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "max_length": 10,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 100,
        },
    )
    is_fond: bool = field(
        default=False,
        metadata={
            "name": "IsFond",
            "type": "Element",
            "required": True,
        },
    )
    row: list[SecuritiesShort.Row] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Row:
        """
        Parameters
        ----------
        id
            Zap. št.
        purchase
            Pridobitev
        sale
            Odsvojitev
        f8
            Zaloga v.p.
        """

        id: int = field(
            metadata={
                "name": "ID",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            }
        )
        purchase: None | SecuritiesShort.Row.Purchase = field(
            default=None,
            metadata={
                "name": "Purchase",
                "type": "Element",
            },
        )
        sale: None | SecuritiesShort.Row.Sale = field(
            default=None,
            metadata={
                "name": "Sale",
                "type": "Element",
            },
        )
        f8: None | str = field(
            default=None,
            metadata={
                "name": "F8",
                "type": "Element",
                "pattern": r"[-]?\d{1,12}(\.\d{1,8})?",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Purchase:
            """
            Parameters
            ----------
            f1
                Datum pridobitve
            f2
                Način pridobitve
            f3
                Količina
            f4
                Nabavna vrednost ob pridobitvi (na enoto)
            f5
                Plačan davek na dediščine in darila
            """

            f1: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F1",
                    "type": "Element",
                },
            )
            f2: None | TypeGainType = field(
                default=None,
                metadata={
                    "name": "F2",
                    "type": "Element",
                },
            )
            f3: None | str = field(
                default=None,
                metadata={
                    "name": "F3",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f4: None | str = field(
                default=None,
                metadata={
                    "name": "F4",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f5: None | str = field(
                default=None,
                metadata={
                    "name": "F5",
                    "type": "Element",
                    "pattern": r"\d{1,10}(\.\d{1,4})?",
                },
            )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Sale:
            """
            Parameters
            ----------
            f6
                Datum odsvojitve
            f7
                Količina odsvojenega v.p.
            f9
                Vrednost ob osvojitvi (na enoto)
            """

            f6: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F6",
                    "type": "Element",
                },
            )
            f7: None | str = field(
                default=None,
                metadata={
                    "name": "F7",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f9: None | str = field(
                default=None,
                metadata={
                    "name": "F9",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )


@dataclass(unsafe_hash=True, kw_only=True)
class SecuritiesWithContract:
    """
    Popisni list vrednostnega papirja, ki je v gospodarjenju pri BPH družbi
    na podlagi pogodbe o gospodarjenju.

    Parameters
    ----------
    isin
        ISIN vrednostnega papirja
    code
        Oznaka vrednostnega papirja
    name
        Naziv vrednostnega papirja
    is_fond
        Indikator ali je vrednostni papir sklad. Če je sklad potem je
        vrednost 'true', drugače je 'false'.
    stock_exchange_name
        Naziv borznoposredniške družba
    resolution
        Opravilna številka sklepa skupščine
    resolution_date
        Datum sklepa skupščine
    row
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "max_length": 12,
        },
    )
    code: None | str = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "max_length": 10,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 100,
        },
    )
    is_fond: bool = field(
        default=False,
        metadata={
            "name": "IsFond",
            "type": "Element",
            "required": True,
        },
    )
    stock_exchange_name: None | str = field(
        default=None,
        metadata={
            "name": "StockExchangeName",
            "type": "Element",
            "max_length": 30,
        },
    )
    resolution: None | str = field(
        default=None,
        metadata={
            "name": "Resolution",
            "type": "Element",
            "max_length": 100,
        },
    )
    resolution_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ResolutionDate",
            "type": "Element",
        },
    )
    row: list[SecuritiesWithContract.Row] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Row:
        """
        Parameters
        ----------
        id
            Zap. št.
        purchase
            Pridobitev
        sale
            Odsvojitev
        f8
            Zaloga v.p.
        """

        id: int = field(
            metadata={
                "name": "ID",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            }
        )
        purchase: None | SecuritiesWithContract.Row.Purchase = field(
            default=None,
            metadata={
                "name": "Purchase",
                "type": "Element",
            },
        )
        sale: None | SecuritiesWithContract.Row.Sale = field(
            default=None,
            metadata={
                "name": "Sale",
                "type": "Element",
            },
        )
        f8: None | str = field(
            default=None,
            metadata={
                "name": "F8",
                "type": "Element",
                "pattern": r"[-]?\d{1,12}(\.\d{1,8})?",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Purchase:
            """
            Parameters
            ----------
            f1
                Datum pridobitve
            f2
                Način pridobitve
            f3
                Količina
            f4
                Nabavna vrednost ob pridobitvi (na enoto)
            f5
                Plačan davek na dediščine in darila
            f11
                Zmanjšana nabavna vrednost vrednostnega papirja (na enoto)
                zaradi zmanjšanja osnovnega kapitala ob nespremenjeni
                količini
            """

            f1: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F1",
                    "type": "Element",
                },
            )
            f2: None | TypeGainType = field(
                default=None,
                metadata={
                    "name": "F2",
                    "type": "Element",
                },
            )
            f3: None | str = field(
                default=None,
                metadata={
                    "name": "F3",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f4: None | str = field(
                default=None,
                metadata={
                    "name": "F4",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f5: None | str = field(
                default=None,
                metadata={
                    "name": "F5",
                    "type": "Element",
                    "pattern": r"\d{1,10}(\.\d{1,4})?",
                },
            )
            f11: None | str = field(
                default=None,
                metadata={
                    "name": "F11",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Sale:
            """
            Parameters
            ----------
            f6
                Datum odsvojitve
            f7
                Količina odsvojenega v.p.
            f9
                Vrednost ob osvojitvi (na enoto)
            f10
                Pravilo iz drugega odstavka v povezavi s petim odstavkom
                97.člena ZDoh-2
            """

            f6: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F6",
                    "type": "Element",
                },
            )
            f7: None | str = field(
                default=None,
                metadata={
                    "name": "F7",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f9: None | str = field(
                default=None,
                metadata={
                    "name": "F9",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f10: None | bool = field(
                default=None,
                metadata={
                    "name": "F10",
                    "type": "Element",
                },
            )


@dataclass(unsafe_hash=True, kw_only=True)
class SecuritiesWithContractShort:
    """
    Popisni list vrednostnega papirja, ki je v gospodarjenju pri BPH družbi
    na podlagi pogodbe o gospodarjenju PLVPGB (Short).

    Parameters
    ----------
    isin
        ISIN vrednostnega papirja
    code
        Oznaka vrednostnega papirja
    name
        Naziv vrednostnega papirja
    is_fond
        Indikator ali je vrednostni papir sklad. Če je sklad potem je
        vrednost 'true', drugače je 'false'.
    stock_exchange_name
        Naziv borznoposredniške družba
    row
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    isin: None | str = field(
        default=None,
        metadata={
            "name": "ISIN",
            "type": "Element",
            "max_length": 12,
        },
    )
    code: None | str = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "max_length": 10,
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 100,
        },
    )
    is_fond: bool = field(
        default=False,
        metadata={
            "name": "IsFond",
            "type": "Element",
            "required": True,
        },
    )
    stock_exchange_name: None | str = field(
        default=None,
        metadata={
            "name": "StockExchangeName",
            "type": "Element",
            "max_length": 30,
        },
    )
    row: list[SecuritiesWithContractShort.Row] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Row:
        """
        Parameters
        ----------
        id
            Zap. št.
        purchase
            Pridobitev
        sale
            Odsvojitev
        f8
            Zaloga v.p.
        """

        id: int = field(
            metadata={
                "name": "ID",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            }
        )
        purchase: None | SecuritiesWithContractShort.Row.Purchase = field(
            default=None,
            metadata={
                "name": "Purchase",
                "type": "Element",
            },
        )
        sale: None | SecuritiesWithContractShort.Row.Sale = field(
            default=None,
            metadata={
                "name": "Sale",
                "type": "Element",
            },
        )
        f8: None | str = field(
            default=None,
            metadata={
                "name": "F8",
                "type": "Element",
                "pattern": r"[-]?\d{1,12}(\.\d{1,8})?",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Purchase:
            """
            Parameters
            ----------
            f1
                Datum pridobitve
            f2
                Način pridobitve
            f3
                Količina
            f4
                Nabavna vrednost ob pridobitvi (na enoto)
            f5
                Plačan davek na dediščine in darila
            """

            f1: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F1",
                    "type": "Element",
                },
            )
            f2: None | TypeGainType = field(
                default=None,
                metadata={
                    "name": "F2",
                    "type": "Element",
                },
            )
            f3: None | str = field(
                default=None,
                metadata={
                    "name": "F3",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f4: None | str = field(
                default=None,
                metadata={
                    "name": "F4",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f5: None | str = field(
                default=None,
                metadata={
                    "name": "F5",
                    "type": "Element",
                    "pattern": r"\d{1,10}(\.\d{1,4})?",
                },
            )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Sale:
            """
            Parameters
            ----------
            f6
                Datum odsvojitve
            f7
                Količina odsvojenega v.p.
            f9
                Vrednost ob osvojitvi (na enoto)
            """

            f6: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F6",
                    "type": "Element",
                },
            )
            f7: None | str = field(
                default=None,
                metadata={
                    "name": "F7",
                    "type": "Element",
                    "pattern": r"\d{1,12}(\.\d{1,8})?",
                },
            )
            f9: None | str = field(
                default=None,
                metadata={
                    "name": "F9",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )


@dataclass(unsafe_hash=True, kw_only=True)
class Shares:
    """
    Popisni list deleža v gospodarskih družbah, zadrugah in drugih oblikah
    organiziranja.

    Parameters
    ----------
    name
        Ime deleža
    foreign_company
        Tuja družba
    divestment_tax_number
        Davčna številka odsvojene družbe
    subsequent_payments
        Uveljavljanje naknadnih vplačil v skladu s 4. točko sedmega odstavka
        98. člena Zdoh-2
    subsequent_payment_row
    row
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "max_length": 100,
        },
    )
    foreign_company: None | bool = field(
        default=None,
        metadata={
            "name": "ForeignCompany",
            "type": "Element",
        },
    )
    divestment_tax_number: None | str = field(
        default=None,
        metadata={
            "name": "DivestmentTaxNumber",
            "type": "Element",
            "pattern": r"[0-9]{8}",
        },
    )
    subsequent_payments: None | bool = field(
        default=None,
        metadata={
            "name": "SubsequentPayments",
            "type": "Element",
        },
    )
    subsequent_payment_row: list[Shares.SubsequentPaymentRow] = field(
        default_factory=list,
        metadata={
            "name": "SubsequentPaymentRow",
            "type": "Element",
        },
    )
    row: list[Shares.Row] = field(
        default_factory=list,
        metadata={
            "name": "Row",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class SubsequentPaymentRow:
        """
        Parameters
        ----------
        payment_tax_number
            Davčna številka družbe
        payment_date
            Datum naknadnega vplačila
        payment_amount
            Znesek
        """

        payment_tax_number: None | str = field(
            default=None,
            metadata={
                "name": "PaymentTaxNumber",
                "type": "Element",
                "pattern": r"[0-9]{8}",
            },
        )
        payment_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "PaymentDate",
                "type": "Element",
            },
        )
        payment_amount: None | str = field(
            default=None,
            metadata={
                "name": "PaymentAmount",
                "type": "Element",
                "pattern": r"\d{1,10}(\.\d{1,4})?",
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Row:
        """
        Parameters
        ----------
        id
            Zap. št.
        purchase
            Pridobitev
        sale
            Odsvojitev
        f7
            Stanje deleža
        """

        id: int = field(
            metadata={
                "name": "ID",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            }
        )
        purchase: None | Shares.Row.Purchase = field(
            default=None,
            metadata={
                "name": "Purchase",
                "type": "Element",
            },
        )
        sale: None | Shares.Row.Sale = field(
            default=None,
            metadata={
                "name": "Sale",
                "type": "Element",
            },
        )
        f7: None | str = field(
            default=None,
            metadata={
                "name": "F7",
                "type": "Element",
                "pattern": r"\d{1,14}(\.\d{1,8})?",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Purchase:
            """
            Parameters
            ----------
            f1
                Datum pridobitve
            f2
                Način pridobitve
            f3
                Nabavna vrednost ob pridobitvi
            f4
                Plačan davek na dediščine in darila
            """

            f1: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F1",
                    "type": "Element",
                },
            )
            f2: None | TypeGainType = field(
                default=None,
                metadata={
                    "name": "F2",
                    "type": "Element",
                },
            )
            f3: None | str = field(
                default=None,
                metadata={
                    "name": "F3",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f4: None | str = field(
                default=None,
                metadata={
                    "name": "F4",
                    "type": "Element",
                    "pattern": r"\d{1,10}(\.\d{1,4})?",
                },
            )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Sale:
            """
            Parameters
            ----------
            f5
                Datum odsvojitve
            f6
                % odsvojenega deleža
            f8
                Vrednost ob odsvojitvi
            f9
                Pravilo iz drugega odstavka v povezavi s petim odstavkom
                97.člena ZDoh-2
            """

            f5: None | XmlDate = field(
                default=None,
                metadata={
                    "name": "F5",
                    "type": "Element",
                },
            )
            f6: None | str = field(
                default=None,
                metadata={
                    "name": "F6",
                    "type": "Element",
                    "min_inclusive": "0",
                    "max_inclusive": "100",
                    "pattern": r"\d{1,3}(\.\d{1,4})?",
                },
            )
            f8: None | str = field(
                default=None,
                metadata={
                    "name": "F8",
                    "type": "Element",
                    "pattern": r"\d{1,14}(\.\d{1,8})?",
                },
            )
            f9: None | bool = field(
                default=None,
                metadata={
                    "name": "F9",
                    "type": "Element",
                },
            )


@dataclass(unsafe_hash=True, kw_only=True)
class DohKdvp:
    """
    Parameters
    ----------
    kdvp
    tax_relief
        Znižanje pozitivne davčne osnove za izgubo, doseženo pri odsvojitvi
        nepremičnin
    tax_base_decrease
        Znižanje pozitivne davčne osnove za preneseno izgubo (tretji
        odstavek 97. člena ZDoh-2)
    attachment
        Priloge
    kdvpitem
    """

    class Meta:
        name = "Doh_KDVP"
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    kdvp: DohKdvp.Kdvp = field(
        metadata={
            "name": "KDVP",
            "type": "Element",
            "required": True,
        }
    )
    tax_relief: list[DohKdvp.TaxRelief] = field(
        default_factory=list,
        metadata={
            "name": "TaxRelief",
            "type": "Element",
        },
    )
    tax_base_decrease: list[DohKdvp.TaxBaseDecrease] = field(
        default_factory=list,
        metadata={
            "name": "TaxBaseDecrease",
            "type": "Element",
        },
    )
    attachment: list[DohKdvp.Attachment] = field(
        default_factory=list,
        metadata={
            "name": "Attachment",
            "type": "Element",
        },
    )
    kdvpitem: list[DohKdvp.Kdvpitem] = field(
        default_factory=list,
        metadata={
            "name": "KDVPItem",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Kdvp:
        """
        Parameters
        ----------
        document_workflow_id
            Vrsta dokumenta - šifra
        document_workflow_name
            Vrsta dokumenta - naziv
        year
            Leto napovedi
        period_start
            Začetek obdobja napovedi (znotraj leta zgoraj)
        period_end
            Konec obdobja napovedi (znotraj leta zgoraj)
        is_resident
            Zavezanec je rezident Republike Slovenije
        country_of_residence_id
            Koda države rezidentstva
        country_of_residence_name
            Naziv države rezidentstva
        telephone_number
            Telefonska številka
        security_count
            Število popisnih listov vredostnega papirja
        security_short_count
            Število popisnih listov vredostnega papirja na kratko
        security_with_contract_count
            Število popisnih listov vrednostnega papirja, ki je v BPH na
            podlagi pogodbe o gospodarjenju
        security_with_contract_short_count
            Število popisnih listov vrednostnega papirja, ki je v BPH na
            podlagi pogodbe o gospodarjenju
        share_count
            Število popisnih listov deleža v gospodarskih družbah, zadrugah
            in drugih oblikah organiziranja
        security_capital_reduction_count
            Število popisnih listov vrednostnega papirja za primer
            zmanjšanja osnovnega kapitala ob nespremenjeni količini
            vrednostnega papirja
        remission_state
            Oprostitev plačila dohodnine ...: odstavek
        remission_article
            Oprostitev plačila dohodnine ...: člen
        res_confirmation_institution
            Oprostitev plačila dohodnine ...: pristojni organ potrdila o
            rezidentstvu
        res_confirmation_date
            Oprostitev plačila dohodnine ...: datum potrdila o rezidentstvu
        email
            Telefonska številka
        """

        document_workflow_id: None | str = field(
            default=None,
            metadata={
                "name": "DocumentWorkflowID",
                "type": "Element",
                "max_length": 1,
            },
        )
        document_workflow_name: None | str = field(
            default=None,
            metadata={
                "name": "DocumentWorkflowName",
                "type": "Element",
            },
        )
        year: None | str = field(
            default=None,
            metadata={
                "name": "Year",
                "type": "Element",
                "pattern": r"[1-9][0-9]{3}",
            },
        )
        period_start: None | XmlDate = field(
            default=None,
            metadata={
                "name": "PeriodStart",
                "type": "Element",
            },
        )
        period_end: None | XmlDate = field(
            default=None,
            metadata={
                "name": "PeriodEnd",
                "type": "Element",
            },
        )
        is_resident: None | bool = field(
            default=None,
            metadata={
                "name": "IsResident",
                "type": "Element",
            },
        )
        country_of_residence_id: None | str = field(
            default=None,
            metadata={
                "name": "CountryOfResidenceID",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            },
        )
        country_of_residence_name: None | str = field(
            default=None,
            metadata={
                "name": "CountryOfResidenceName",
                "type": "Element",
                "max_length": 40,
            },
        )
        telephone_number: None | str = field(
            default=None,
            metadata={
                "name": "TelephoneNumber",
                "type": "Element",
            },
        )
        security_count: int = field(
            default=0,
            metadata={
                "name": "SecurityCount",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            },
        )
        security_short_count: int = field(
            default=0,
            metadata={
                "name": "SecurityShortCount",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            },
        )
        security_with_contract_count: int = field(
            default=0,
            metadata={
                "name": "SecurityWithContractCount",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            },
        )
        security_with_contract_short_count: int = field(
            default=0,
            metadata={
                "name": "SecurityWithContractShortCount",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            },
        )
        share_count: int = field(
            default=0,
            metadata={
                "name": "ShareCount",
                "type": "Element",
                "required": True,
                "min_inclusive": 0,
            },
        )
        security_capital_reduction_count: None | int = field(
            default=None,
            metadata={
                "name": "SecurityCapitalReductionCount",
                "type": "Element",
                "min_inclusive": 0,
            },
        )
        remission_state: None | str = field(
            default=None,
            metadata={
                "name": "RemissionState",
                "type": "Element",
                "max_length": 4,
            },
        )
        remission_article: None | str = field(
            default=None,
            metadata={
                "name": "RemissionArticle",
                "type": "Element",
                "max_length": 4,
            },
        )
        res_confirmation_institution: None | str = field(
            default=None,
            metadata={
                "name": "ResConfirmationInstitution",
                "type": "Element",
                "max_length": 100,
            },
        )
        res_confirmation_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "ResConfirmationDate",
                "type": "Element",
            },
        )
        email: None | str = field(
            default=None,
            metadata={
                "name": "Email",
                "type": "Element",
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class TaxRelief:
        """
        Parameters
        ----------
        order_number
            Številka odločbe
        order_date
            Datum odločbe
        acquirement_date
            Datum pridobitve
        expropriation_date
            Datum odsvojitve
        loss
            Izguba (v EUR s centi)
        profit
            Dobiček (v EUR s centi)
        income_tax
            Odmerjena dohodnina (v EUR s centi)
        is_prefilled
            Predizpolnjeno polje
        """

        order_number: None | str = field(
            default=None,
            metadata={
                "name": "OrderNumber",
                "type": "Element",
                "max_length": 50,
            },
        )
        order_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "OrderDate",
                "type": "Element",
            },
        )
        acquirement_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "AcquirementDate",
                "type": "Element",
            },
        )
        expropriation_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "ExpropriationDate",
                "type": "Element",
            },
        )
        loss: None | str = field(
            default=None,
            metadata={
                "name": "Loss",
                "type": "Element",
                "pattern": r"\d{1,12}(\.\d{1,2})?",
            },
        )
        profit: None | str = field(
            default=None,
            metadata={
                "name": "Profit",
                "type": "Element",
                "pattern": r"\d{1,12}(\.\d{1,2})?",
            },
        )
        income_tax: None | str = field(
            default=None,
            metadata={
                "name": "IncomeTax",
                "type": "Element",
                "pattern": r"\d{1,12}(\.\d{1,2})?",
            },
        )
        is_prefilled: None | bool = field(
            default=None,
            metadata={
                "name": "IsPrefilled",
                "type": "Element",
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class TaxBaseDecrease:
        """
        Parameters
        ----------
        order_number
            Številka odločbe
        order_date
            Datum odločbe
        tax_office_id
            Šifra davčnega urada
        tax_office_name
            Naziv davčnega urada
        loss
            Izguba (v EUR s centi)
        """

        order_number: None | str = field(
            default=None,
            metadata={
                "name": "OrderNumber",
                "type": "Element",
                "max_length": 50,
            },
        )
        order_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "OrderDate",
                "type": "Element",
            },
        )
        tax_office_id: None | str = field(
            default=None,
            metadata={
                "name": "TaxOfficeID",
                "type": "Element",
                "pattern": r"[0-9]{2}",
            },
        )
        tax_office_name: None | str = field(
            default=None,
            metadata={
                "name": "TaxOfficeName",
                "type": "Element",
                "max_length": 40,
            },
        )
        loss: None | str = field(
            default=None,
            metadata={
                "name": "Loss",
                "type": "Element",
                "pattern": r"\d{1,12}(\.\d{1,2})?",
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Attachment:
        document: None | str = field(
            default=None,
            metadata={
                "name": "Document",
                "type": "Element",
                "max_length": 70,
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Kdvpitem:
        """
        Parameters
        ----------
        item_id
            ID popisnega lista
        inventory_list_type
            Vrsta popisnega lista
        name
            Naziv popisnega lista
        has_foreign_tax
            Davek plačan v tujini
        foreign_tax
            Tuji davek (v EUR s centi)
        ftcountry_id
            Koda države v kateri je plačan tuji davek
        ftcountry_name
            Ime države v kateri je plačan tuji davek
        has_loss_transfer
            Prenos izgube po tretjem odstavku 97.člena ZDoh-2
        foreign_transfer
            Odsvojitev deleža, ki je bil v tujini pridobljen z zamenjavo
            deleža skladno z Direktivo 90/434/EGS
        tax_decrease_conformance
            Uveljavljanje oprostitve po 5. točki drugega odstavka 96. člena
            ZDoh-2
        securities
        securities_short
        shares
        securities_with_contract
        securities_with_contract_short
        securities_capital_reduction
        """

        item_id: None | int = field(
            default=None,
            metadata={
                "name": "ItemID",
                "type": "Element",
                "min_inclusive": 0,
            },
        )
        inventory_list_type: TypeInventory = field(
            metadata={
                "name": "InventoryListType",
                "type": "Element",
                "required": True,
            }
        )
        name: None | str = field(
            default=None,
            metadata={
                "name": "Name",
                "type": "Element",
                "max_length": 100,
            },
        )
        has_foreign_tax: None | bool = field(
            default=None,
            metadata={
                "name": "HasForeignTax",
                "type": "Element",
            },
        )
        foreign_tax: None | str = field(
            default=None,
            metadata={
                "name": "ForeignTax",
                "type": "Element",
                "pattern": r"\d{1,10}(\.\d{1,4})?",
            },
        )
        ftcountry_id: None | str = field(
            default=None,
            metadata={
                "name": "FTCountryID",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            },
        )
        ftcountry_name: None | str = field(
            default=None,
            metadata={
                "name": "FTCountryName",
                "type": "Element",
                "max_length": 40,
            },
        )
        has_loss_transfer: None | bool = field(
            default=None,
            metadata={
                "name": "HasLossTransfer",
                "type": "Element",
            },
        )
        foreign_transfer: None | bool = field(
            default=None,
            metadata={
                "name": "ForeignTransfer",
                "type": "Element",
            },
        )
        tax_decrease_conformance: None | bool = field(
            default=None,
            metadata={
                "name": "TaxDecreaseConformance",
                "type": "Element",
                "nillable": True,
            },
        )
        securities: None | Securities = field(
            default=None,
            metadata={
                "name": "Securities",
                "type": "Element",
            },
        )
        securities_short: None | SecuritiesShort = field(
            default=None,
            metadata={
                "name": "SecuritiesShort",
                "type": "Element",
            },
        )
        shares: None | Shares = field(
            default=None,
            metadata={
                "name": "Shares",
                "type": "Element",
            },
        )
        securities_with_contract: None | SecuritiesWithContract = field(
            default=None,
            metadata={
                "name": "SecuritiesWithContract",
                "type": "Element",
            },
        )
        securities_with_contract_short: None | SecuritiesWithContractShort = (
            field(
                default=None,
                metadata={
                    "name": "SecuritiesWithContractShort",
                    "type": "Element",
                },
            )
        )
        securities_capital_reduction: None | SecuritiesCapitalReduction = (
            field(
                default=None,
                metadata={
                    "name": "SecuritiesCapitalReduction",
                    "type": "Element",
                },
            )
        )


@dataclass(unsafe_hash=True, kw_only=True)
class Envelope:
    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"

    header: Header = field(
        metadata={
            "name": "Header",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )
    attachment_list: None | AttachmentList = field(
        default=None,
        metadata={
            "name": "AttachmentList",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    signatures: Signatures = field(
        metadata={
            "name": "Signatures",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )
    body: Envelope.Body = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Body:
        body_content: BodyContent = field(
            metadata={
                "name": "bodyContent",
                "type": "Element",
                "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
                "required": True,
            }
        )
        doh_kdvp: DohKdvp = field(
            metadata={
                "name": "Doh_KDVP",
                "type": "Element",
                "required": True,
            }
        )
        attachment_hash: None | AttachmentHash = field(
            default=None,
            metadata={
                "name": "AttachmentHash",
                "type": "Element",
            },
        )
