import urllib.request
import sys
import xml.etree.ElementTree
import os.path
from xml.dom import minidom

""" Fetch ib-affiliates.xml from GitHub if it doesn't exist and use the data for Doh-Obr.xml """
def getIbAffiliateInfo(ibEntities, accountId):
    ibAffiliateCode = getIbEntityCode(ibEntities, accountId)
    if not os.path.isfile("ib-affiliates.xml"):
        urllib.request.urlretrieve(
            "https://github.com/jamsix/ib-edavki/raw/master/ib-affiliates.xml",
            "ib-affiliates.xml",
        )
    if os.path.isfile("ib-affiliates.xml"):
        ibAffiliateInfos = xml.etree.ElementTree.parse("ib-affiliates.xml").getroot()
        for affiliate in ibAffiliateInfos:
            if affiliate.find("code").text == str(ibAffiliateCode):
                return {
                    "code": affiliate.find("code").text,
                    "name": affiliate.find("name").text,
                    "taxNumber": affiliate.find("taxNumber").text,
                    "address": affiliate.find("address").text,
                    "country": affiliate.find("country").text,
                }
    return {
        "code": "",
        "name": "",
        "taxNumber": "",
        "address": "",
        "country": "",
    }

""" Get the IB entity matching account id """
def getIbEntityCode(ibEntities, accountId):
    for ibEntity in ibEntities:
        if (ibEntity["accountId"] == accountId):
            return ibEntity["ibEntity"]
    
    print("IB Entity for account "
        + accountId + " "
        + "not found in flex statement. "
        + "Check your report settings.")
    
    return None

""" Get interest from IB XML """
def generate(taxpayerConfig,
             ibEntities,
             ibCashTransactionsList,
             rates,
             reportYear,
             test,
             testYearDiff):
    interests = []
    for ibCashTransactions in ibCashTransactionsList:
        if ibCashTransactions is None:
            continue
        for ibCashTransaction in ibCashTransactions:
            if (
                ibCashTransaction.tag == "CashTransaction"
                and ibCashTransaction.get("dateTime").startswith(str(reportYear))
                and ibCashTransaction.get("type")
                in ["Broker Interest Received", "Broker Fees"]
            ):
                interest = {
                    "accountId": ibCashTransaction.get("accountId"),
                    "currency": ibCashTransaction.get("currency"),
                    "amount": float(ibCashTransaction.get("amount")),
                    "description": ibCashTransaction.get("description"),
                    "dateTime": ibCashTransaction.get("dateTime"),
                    "tax": 0,
                    "taxEUR": 0,
                }

                """ Convert amount to EUR """
                if interest["currency"] == "EUR":
                    interest["amountEUR"] = interest["amount"]
                else:
                    date = interest["dateTime"][0:8]
                    currency = interest["currency"]
                    if date in rates and currency in rates[date]:
                        rate = float(rates[date][currency])
                    else:
                        for i in range(0, 6):
                            date = str(int(date) - 1)
                            if date in rates and currency in rates[date]:
                                rate = float(rates[date][currency])
                                print(
                                    "There is no exchange rate for "
                                    + str(interest["dateTime"][0:8])
                                    + ", using "
                                    + str(date)
                                )
                                break
                            if i == 6:
                                sys.exit(
                                    "Error: There is no exchange rate for " + str(date)
                                )
                    interest["amountEUR"] = interest["amount"] / rate
                interests.append(interest)

    """ Merge multiple dividends or payments in lieu of dividents on the same day from the same company into a single entry """
    mergedInterests = []
    for interest in interests:
        merged = False
        for mergedInterest in mergedInterests:
            if interest["dateTime"][0:8] == mergedInterest["dateTime"][0:8]:
                mergedInterest["amountEUR"] = (
                    mergedInterest["amountEUR"] + interest["amountEUR"]
                )
                mergedInterest["taxEUR"] = mergedInterest["taxEUR"] + interest["taxEUR"]
                merged = True
                break
        if merged == False:
            mergedInterests.append(interest)
    interests = mergedInterests

    """ Generate Doh-Obr.xml """
    envelope = xml.etree.ElementTree.Element(
        "Envelope", xmlns="http://edavki.durs.si/Documents/Schemas/Doh_Obr_2.xsd"
    )
    envelope.set(
        "xmlns:edp", "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"
    )
    header = xml.etree.ElementTree.SubElement(envelope, "edp:Header")
    taxpayer = xml.etree.ElementTree.SubElement(header, "edp:taxpayer")
    xml.etree.ElementTree.SubElement(taxpayer, "edp:taxNumber").text = taxpayerConfig[
        "taxNumber"
    ]
    xml.etree.ElementTree.SubElement(
        taxpayer, "edp:taxpayerType"
    ).text = taxpayerConfig["taxpayerType"]
    xml.etree.ElementTree.SubElement(taxpayer, "edp:name").text = taxpayerConfig["name"]
    xml.etree.ElementTree.SubElement(taxpayer, "edp:address1").text = taxpayerConfig[
        "address1"
    ]
    xml.etree.ElementTree.SubElement(taxpayer, "edp:city").text = taxpayerConfig["city"]
    xml.etree.ElementTree.SubElement(taxpayer, "edp:postNumber").text = taxpayerConfig[
        "postNumber"
    ]
    xml.etree.ElementTree.SubElement(taxpayer, "edp:postName").text = taxpayerConfig[
        "postName"
    ]
    xml.etree.ElementTree.SubElement(envelope, "edp:AttachmentList")
    xml.etree.ElementTree.SubElement(envelope, "edp:Signatures")
    body = xml.etree.ElementTree.SubElement(envelope, "body")
    xml.etree.ElementTree.SubElement(body, "edp:bodyContent")
    Doh_Obr = xml.etree.ElementTree.SubElement(body, "Doh_Obr")
    if test == True:
        dYear = str(reportYear + testYearDiff)
    else:
        dYear = str(reportYear)
    xml.etree.ElementTree.SubElement(Doh_Obr, "Period").text = dYear
    if test == True:
        xml.etree.ElementTree.SubElement(Doh_Obr, "DocumentWorkflowID").text = "I"
    else:
        xml.etree.ElementTree.SubElement(Doh_Obr, "DocumentWorkflowID").text = "O"
    xml.etree.ElementTree.SubElement(Doh_Obr, "Email").text = taxpayerConfig[
        "email"
    ]
    xml.etree.ElementTree.SubElement(Doh_Obr, "TelephoneNumber").text = taxpayerConfig[
        "telephoneNumber"
    ]
    xml.etree.ElementTree.SubElement(Doh_Obr, "ResidentOfRepublicOfSlovenia"
    ).text = taxpayerConfig[
        "isResident"
    ]
    xml.etree.ElementTree.SubElement(Doh_Obr, "Country").text = taxpayerConfig[
        "residentCountry"
    ]

    interests = sorted(interests, key=lambda k: k["dateTime"][0:8])
    for interest in interests:
        if round(interest["amountEUR"], 2) <= 0:
            continue
        Interest = xml.etree.ElementTree.SubElement(Doh_Obr, "Interest")

        ibAffiliateInfo = getIbAffiliateInfo(ibEntities, interest["accountId"])

        xml.etree.ElementTree.SubElement(Interest, "Date").text = (
            dYear + "-" + interest["dateTime"][4:6] + "-" + interest["dateTime"][6:8]
        )
        xml.etree.ElementTree.SubElement(
            Interest, "IdentificationNumber"
        ).text = ibAffiliateInfo["taxNumber"]
        xml.etree.ElementTree.SubElement(Interest, "Name").text = ibAffiliateInfo[
            "name"
        ]
        xml.etree.ElementTree.SubElement(Interest, "Address").text = ibAffiliateInfo[
            "address"
        ]
        xml.etree.ElementTree.SubElement(Interest, "Country").text = ibAffiliateInfo[
            "country"
        ]
        xml.etree.ElementTree.SubElement(Interest, "Type").text = "2"
        xml.etree.ElementTree.SubElement(Interest, "Value").text = "{0:.2f}".format(
            interest["amountEUR"]
        )
        xml.etree.ElementTree.SubElement(
            Interest, "ForeignTax"
        ).text = "{0:.2f}".format(interest["taxEUR"])
        if "country" in interest:
            xml.etree.ElementTree.SubElement(Interest, "Country2").text = interest[
                "country"
            ]

    xmlString = xml.etree.ElementTree.tostring(envelope)
    prettyXmlString = minidom.parseString(xmlString).toprettyxml(indent="\t")
    with open("Doh-Obr.xml", "w", encoding="utf-8") as f:
        f.write(prettyXmlString)
        print("Doh-Obr.xml created")
