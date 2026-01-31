from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from xsdata.models.datatype import XmlDate

from ib_edavki.generated.edp_common_1 import (
    AttachmentList,
    Header,
    Signatures,
)

__NAMESPACE__ = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"


@dataclass(unsafe_hash=True, kw_only=True)
class CorpData:
    """
    Parameters
    ----------
    id
        id
    trade_id
        Naziv družbe ali ISIN koda, trgovalna koda ali naziv delnice
    sold_date
        Datum odsvojitve delnic ali deležev družbe
    corp_amount
        Količina pridobljenih delnic
    corp_share
        % pridobljenega deleža
    corp_sold_amount
        Količina odsvojenih delnic
    corp_sold_share
        % odsvojenega deleža
    nominal_total_value
        Nominalna vrednost celotnega osnovnega kapitala v družbi
    sum
        Znesek (SUM(Nabavna vrednost odsvojenih delnic oz. deleža) -
        SUM(Znesek (bruto) izplačane vrednosti delnic oz. deležev))
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

    id: None | int = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
        },
    )
    trade_id: None | str = field(
        default=None,
        metadata={
            "name": "TradeId",
            "type": "Element",
        },
    )
    sold_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "SoldDate",
            "type": "Element",
        },
    )
    corp_amount: None | Decimal = field(
        default=None,
        metadata={
            "name": "CorpAmount",
            "type": "Element",
        },
    )
    corp_share: None | Decimal = field(
        default=None,
        metadata={
            "name": "CorpShare",
            "type": "Element",
        },
    )
    corp_sold_amount: None | Decimal = field(
        default=None,
        metadata={
            "name": "CorpSoldAmount",
            "type": "Element",
        },
    )
    corp_sold_share: None | Decimal = field(
        default=None,
        metadata={
            "name": "CorpSoldShare",
            "type": "Element",
        },
    )
    nominal_total_value: None | Decimal = field(
        default=None,
        metadata={
            "name": "NominalTotalValue",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    sum: None | Decimal = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "fraction_digits": 2,
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class CorpDataDetail:
    """
    Parameters
    ----------
    id
        CorpData id
    purch_date
        Datum pridobitve
    purch_type
        Način pridobitve
    purch_amount
        Količina pridobljenih delnic
    purch_share
        % pridobljenega deleža
    value_of_purchased
        Vrednost pridobljenih delnic ali deleža družbe
    value_at_purchase
        Nabavna vrednost ob pridobitvi
    sold_amount
        Količina odsvojenih delnic
    sold_share
        % odsvojenega deleža
    sold_value
        Vrednost odsvojenih delnic ali deleža
    sold_shares_value_at_purchase
        Nabavna vrednost odsvojenih delnic oz. deleža
    gross_sold_value
        Bruto izplačana vrednost delnic oz. deleža
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

    id: None | int = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
        },
    )
    purch_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "PurchDate",
            "type": "Element",
        },
    )
    purch_type: None | str = field(
        default=None,
        metadata={
            "name": "PurchType",
            "type": "Element",
        },
    )
    purch_amount: None | Decimal = field(
        default=None,
        metadata={
            "name": "PurchAmount",
            "type": "Element",
        },
    )
    purch_share: None | Decimal = field(
        default=None,
        metadata={
            "name": "PurchShare",
            "type": "Element",
        },
    )
    value_of_purchased: None | Decimal = field(
        default=None,
        metadata={
            "name": "ValueOfPurchased",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    value_at_purchase: None | Decimal = field(
        default=None,
        metadata={
            "name": "ValueAtPurchase",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    sold_amount: None | Decimal = field(
        default=None,
        metadata={
            "name": "SoldAmount",
            "type": "Element",
        },
    )
    sold_share: None | Decimal = field(
        default=None,
        metadata={
            "name": "SoldShare",
            "type": "Element",
        },
    )
    sold_value: None | Decimal = field(
        default=None,
        metadata={
            "name": "SoldValue",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    sold_shares_value_at_purchase: None | Decimal = field(
        default=None,
        metadata={
            "name": "SoldSharesValueAtPurchase",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    gross_sold_value: None | Decimal = field(
        default=None,
        metadata={
            "name": "GrossSoldValue",
            "type": "Element",
            "fraction_digits": 2,
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class Dividend:
    """
    Parameters
    ----------
    date
        Datum prejema dividend
    payer_tax_number
        Davčna številka izplačevalca dividend
    payer_identification_number
        Identifikacijska številka izplačevalca dividend
    payer_name
        Naziv izplačevalca dividend
    payer_address
        Naslov izplačevalca dividend
    payer_country
        Država izplačevalca dividend
    type_value
        Vrsta dividende
    value
        Znesek dividend (v EUR)
    foreign_tax
        Tuji davek (v EUR)
    source_country
        Država vira
    relief_statement
        Uveljavljam oprostitev po mednarodni pogodbi
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

    date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
        },
    )
    payer_tax_number: None | str = field(
        default=None,
        metadata={
            "name": "PayerTaxNumber",
            "type": "Element",
        },
    )
    payer_identification_number: None | str = field(
        default=None,
        metadata={
            "name": "PayerIdentificationNumber",
            "type": "Element",
        },
    )
    payer_name: None | str = field(
        default=None,
        metadata={
            "name": "PayerName",
            "type": "Element",
        },
    )
    payer_address: None | str = field(
        default=None,
        metadata={
            "name": "PayerAddress",
            "type": "Element",
        },
    )
    payer_country: None | str = field(
        default=None,
        metadata={
            "name": "PayerCountry",
            "type": "Element",
        },
    )
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
        },
    )
    value: None | Decimal = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    foreign_tax: None | Decimal = field(
        default=None,
        metadata={
            "name": "ForeignTax",
            "type": "Element",
            "fraction_digits": 2,
        },
    )
    source_country: None | str = field(
        default=None,
        metadata={
            "name": "SourceCountry",
            "type": "Element",
        },
    )
    relief_statement: None | str = field(
        default=None,
        metadata={
            "name": "ReliefStatement",
            "type": "Element",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class DohDiv:
    class Meta:
        name = "Doh_Div"
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

    period: None | str = field(
        default=None,
        metadata={
            "name": "Period",
            "type": "Element",
        },
    )
    email_address: None | str = field(
        default=None,
        metadata={
            "name": "EmailAddress",
            "type": "Element",
        },
    )
    phone_number: None | str = field(
        default=None,
        metadata={
            "name": "PhoneNumber",
            "type": "Element",
        },
    )
    resident_country: None | str = field(
        default=None,
        metadata={
            "name": "ResidentCountry",
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
    locked: None | bool = field(
        default=None,
        metadata={
            "name": "Locked",
            "type": "Element",
        },
    )
    self_report: None | bool = field(
        default=None,
        metadata={
            "name": "SelfReport",
            "type": "Element",
        },
    )
    wf_type_u: None | bool = field(
        default=None,
        metadata={
            "name": "WfTypeU",
            "type": "Element",
        },
    )
    notes: None | str = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class SubseqSubmissDecision:
    """
    Parameters
    ----------
    decision_id
        Številka sklepa
    decision_date
        Datum izdaje sklepa
    submission_deadline
        Rok za predložitev, določen v sklepu
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

    decision_id: None | str = field(
        default=None,
        metadata={
            "name": "DecisionId",
            "type": "Element",
        },
    )
    decision_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "DecisionDate",
            "type": "Element",
        },
    )
    submission_deadline: None | XmlDate = field(
        default=None,
        metadata={
            "name": "SubmissionDeadline",
            "type": "Element",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class SubseqSubmissProposal:
    """
    Parameters
    ----------
    proposal_submitted
        Vloga za podaljšanje roka - že vložena
    start_date
        Datum prenehanja razlogov za zamudo roka
    proposal_deadline
        Rok za naknadno predložitev
    delay_reasons
        Navedba opravičljivih razlogov za zamudo roka
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

    proposal_submitted: None | bool = field(
        default=None,
        metadata={
            "name": "ProposalSubmitted",
            "type": "Element",
        },
    )
    start_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
        },
    )
    proposal_deadline: None | XmlDate = field(
        default=None,
        metadata={
            "name": "ProposalDeadline",
            "type": "Element",
        },
    )
    delay_reasons: None | str = field(
        default=None,
        metadata={
            "name": "DelayReasons",
            "type": "Element",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class Envelope:
    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"

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
        doh_div: DohDiv = field(
            metadata={
                "name": "Doh_Div",
                "type": "Element",
                "required": True,
            }
        )
        dividend: list[Dividend] = field(
            default_factory=list,
            metadata={
                "name": "Dividend",
                "type": "Element",
            },
        )
        corp_data: list[CorpData] = field(
            default_factory=list,
            metadata={
                "name": "CorpData",
                "type": "Element",
            },
        )
        corp_data_detail: list[CorpDataDetail] = field(
            default_factory=list,
            metadata={
                "name": "CorpDataDetail",
                "type": "Element",
            },
        )
        subseq_submiss_decision: None | SubseqSubmissDecision = field(
            default=None,
            metadata={
                "name": "SubseqSubmissDecision",
                "type": "Element",
            },
        )
        subseq_submiss_proposal: None | SubseqSubmissProposal = field(
            default=None,
            metadata={
                "name": "SubseqSubmissProposal",
                "type": "Element",
            },
        )
