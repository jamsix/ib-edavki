from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"


@dataclass(unsafe_hash=True, kw_only=True)
class AttachmentList:
    """
    Document attachments.
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    external_attachment: list[AttachmentList.ExternalAttachment] = field(
        default_factory=list,
        metadata={
            "name": "ExternalAttachment",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class ExternalAttachment:
        attachment_id: None | int = field(
            default=None,
            metadata={
                "name": "attachmentId",
                "type": "Element",
            },
        )
        type_value: None | str = field(
            default=None,
            metadata={
                "name": "type",
                "type": "Element",
            },
        )
        filename: str = field(
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        mimetype: str = field(
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        hash: AttachmentList.ExternalAttachment.Hash = field(
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        description: None | str = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )

        @dataclass(unsafe_hash=True, kw_only=True)
        class Hash:
            value: str = field(
                default="",
                metadata={
                    "required": True,
                },
            )
            type_value: str = field(
                metadata={
                    "name": "type",
                    "type": "Attribute",
                    "required": True,
                }
            )


@dataclass(unsafe_hash=True, kw_only=True)
class Ner:
    """
    Parameters
    ----------
    total_f8
        ...
    total_f9
        ...
    total_f10
        ...
    neritem
    """

    class Meta:
        name = "NER"
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    total_f8: None | str = field(
        default=None,
        metadata={
            "name": "Total_F8",
            "type": "Element",
            "pattern": r"\d{1,14}",
        },
    )
    total_f9: None | str = field(
        default=None,
        metadata={
            "name": "Total_F9",
            "type": "Element",
            "pattern": r"\d{1,14}",
        },
    )
    total_f10: None | str = field(
        default=None,
        metadata={
            "name": "Total_F10",
            "type": "Element",
            "pattern": r"\d{1,14}",
        },
    )
    neritem: list[Ner.Neritem] = field(
        default_factory=list,
        metadata={
            "name": "NERItem",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class Neritem:
        """
        Parameters
        ----------
        f1_name
            ...
        f2_address
            ...
        f3_resident_country
            ISO 2 letter country code
        f4_tax_number
            ...
        f5_birth_date
            ...
        f6_benefits
            ...
        f7_other_benefits
            ...
        f8
            ...
        f9
            ...
        f10
            ...
        """

        f1_name: None | str = field(
            default=None,
            metadata={
                "name": "F1_Name",
                "type": "Element",
            },
        )
        f2_address: None | str = field(
            default=None,
            metadata={
                "name": "F2_Address",
                "type": "Element",
            },
        )
        f3_resident_country: None | str = field(
            default=None,
            metadata={
                "name": "F3_ResidentCountry",
                "type": "Element",
            },
        )
        f4_tax_number: None | int = field(
            default=None,
            metadata={
                "name": "F4_TaxNumber",
                "type": "Element",
            },
        )
        f5_birth_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "F5_BirthDate",
                "type": "Element",
            },
        )
        f6_benefits: None | str = field(
            default=None,
            metadata={
                "name": "F6_Benefits",
                "type": "Element",
            },
        )
        f7_other_benefits: None | str = field(
            default=None,
            metadata={
                "name": "F7_OtherBenefits",
                "type": "Element",
            },
        )
        f8: None | str = field(
            default=None,
            metadata={
                "name": "F8",
                "type": "Element",
                "pattern": r"\d{1,14}",
            },
        )
        f9: None | str = field(
            default=None,
            metadata={
                "name": "F9",
                "type": "Element",
                "pattern": r"\d{1,14}",
            },
        )
        f10: None | str = field(
            default=None,
            metadata={
                "name": "F10",
                "type": "Element",
                "pattern": r"\d{1,14}",
            },
        )


@dataclass(unsafe_hash=True, kw_only=True)
class Tsasignature:
    """
    Parameters
    ----------
    w3_org_2000_09_xmldsig_element
        Place for ds:Signature element
    """

    class Meta:
        name = "TSASignature"
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    w3_org_2000_09_xmldsig_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class Transformation:
    """
    Instruct how to display xml document localfile - xslt transformation is
    stored localy on edavki url - xslt transformation is published on
    internet data - xslt transformation is included in here document xml.
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    localfile: None | str = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    url: None | str = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    data: None | str = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class BodyContent:
    class Meta:
        name = "bodyContent"
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class CustodianType:
    """
    Parameters
    ----------
    name
    address1
    address2
    city
    custodian_notes
        Custodian notes kadar oddaja skrbnik
    custodian_submit_date
        Datum oddaje custodiana
    """

    class Meta:
        name = "custodianType"

    name: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    address1: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    address2: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    city: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    custodian_notes: None | str = field(
        default=None,
        metadata={
            "name": "CustodianNotes",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    custodian_submit_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "CustodianSubmitDate",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class PresentationType:
    class Meta:
        name = "presentationType"

    schemas_hermes_softlab_com_2003_09_signatures_element: list[object] = (
        field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "urn:schemas-hermes-softlab-com:2003/09/Signatures",
                "max_occurs": 2,
            },
        )
    )


@dataclass(unsafe_hash=True, kw_only=True)
class ReceiptType:
    class Meta:
        name = "receiptType"

    timestamp: XmlDateTime = field(
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )
    document_number: str = field(
        metadata={
            "name": "documentNumber",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    meta_text1: None | str = field(
        default=None,
        metadata={
            "name": "metaText1",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    meta_date1: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "metaDate1",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class ServerSignerType:
    """
    Parameters
    ----------
    timestamp
        Timestamp when document signed Čas podpisa dokumenta
    name
        Name of signing user Ime podpisnika
    id
        Identification number of signing user Identifikacijska številka
        podpisnika
    """

    class Meta:
        name = "serverSignerType"

    timestamp: None | XmlDateTime = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    name: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )
    id: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )


@dataclass(unsafe_hash=True, kw_only=True)
class SignerType:
    """
    Parameters
    ----------
    timestamp
        Timestamp when document signed (informative) Čas podpisa dokumenta
        (informativen)
    name
        Name of signing user (from certificate) Ime podpisnika (iz
        digitalnega potrdila)
    """

    class Meta:
        name = "signerType"

    timestamp: None | XmlDateTime = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    name: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "required": True,
        }
    )


class TaxpayerTypeType(Enum):
    """
    Properties
    ----------
    FO
        Fizična oseba
    PO
        Pravna oseba
    SP
        Fizična oseba z dejavnostjo
    """

    FO = "FO"
    PO = "PO"
    SP = "SP"


@dataclass(unsafe_hash=True, kw_only=True)
class WorkflowType:
    """
    Parameters
    ----------
    document_workflow_id
        Vrsta dokumenta - šifra
    document_workflow_name
        Vrsta dokumenta - naziv
    """

    class Meta:
        name = "workflowType"

    document_workflow_id: None | str = field(
        default=None,
        metadata={
            "name": "DocumentWorkflowID",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "max_length": 1,
        },
    )
    document_workflow_name: None | str = field(
        default=None,
        metadata={
            "name": "DocumentWorkflowName",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class DepositorServerSignature:
    """
    Document depositor.

    Dokument vložil.

    Parameters
    ----------
    depositor
    receipt
    schemas_hermes_softlab_com_2003_09_signatures_element
    w3_org_2000_09_xmldsig_element
        Place for ds:Signature element
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    depositor: ServerSignerType = field(
        metadata={
            "name": "Depositor",
            "type": "Element",
            "required": True,
        }
    )
    receipt: ReceiptType = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    schemas_hermes_softlab_com_2003_09_signatures_element: None | object = (
        field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "urn:schemas-hermes-softlab-com:2003/09/Signatures",
            },
        )
    )
    w3_org_2000_09_xmldsig_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class PreparerServerSignature:
    """
    Document preparer.

    Dokument pripravil.

    Parameters
    ----------
    preparer
    schemas_hermes_softlab_com_2003_09_signatures_element
    w3_org_2000_09_xmldsig_element
        Place for ds:Signature element
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    preparer: ServerSignerType = field(
        metadata={
            "name": "Preparer",
            "type": "Element",
            "required": True,
        }
    )
    schemas_hermes_softlab_com_2003_09_signatures_element: None | object = (
        field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "urn:schemas-hermes-softlab-com:2003/09/Signatures",
            },
        )
    )
    w3_org_2000_09_xmldsig_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class ServerSignature:
    """
    Signature confirming reception of the document by DURS.

    Placed inside the
    edp:DepositorSignature/ds:Signature/ds:Object[@Id='ServerSignatureObject'].

    Parameters
    ----------
    receipt
    schemas_hermes_softlab_com_2003_09_signatures_element
    w3_org_2000_09_xmldsig_element
        Place for ds:Signature element
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    receipt: ReceiptType = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    schemas_hermes_softlab_com_2003_09_signatures_element: None | object = (
        field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "urn:schemas-hermes-softlab-com:2003/09/Signatures",
            },
        )
    )
    w3_org_2000_09_xmldsig_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class TaxPayerType:
    """
    Parameters
    ----------
    tax_number
    vat_number
    taxpayer_type
    name
    address1
    address2
    city
    post_number
    post_name
    municipality_name
    birth_date
    maticna_stevilka
        Maticna stevilka
    invalidsko_podjetje
        Maticna stevilka
    resident
    activity_code
    activity_name
    country_id
    country_name
    """

    class Meta:
        name = "taxPayerType"

    tax_number: None | str = field(
        default=None,
        metadata={
            "name": "taxNumber",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "pattern": r"[0-9]{8}",
        },
    )
    vat_number: None | str = field(
        default=None,
        metadata={
            "name": "vatNumber",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "pattern": r"[A-Z][A-Z].+",
        },
    )
    taxpayer_type: None | TaxpayerTypeType = field(
        default=None,
        metadata={
            "name": "taxpayerType",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    address1: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    address2: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    city: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    post_number: None | str = field(
        default=None,
        metadata={
            "name": "postNumber",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
            "max_length": 12,
        },
    )
    post_name: None | str = field(
        default=None,
        metadata={
            "name": "postName",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    municipality_name: None | str = field(
        default=None,
        metadata={
            "name": "municipalityName",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    birth_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "birthDate",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    maticna_stevilka: None | str = field(
        default=None,
        metadata={
            "name": "maticnaStevilka",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    invalidsko_podjetje: None | bool = field(
        default=None,
        metadata={
            "name": "invalidskoPodjetje",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    resident: None | bool = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    activity_code: None | str = field(
        default=None,
        metadata={
            "name": "activityCode",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    activity_name: None | str = field(
        default=None,
        metadata={
            "name": "activityName",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    country_id: None | str = field(
        default=None,
        metadata={
            "name": "countryID",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )
    country_name: None | str = field(
        default=None,
        metadata={
            "name": "countryName",
            "type": "Element",
            "namespace": "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class Header:
    """
    Parameters
    ----------
    taxpayer
        Tax payer for this document Podatki o davčnem zavezancu za ta
        dokument
    response_to
        This document is a response to another document (document id) Ta
        dokument je odgovor na drug dokument (document id)
    workflow
        Podatki o workflowu dokumenta
    custodian_info
        Podatki skrbnika / vnasa skrbnik
    domain
        System where document is deposited Domena sistema kamor je vložen
        dokument
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    taxpayer: TaxPayerType = field(
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    response_to: None | str = field(
        default=None,
        metadata={
            "name": "responseTo",
            "type": "Element",
        },
    )
    workflow: None | WorkflowType = field(
        default=None,
        metadata={
            "name": "Workflow",
            "type": "Element",
        },
    )
    custodian_info: None | CustodianType = field(
        default=None,
        metadata={
            "name": "CustodianInfo",
            "type": "Element",
        },
    )
    domain: None | str = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )


@dataclass(unsafe_hash=True, kw_only=True)
class Signatures:
    """
    Document signature(s) Podpisi na dokumentu.

    Parameters
    ----------
    preparer_signature
        Signature of the person that prepared the document. Podpis osebe ki
        je pripravila dokument.
    depositor_signature
        Signature of the person that deposited the document. Podpis osebe ki
        je vložila dokument.
    preparer_server_signature
    depositor_server_signature
    server_signature
    non_edp
        Document information for documents coming from the backend system
        (not signed). Podatki od dokumentih iz zalednega sistema (niso
        podpisani)
    """

    class Meta:
        namespace = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    preparer_signature: None | Signatures.PreparerSignature = field(
        default=None,
        metadata={
            "name": "PreparerSignature",
            "type": "Element",
        },
    )
    depositor_signature: None | Signatures.DepositorSignature = field(
        default=None,
        metadata={
            "name": "DepositorSignature",
            "type": "Element",
        },
    )
    preparer_server_signature: None | PreparerServerSignature = field(
        default=None,
        metadata={
            "name": "PreparerServerSignature",
            "type": "Element",
        },
    )
    depositor_server_signature: None | DepositorServerSignature = field(
        default=None,
        metadata={
            "name": "DepositorServerSignature",
            "type": "Element",
        },
    )
    server_signature: None | ServerSignature = field(
        default=None,
        metadata={
            "name": "ServerSignature",
            "type": "Element",
        },
    )
    non_edp: None | Signatures.NonEdp = field(
        default=None,
        metadata={
            "name": "NonEDP",
            "type": "Element",
        },
    )

    @dataclass(unsafe_hash=True, kw_only=True)
    class PreparerSignature:
        """
        Parameters
        ----------
        preparer
        schemas_hermes_softlab_com_2003_09_signatures_element
        w3_org_2000_09_xmldsig_element
            Place for ds:Signature element
        """

        preparer: SignerType = field(
            metadata={
                "name": "Preparer",
                "type": "Element",
                "required": True,
            }
        )
        schemas_hermes_softlab_com_2003_09_signatures_element: (
            None | object
        ) = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "urn:schemas-hermes-softlab-com:2003/09/Signatures",
            },
        )
        w3_org_2000_09_xmldsig_element: None | object = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "http://www.w3.org/2000/09/xmldsig#",
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class DepositorSignature:
        """
        Parameters
        ----------
        depositor
        schemas_hermes_softlab_com_2003_09_signatures_element
        w3_org_2000_09_xmldsig_element
            Place for ds:Signature element
        """

        depositor: SignerType = field(
            metadata={
                "name": "Depositor",
                "type": "Element",
                "required": True,
            }
        )
        schemas_hermes_softlab_com_2003_09_signatures_element: (
            None | object
        ) = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "urn:schemas-hermes-softlab-com:2003/09/Signatures",
            },
        )
        w3_org_2000_09_xmldsig_element: None | object = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "http://www.w3.org/2000/09/xmldsig#",
            },
        )

    @dataclass(unsafe_hash=True, kw_only=True)
    class NonEdp:
        receipt: ReceiptType = field(
            metadata={
                "type": "Element",
                "required": True,
            }
        )
