#!/usr/bin/python

import urllib.request
import sys
import xml.etree.ElementTree
import datetime
import os
import glob
import copy
import argparse
import shutil
from xml.dom import minidom
import re


bsRateXmlUrl = "https://www.bsi.si/_data/tecajnice/dtecbs-l.xml"
normalAssets = ["STK"]
derivateAssets = ["CFD", "OPT", "FUT", "FOP", "WAR"]
ignoreAssets = ["CASH", "CMDTY"]


stockSplits = {}


def getSplitMultiplier(symbol, date):
    multiplier = 1

    if symbol in stockSplits:
        for splitData in stockSplits[symbol]:
            if datetime.datetime.strptime(date, "%Y%m%d") < splitData["date"]:
                multiplier *= splitData["multiplier"]

    return multiplier


def addStockSplits(corporateActions):
    for action in corporateActions:
        description = action.attrib["description"]
        descriptionSearch = re.search(r"SPLIT (.+) FOR (.+) \(", description)
        if descriptionSearch is not None:
            # we have to extract split information from description since IB does not provide
            # any information on what the corporate action is

            multiplier = float(descriptionSearch.group(1)) / float(
                descriptionSearch.group(2)
            )
            symbol = action.attrib["symbol"]
            date = datetime.datetime.strptime(action.attrib["reportDate"], "%Y%m%d")
            if symbol not in stockSplits:
                stockSplits[symbol] = []

            # check if the same split was added from a different report
            for split in stockSplits[symbol]:
                if split["date"] == date and split["multiplier"] == multiplier:
                    continue

            stockSplits[symbol].append({"date": date, "multiplier": multiplier})


def main():
    if not os.path.isfile("taxpayer.xml"):
        print("Modify taxpayer.xml and add your data first!")
        f = open("taxpayer.xml", "w+", encoding="utf-8")
        f.write(
            "<taxpayer>\n"
            "   <taxNumber>12345678</taxNumber>\n"
            "   <taxpayerType>FO</taxpayerType>\n"
            "   <name>Janez Novak</name>\n"
            "   <address1>Slovenska 1</address1>\n"
            "   <city>Ljubljana</city>\n"
            "   <postNumber>1000</postNumber>\n"
            "   <postName>Ljubljana</postName>\n"
            "   <email>janez.novak@furs.si</email>\n"
            "   <telephoneNumber>01 123 45 67</telephoneNumber>\n"
            "   <residentCountry>SI</residentCountry>\n"
            "   <isResident>true</isResident>\n"
            "</taxpayer>"
        )
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ibXmlFiles",
        metavar="ib-xml-file",
        help="InteractiveBrokers XML ouput file(s) (see README.md on how to generate one)",
        nargs="+",
    )
    parser.add_argument(
        "-y",
        metavar="report-year",
        type=int,
        default=0,
        help="Report will be generated for the provided calendar year (defaults to "
        + str(datetime.date.today().year - 1)
        + ")",
    )
    parser.add_argument(
        "-t",
        help="Change trade dates to previous year (see README.md)",
        action="store_true",
    )

    args = parser.parse_args()
    ibXmlFilenames = args.ibXmlFiles
    test = args.t
    if args.y == 0:
        if test == True:
            reportYear = datetime.date.today().year
        else:
            reportYear = datetime.date.today().year - 1
    else:
        reportYear = int(args.y)

    if test == True:
        testYearDiff = reportYear - datetime.date.today().year - 1

    """ Parse taxpayer information from the local taxpayer.xml file """
    taxpayer = xml.etree.ElementTree.parse("taxpayer.xml").getroot()
    taxpayerConfig = {
        "taxNumber": taxpayer.find("taxNumber").text,
        "taxpayerType": "FO",
        "name": taxpayer.find("name").text,
        "address1": taxpayer.find("address1").text,
        "city": taxpayer.find("city").text,
        "postNumber": taxpayer.find("postNumber").text,
        "postName": taxpayer.find("postName").text,
        "email": taxpayer.find("email").text,
        "telephoneNumber": taxpayer.find("telephoneNumber").text,
        "residentCountry": taxpayer.find("residentCountry").text,
        "isResident": taxpayer.find("isResident").text,
    }

    """ Fetch companies.xml from GitHub if it doesn't exist and use the data for Doh-Div.xml """
    companies = {}
    if not os.path.isfile("companies.xml"):
        urllib.request.urlretrieve(
            "https://github.com/jamsix/ib-edavki/raw/master/companies.xml",
            "companies.xml",
        )
    if os.path.isfile("companies.xml"):
        cmpns = xml.etree.ElementTree.parse("companies.xml").getroot()
        for company in cmpns:
            c = {
                "symbol": company.find("symbol").text,
                "name": company.find("name").text,
                "taxNumber": company.find("taxNumber").text,
                "address": company.find("address").text,
                "country": company.find("country").text,
            }
            companies[c["symbol"]] = c

    """ Fetch relief-statements.xml from GitHub if it doesn't exist and use the data for Doh-Div.xml """
    if not os.path.isfile("relief-statements.xml"):
        urllib.request.urlretrieve(
            "https://github.com/jamsix/ib-edavki/raw/master/relief-statements.xml",
            "treaties.xml",
        )
    if os.path.isfile("relief-statements.xml"):
        statements = xml.etree.ElementTree.parse("relief-statements.xml").getroot()
        for statement in statements:
            for symbol in companies:
                if companies[symbol]["country"] == statement.find("country").text:
                    companies[symbol]["reliefStatement"] = statement.find(
                        "statement"
                    ).text

    """ Creating daily exchange rates object """
    bsRateXmlFilename = (
        "bsrate-"
        + str(datetime.date.today().year)
        + str(datetime.date.today().month)
        + str(datetime.date.today().day)
        + ".xml"
    )
    if not os.path.isfile(bsRateXmlFilename):
        for file in glob.glob("bsrate-*.xml"):
            os.remove(file)
        urllib.request.urlretrieve(bsRateXmlUrl, bsRateXmlFilename)
    bsRateXml = xml.etree.ElementTree.parse(bsRateXmlFilename).getroot()
    bsRates = bsRateXml.find("DtecBS")

    rates = {}
    for d in bsRateXml:
        date = d.attrib["datum"].replace("-", "")
        rates[date] = {}
        for r in d:
            currency = r.attrib["oznaka"]
            rates[date][currency] = r.text

    """ Parsing IB XMLs """
    ibTradesList = []
    ibCashTransactionsList = []
    ibSecuritiesInfoList = []
    for ibXmlFilename in ibXmlFilenames:
        ibXml = xml.etree.ElementTree.parse(ibXmlFilename).getroot()
        ibTradesList.append(ibXml[0][0].find("Trades"))
        """ibPositions = ibXml[0][0].find('OpenPositions')"""
        ibCashTransactionsList.append(ibXml[0][0].find("CashTransactions"))
        ibSecuritiesInfoList.append(ibXml[0][0].find("SecuritiesInfo"))
        ibFlexStatement = ibXml[0][0]

        corporateActions = ibXml[0][0].find("CorporateActions")
        if corporateActions is not None:
            addStockSplits(corporateActions)

    if test == True:
        statementStartDate = str(reportYear + testYearDiff) + "0101"
        statementEndDate = str(reportYear + testYearDiff) + "1231"
    else:
        statementStartDate = str(reportYear) + "0101"
        statementEndDate = str(reportYear) + "1231"

    """ Dictionary of stock trade arrays, each key represents one securityID """
    trades = {}

    """ Get trades from IB XML and sort them by securityID """
    for ibTrades in ibTradesList:
        if ibTrades is None:
            continue
        for ibTrade in ibTrades:
            if ibTrade.attrib["assetCategory"] in ignoreAssets:
                continue

            if ibTrade.tag == "Trade":
                try:
                    time = ibTrade.attrib["tradeTime"]
                except KeyError:
                    time = "0"
                trade = {
                    "conid": ibTrade.attrib["conid"],
                    "symbol": ibTrade.attrib["symbol"],
                    "currency": ibTrade.attrib["currency"],
                    "assetCategory": ibTrade.attrib["assetCategory"],
                    "tradePrice": float(ibTrade.attrib["tradePrice"]),
                    "quantity": float(ibTrade.attrib["quantity"]),
                    "buySell": ibTrade.attrib["buySell"],
                    "tradeDate": ibTrade.attrib["tradeDate"],
                    "tradeTime": time,
                    "transactionID": ibTrade.attrib["transactionID"],
                    "ibOrderID": ibTrade.attrib["ibOrderID"],
                    "openCloseIndicator": ibTrade.attrib["openCloseIndicator"],
                }

                splitMultiplier = getSplitMultiplier(
                    trade["symbol"], trade["tradeDate"]
                )

                trade["quantity"] *= splitMultiplier
                trade["tradePrice"] /= splitMultiplier

                if ibTrade.attrib["securityID"] != "":
                    trade["securityID"] = ibTrade.attrib["securityID"]
                if ibTrade.attrib["isin"] != "":
                    trade["isin"] = ibTrade.attrib["isin"]
                if ibTrade.attrib["cusip"] != "":
                    trade["cusip"] = ibTrade.attrib["cusip"]
                if ibTrade.attrib["description"] != "":
                    trade["description"] = ibTrade.attrib["description"]
                """ Futures and options have multipliers, i.e. a quantity of 1 with tradePrice 3 and multiplier 100 is actually a future/option for 100 stocks, worth 100 x 3 = 300 """
                if "multiplier" in ibTrade.attrib:
                    trade["tradePrice"] = trade["tradePrice"] * float(
                        ibTrade.attrib["multiplier"]
                    )
                """ If trade is an option exercise, tradePrice is set to 0, but closePrice is the one position was settled for """
                # TODO: handle warrants exercise
                if (
                    trade["assetCategory"] == "OPT"
                    and ibTrade.attrib["notes"] == "Ex"
                    and ibTrade.attrib["closePrice"] != ""
                ):
                    trade["tradePrice"] = ibTrade.attrib["closePrice"]
                    if "multiplier" in ibTrade.attrib:
                        trade["tradePrice"] = float(
                            ibTrade.attrib["closePrice"]
                        ) * float(ibTrade.attrib["multiplier"])

                lastTrade = trade

                """
                    IB is PITA in terms of unique security ID, old outputs and some asset types only have conid,
                    same assets have ISIN but had none in the past, euro ETFs can have different symbols but same ISIN.
                    Code below merges trades based on these IDs in the order of ISIN > CUSIP > securityID > CONID > Symbol
                """
                match = False
                securityID = None
                if "isin" in trade:
                    securityID = trade["isin"]
                    for xSecurityID in trades:
                        for xtrade in trades[xSecurityID]:
                            if "isin" in xtrade and xtrade["isin"] == trade["isin"]:
                                trades[xSecurityID].append(trade)
                                if xSecurityID != securityID:
                                    trades[securityID] = trades[xSecurityID]
                                    trades.pop(xSecurityID)
                                match = True
                                break
                        if match:
                            break
                    if match:
                        continue
                if "cusip" in trade:
                    if not securityID:
                        securityID = trade["cusip"]
                    for xSecurityID in trades:
                        for xtrade in trades[xSecurityID]:
                            if "cusip" in xtrade and xtrade["cusip"] == trade["cusip"]:
                                trades[xSecurityID].append(trade)
                                if xSecurityID != securityID:
                                    trades[securityID] = trades[xSecurityID]
                                    trades.pop(xSecurityID)
                                match = True
                                break
                        if match:
                            break
                    if match:
                        continue
                if "securityID" in trade:
                    if not securityID:
                        securityID = trade["securityID"]
                    for xSecurityID in trades:
                        for xtrade in trades[xSecurityID]:
                            if (
                                "securityID" in xtrade
                                and xtrade["securityID"] == trade["securityID"]
                            ):
                                trades[xSecurityID].append(trade)
                                if xSecurityID != securityID:
                                    trades[securityID] = trades[xSecurityID]
                                    trades.pop(xSecurityID)
                                match = True
                                break
                        if match:
                            break
                    if match:
                        continue
                if "conid" in trade:
                    if not securityID:
                        securityID = trade["conid"]
                    for xSecurityID in trades:
                        for xtrade in trades[xSecurityID]:
                            if "conid" in xtrade and xtrade["conid"] == trade["conid"]:
                                trades[xSecurityID].append(trade)
                                if xSecurityID != securityID:
                                    trades[securityID] = trades[xSecurityID]
                                    trades.pop(xSecurityID)
                                match = True
                                break
                        if match:
                            break
                    if match:
                        continue
                if "symbol" in trade:
                    if not securityID:
                        securityID = trade["symbol"]
                    for xSecurityID in trades:
                        for xtrade in trades[xSecurityID]:
                            if (
                                "symbol" in xtrade
                                and xtrade["symbol"] == trade["symbol"]
                            ):
                                trades[xSecurityID].append(trade)
                                if xSecurityID != securityID:
                                    trades[securityID] = trades[xSecurityID]
                                    trades.pop(xSecurityID)
                                match = True
                                break
                        if match:
                            break
                    if match:
                        continue

                trades[securityID] = [trade]

            elif ibTrade.tag == "Lot" and lastTrade != None:
                if "openTransactionIds" not in lastTrade:
                    lastTrade["openTransactionIds"] = {}
                tid = ibTrade.attrib["transactionID"]

                splitMultiplier = getSplitMultiplier(
                    ibTrade.attrib["symbol"], ibTrade.attrib["tradeDate"]
                )

                if tid not in lastTrade["openTransactionIds"]:
                    lastTrade["openTransactionIds"][tid] = (
                        float(ibTrade.attrib["quantity"]) * splitMultiplier
                    )
                else:
                    lastTrade["openTransactionIds"][tid] += (
                        float(ibTrade.attrib["quantity"]) * splitMultiplier
                    )

    """ Detect if trades are Normal or Derivates and if they are Opening or Closing positions
        Convert the price to EUR """
    for securityID in trades:
        beforeTradePosition = 0
        for trade in trades[securityID]:
            if trade["currency"] == "EUR":
                trade["tradePriceEUR"] = trade["tradePrice"]
            else:
                date = trade["tradeDate"]
                currency = trade["currency"]
                if date in rates and currency in rates[date]:
                    rate = float(rates[date][currency])
                else:
                    for i in range(0, 6):
                        date = str(int(date) - 1)
                        if date in rates and currency in rates[date]:
                            rate = float(rates[date][currency])
                            print(
                                "There is no exchange rate for "
                                + str(trade["tradeDate"])
                                + ", using "
                                + str(date)
                            )
                            break
                        if i == 6:
                            sys.exit(
                                "Error: There is no exchange rate for " + str(date)
                            )
                trade["tradePriceEUR"] = trade["tradePrice"] / rate

            if (trade["openCloseIndicator"] == "O" and trade["quantity"] > 0) or (
                trade["openCloseIndicator"] == "C" and trade["quantity"] < 0
            ):
                trade["positionType"] = "long"
            else:
                trade["positionType"] = "short"

            if trade["assetCategory"] in normalAssets:
                trade["assetType"] = "normal"
            elif trade["assetCategory"] in derivateAssets:
                trade["assetType"] = "derivate"

    """ Filter trades to only include those that closed in the parameter year and trades that opened the closing position """
    yearTrades = {}
    for securityID in trades:
        for trade in trades[securityID]:
            if (
                trade["tradeDate"][0:4] == str(reportYear)
                and trade["openCloseIndicator"] == "C"
            ):
                if securityID not in yearTrades:
                    yearTrades[securityID] = []
                for xtrade in trades[securityID]:
                    if xtrade["transactionID"] in trade["openTransactionIds"]:
                        ctrade = copy.copy(xtrade)
                        tid = ctrade["transactionID"]
                        ctrade["quantity"] = trade["openTransactionIds"][tid]
                        yearTrades[securityID].append(ctrade)

                yearTrades[securityID].append(trade)

    """ Logical trade order can be executed as multiple suborders at different price. Merge suborders in a single logical order. """
    mergedTrades = {}
    for securityID in yearTrades:
        for trade in yearTrades[securityID]:
            tradeExists = False
            if securityID in mergedTrades:
                for previousTrade in mergedTrades[securityID]:
                    if previousTrade["ibOrderID"] == trade["ibOrderID"]:
                        previousTrade["tradePrice"] = (
                            previousTrade["quantity"] * previousTrade["tradePrice"]
                            + trade["quantity"] * trade["tradePrice"]
                        ) / (previousTrade["quantity"] + trade["quantity"])
                        previousTrade["quantity"] = (
                            previousTrade["quantity"] + trade["quantity"]
                        )
                        tradeExists = True
                        break
            if tradeExists == False:
                if securityID not in mergedTrades:
                    mergedTrades[securityID] = []
                mergedTrades[securityID].append(trade)

    """ Sort the trades by time """
    for securityID in mergedTrades:
        l = sorted(
            mergedTrades[securityID],
            key=lambda k: "%s%s" % (k["tradeDate"], k["tradeTime"]),
        )
        mergedTrades[securityID] = l

    """ Sort the trades in 4 categories """
    longNormalTrades = {}
    shortNormalTrades = {}
    longDerivateTrades = {}
    shortDerivateTrades = {}

    for securityID in mergedTrades:
        for trade in mergedTrades[securityID]:
            if trade["assetType"] == "normal" and trade["positionType"] == "long":
                if securityID not in longNormalTrades:
                    longNormalTrades[securityID] = []
                longNormalTrades[securityID].append(trade)
            elif trade["assetType"] == "normal" and trade["positionType"] == "short":
                if securityID not in shortNormalTrades:
                    shortNormalTrades[securityID] = []
                shortNormalTrades[securityID].append(trade)
            elif trade["assetType"] == "derivate" and trade["positionType"] == "long":
                if securityID not in longDerivateTrades:
                    longDerivateTrades[securityID] = []
                longDerivateTrades[securityID].append(trade)
            elif trade["assetType"] == "derivate" and trade["positionType"] == "short":
                if securityID not in shortDerivateTrades:
                    shortDerivateTrades[securityID] = []
                shortDerivateTrades[securityID].append(trade)
            else:
                sys.exit(
                    "Error: cannot figure out if trade is Normal or Derivate, Long or Short"
                )

    """ Generate the files for Normal """
    envelope = xml.etree.ElementTree.Element(
        "Envelope", xmlns="http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"
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
    Doh_KDVP = xml.etree.ElementTree.SubElement(body, "Doh_KDVP")
    KDVP = xml.etree.ElementTree.SubElement(Doh_KDVP, "KDVP")
    if test == True:
        xml.etree.ElementTree.SubElement(KDVP, "DocumentWorkflowID").text = "I"
    else:
        xml.etree.ElementTree.SubElement(KDVP, "DocumentWorkflowID").text = "O"
    xml.etree.ElementTree.SubElement(KDVP, "Year").text = statementEndDate[0:4]
    xml.etree.ElementTree.SubElement(KDVP, "PeriodStart").text = (
        statementStartDate[0:4]
        + "-"
        + statementStartDate[4:6]
        + "-"
        + statementStartDate[6:8]
    )
    xml.etree.ElementTree.SubElement(KDVP, "PeriodEnd").text = (
        statementEndDate[0:4]
        + "-"
        + statementEndDate[4:6]
        + "-"
        + statementEndDate[6:8]
    )
    xml.etree.ElementTree.SubElement(KDVP, "IsResident").text = "true"
    xml.etree.ElementTree.SubElement(KDVP, "TelephoneNumber").text = taxpayerConfig[
        "telephoneNumber"
    ]
    xml.etree.ElementTree.SubElement(KDVP, "SecurityCount").text = str(
        len(longNormalTrades)
    )
    xml.etree.ElementTree.SubElement(KDVP, "SecurityShortCount").text = str(
        len(shortNormalTrades)
    )
    xml.etree.ElementTree.SubElement(KDVP, "SecurityWithContractCount").text = "0"
    xml.etree.ElementTree.SubElement(KDVP, "SecurityWithContractShortCount").text = "0"
    xml.etree.ElementTree.SubElement(KDVP, "ShareCount").text = "0"
    xml.etree.ElementTree.SubElement(KDVP, "Email").text = taxpayerConfig["email"]

    for securityID in longNormalTrades:
        trades = longNormalTrades[securityID]
        KDVPItem = xml.etree.ElementTree.SubElement(Doh_KDVP, "KDVPItem")
        InventoryListType = xml.etree.ElementTree.SubElement(
            KDVPItem, "InventoryListType"
        ).text = "PLVP"
        Name = xml.etree.ElementTree.SubElement(KDVPItem, "Name").text = trades[0][
            "description"
        ]
        HasForeignTax = xml.etree.ElementTree.SubElement(
            KDVPItem, "HasForeignTax"
        ).text = "false"
        HasLossTransfer = xml.etree.ElementTree.SubElement(
            KDVPItem, "HasLossTransfer"
        ).text = "false"
        ForeignTransfer = xml.etree.ElementTree.SubElement(
            KDVPItem, "ForeignTransfer"
        ).text = "false"
        TaxDecreaseConformance = xml.etree.ElementTree.SubElement(
            KDVPItem, "TaxDecreaseConformance"
        ).text = "false"
        Securities = xml.etree.ElementTree.SubElement(KDVPItem, "Securities")
        if len(trades) > 0 and "isin" in trades[0]:
            ISIN = xml.etree.ElementTree.SubElement(Securities, "ISIN").text = trades[
                0
            ]["isin"]
        Code = xml.etree.ElementTree.SubElement(Securities, "Code").text = trades[0][
            "symbol"
        ][:10]
        if len(trades) > 0 and "description" in trades[0]:
            Name = xml.etree.ElementTree.SubElement(Securities, "Name").text = trades[
                0
            ]["description"]
        IsFond = xml.etree.ElementTree.SubElement(Securities, "IsFond").text = "false"

        F8Value = 0
        n = -1
        for trade in trades:
            n += 1
            if test == True:
                tradeYear = int(trade["tradeDate"][0:4]) + testYearDiff
            else:
                tradeYear = int(trade["tradeDate"][0:4])
            Row = xml.etree.ElementTree.SubElement(Securities, "Row")
            ID = xml.etree.ElementTree.SubElement(Row, "ID").text = str(n)
            if trade["quantity"] > 0:
                PurchaseSale = xml.etree.ElementTree.SubElement(Row, "Purchase")
                F1 = xml.etree.ElementTree.SubElement(PurchaseSale, "F1").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F2 = xml.etree.ElementTree.SubElement(PurchaseSale, "F2").text = "B"
                F3 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F3"
                ).text = "{0:.4f}".format(trade["quantity"])
                F4 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F4"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
                F5 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F5"
                ).text = "0.0000"
            else:
                PurchaseSale = xml.etree.ElementTree.SubElement(Row, "Sale")
                F6 = xml.etree.ElementTree.SubElement(PurchaseSale, "F6").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F7 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F7"
                ).text = "{0:.4f}".format(-trade["quantity"])
                F9 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F9"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
            F8Value += trade["quantity"]
            F8 = xml.etree.ElementTree.SubElement(Row, "F8").text = "{0:.4f}".format(
                F8Value
            )

    for securityID in shortNormalTrades:
        trades = shortNormalTrades[securityID]
        KDVPItem = xml.etree.ElementTree.SubElement(Doh_KDVP, "KDVPItem")
        InventoryListType = xml.etree.ElementTree.SubElement(
            KDVPItem, "InventoryListType"
        ).text = "PLVPSHORT"
        Name = xml.etree.ElementTree.SubElement(KDVPItem, "Name").text = trades[0][
            "description"
        ]
        HasForeignTax = xml.etree.ElementTree.SubElement(
            KDVPItem, "HasForeignTax"
        ).text = "false"
        HasLossTransfer = xml.etree.ElementTree.SubElement(
            KDVPItem, "HasLossTransfer"
        ).text = "false"
        ForeignTransfer = xml.etree.ElementTree.SubElement(
            KDVPItem, "ForeignTransfer"
        ).text = "false"
        TaxDecreaseConformance = xml.etree.ElementTree.SubElement(
            KDVPItem, "TaxDecreaseConformance"
        ).text = "false"
        SecuritiesShort = xml.etree.ElementTree.SubElement(KDVPItem, "SecuritiesShort")
        if len(trades) > 0 and "isin" in trades[0]:
            ISIN = xml.etree.ElementTree.SubElement(
                SecuritiesShort, "ISIN"
            ).text = trades[0]["isin"]
        Code = xml.etree.ElementTree.SubElement(SecuritiesShort, "Code").text = trades[
            0
        ]["symbol"][:10]
        if len(trades) > 0 and "description" in trades[0]:
            Name = xml.etree.ElementTree.SubElement(
                SecuritiesShort, "Name"
            ).text = trades[0]["description"]
        IsFond = xml.etree.ElementTree.SubElement(
            SecuritiesShort, "IsFond"
        ).text = "false"

        F8Value = 0
        n = -1
        for trade in trades:
            n += 1
            if test == True:
                tradeYear = int(trade["tradeDate"][0:4]) + testYearDiff
            else:
                tradeYear = int(trade["tradeDate"][0:4])
            Row = xml.etree.ElementTree.SubElement(SecuritiesShort, "Row")
            ID = xml.etree.ElementTree.SubElement(Row, "ID").text = str(n)
            if trade["quantity"] > 0:
                PurchaseSale = xml.etree.ElementTree.SubElement(Row, "Purchase")
                F1 = xml.etree.ElementTree.SubElement(PurchaseSale, "F1").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F2 = xml.etree.ElementTree.SubElement(PurchaseSale, "F2").text = "A"
                F3 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F3"
                ).text = "{0:.4f}".format(trade["quantity"])
                F4 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F4"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
                F5 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F5"
                ).text = "0.0000"
            else:
                PurchaseSale = xml.etree.ElementTree.SubElement(Row, "Sale")
                F6 = xml.etree.ElementTree.SubElement(PurchaseSale, "F6").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F7 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F7"
                ).text = "{0:.4f}".format(-trade["quantity"])
                F9 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F9"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
            F8Value += trade["quantity"]
            F8 = xml.etree.ElementTree.SubElement(Row, "F8").text = "{0:.4f}".format(
                F8Value
            )

    xmlString = xml.etree.ElementTree.tostring(envelope)
    prettyXmlString = minidom.parseString(xmlString).toprettyxml(indent="\t")
    with open("Doh-KDVP.xml", "w", encoding="utf-8") as f:
        f.write(prettyXmlString)
        print("Doh-KDVP.xml created")

    """ Generate the files for Derivates """
    envelope = xml.etree.ElementTree.Element(
        "Envelope", xmlns="http://edavki.durs.si/Documents/Schemas/D_IFI_4.xsd"
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
    workflow = xml.etree.ElementTree.SubElement(header, "edp:Workflow")
    if test == True:
        xml.etree.ElementTree.SubElement(workflow, "edp:DocumentWorkflowID").text = "I"
    else:
        xml.etree.ElementTree.SubElement(workflow, "edp:DocumentWorkflowID").text = "O"
    xml.etree.ElementTree.SubElement(envelope, "edp:AttachmentList")
    xml.etree.ElementTree.SubElement(envelope, "edp:Signatures")
    body = xml.etree.ElementTree.SubElement(envelope, "body")
    xml.etree.ElementTree.SubElement(body, "edp:bodyContent")
    difi = xml.etree.ElementTree.SubElement(body, "D_IFI")
    xml.etree.ElementTree.SubElement(difi, "PeriodStart").text = (
        statementStartDate[0:4]
        + "-"
        + statementStartDate[4:6]
        + "-"
        + statementStartDate[6:8]
    )
    xml.etree.ElementTree.SubElement(difi, "PeriodEnd").text = (
        statementEndDate[0:4]
        + "-"
        + statementEndDate[4:6]
        + "-"
        + statementEndDate[6:8]
    )
    xml.etree.ElementTree.SubElement(difi, "TelephoneNumber").text = taxpayerConfig[
        "telephoneNumber"
    ]
    xml.etree.ElementTree.SubElement(difi, "Email").text = taxpayerConfig["email"]

    n = 0
    for securityID in longDerivateTrades:
        trades = longDerivateTrades[securityID]
        n += 1
        TItem = xml.etree.ElementTree.SubElement(difi, "TItem")
        TypeId = xml.etree.ElementTree.SubElement(TItem, "TypeId").text = "PLIFI"
        if trades[0]["assetCategory"] == "FUT":
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "01"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "terminska pogodba"
        elif trades[0]["assetCategory"] == "CFD":
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "02"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "finančne pogodbe na razliko"
        elif trades[0]["assetCategory"] == "OPT":
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "03"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "opcija in certifikat"
        else:
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "04"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "drugo"
        if len(trades) > 0 and "description" in trades[0]:
            Name = xml.etree.ElementTree.SubElement(TItem, "Name").text = trades[0][
                "description"
            ]
        if trades[0]["assetCategory"] != "OPT" and trades[0]["assetCategory"] != "WAR":
            """ Option descriptions are to long and not accepted by eDavki """
            Code = xml.etree.ElementTree.SubElement(TItem, "Code").text = trades[0][
                "symbol"
            ][:10]
        if len(trades) > 0 and "isin" in trades[0]:
            ISIN = xml.etree.ElementTree.SubElement(TItem, "ISIN").text = trades[0][
                "isin"
            ]
        HasForeignTax = xml.etree.ElementTree.SubElement(
            TItem, "HasForeignTax"
        ).text = "false"

        F8Value = 0
        for trade in trades:
            if test == True:
                tradeYear = int(trade["tradeDate"][0:4]) + testYearDiff
            else:
                tradeYear = int(trade["tradeDate"][0:4])
            TSubItem = xml.etree.ElementTree.SubElement(TItem, "TSubItem")
            if trade["quantity"] > 0:
                PurchaseSale = xml.etree.ElementTree.SubElement(TSubItem, "Purchase")
                F1 = xml.etree.ElementTree.SubElement(PurchaseSale, "F1").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F2 = xml.etree.ElementTree.SubElement(PurchaseSale, "F2").text = "A"
                F3 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F3"
                ).text = "{0:.4f}".format(trade["quantity"])
                F4 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F4"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
                F9 = xml.etree.ElementTree.SubElement(PurchaseSale, "F9").text = "false"
                # TODO: kako ugotovit iz reporta F9 = Trgovanje z vzvodom
            else:
                PurchaseSale = xml.etree.ElementTree.SubElement(TSubItem, "Sale")
                F5 = xml.etree.ElementTree.SubElement(PurchaseSale, "F5").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F6 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F6"
                ).text = "{0:.4f}".format(-trade["quantity"])
                F7 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F7"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
            F8Value += trade["quantity"]
            F8 = xml.etree.ElementTree.SubElement(
                TSubItem, "F8"
            ).text = "{0:.4f}".format(F8Value)

    for securityID in shortDerivateTrades:
        trades = shortDerivateTrades[securityID]
        n += 1
        TItem = xml.etree.ElementTree.SubElement(difi, "TItem")
        TypeId = xml.etree.ElementTree.SubElement(TItem, "TypeId").text = "PLIFIShort"
        if trades[0]["assetCategory"] == "FUT":
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "01"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "terminska pogodba"
        elif trades[0]["assetCategory"] == "CFD":
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "02"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "finančne pogodbe na razliko"
        elif trades[0]["assetCategory"] == "OPT":
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "03"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "opcija in certifikat"
        else:
            Type = xml.etree.ElementTree.SubElement(TItem, "Type").text = "04"
            TypeName = xml.etree.ElementTree.SubElement(
                TItem, "TypeName"
            ).text = "drugo"
        if len(trades) > 0 and "description" in trades[0]:
            Name = xml.etree.ElementTree.SubElement(TItem, "Name").text = trades[0][
                "description"
            ]
        if trades[0]["assetCategory"] != "OPT" and trades[0]["assetCategory"] != "WAR":
            """ Option descriptions are to long and not accepted by eDavki """
            Code = xml.etree.ElementTree.SubElement(TItem, "Code").text = trades[0][
                "symbol"
            ][:10]
        if len(trades) > 0 and "isin" in trades[0]:
            ISIN = xml.etree.ElementTree.SubElement(TItem, "ISIN").text = trades[0][
                "isin"
            ]
        HasForeignTax = xml.etree.ElementTree.SubElement(
            TItem, "HasForeignTax"
        ).text = "false"

        F8Value = 0
        for trade in trades:
            if test == True:
                tradeYear = int(trade["tradeDate"][0:4]) + testYearDiff
            else:
                tradeYear = int(trade["tradeDate"][0:4])
            TShortSubItem = xml.etree.ElementTree.SubElement(TItem, "TShortSubItem")
            if trade["quantity"] > 0:
                PurchaseSale = xml.etree.ElementTree.SubElement(
                    TShortSubItem, "Purchase"
                )
                F4 = xml.etree.ElementTree.SubElement(PurchaseSale, "F4").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F5 = xml.etree.ElementTree.SubElement(PurchaseSale, "F5").text = "A"
                F6 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F6"
                ).text = "{0:.4f}".format(trade["quantity"])
                F7 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F7"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
            else:
                PurchaseSale = xml.etree.ElementTree.SubElement(TShortSubItem, "Sale")
                F1 = xml.etree.ElementTree.SubElement(PurchaseSale, "F1").text = (
                    str(tradeYear)
                    + "-"
                    + trade["tradeDate"][4:6]
                    + "-"
                    + trade["tradeDate"][6:8]
                )
                F2 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F2"
                ).text = "{0:.4f}".format(-trade["quantity"])
                F3 = xml.etree.ElementTree.SubElement(
                    PurchaseSale, "F3"
                ).text = "{0:.4f}".format(trade["tradePriceEUR"])
                F9 = xml.etree.ElementTree.SubElement(PurchaseSale, "F9").text = "false"
                # TODO: kako ugotovit iz reporta F9 = Trgovanje z vzvodom
            F8Value += trade["quantity"]
            F8 = xml.etree.ElementTree.SubElement(
                TShortSubItem, "F8"
            ).text = "{0:.4f}".format(F8Value)

    xmlString = xml.etree.ElementTree.tostring(envelope)
    prettyXmlString = minidom.parseString(xmlString).toprettyxml(indent="\t")
    with open("D-IFI.xml", "w", encoding="utf-8") as f:
        f.write(prettyXmlString)
        print("D-IFI.xml created")

    """ Get dividends from IB XML """
    dividends = []
    for ibCashTransactions in ibCashTransactionsList:
        if ibCashTransactions is None:
            continue
        for ibCashTransaction in ibCashTransactions:
            if (
                ibCashTransaction.tag == "CashTransaction"
                and ibCashTransaction.attrib["dateTime"].startswith(str(reportYear))
                and ibCashTransaction.attrib["type"]
                in ["Dividends", "Payment In Lieu Of Dividends"]
            ):
                dividend = {
                    "currency": ibCashTransaction.attrib["currency"],
                    "type": ibCashTransaction.attrib["type"],
                    "conid": ibCashTransaction.attrib["conid"],
                    "amount": float(ibCashTransaction.attrib["amount"]),
                    "symbol": ibCashTransaction.attrib["symbol"],
                    "description": ibCashTransaction.attrib["description"],
                    "dateTime": ibCashTransaction.attrib["dateTime"],
                    "transactionID": ibCashTransaction.attrib["transactionID"],
                    "tax": 0,
                    "taxEUR": 0,
                }
                dividend["securityID"] = ibCashTransaction.attrib["securityID"]
                if dividend["securityID"] == "":
                    dividend["securityID"] = dividend["conid"]
                if companies and dividend["symbol"] in companies:
                    dividend["description"] = companies[dividend["symbol"]]["name"]
                    dividend["taxNumber"] = companies[dividend["symbol"]]["taxNumber"]
                    dividend["address"] = companies[dividend["symbol"]]["address"]
                    dividend["country"] = companies[dividend["symbol"]]["country"]
                    if "reliefStatement" in companies[dividend["symbol"]]:
                        dividend["reliefStatement"] = companies[dividend["symbol"]][
                            "reliefStatement"
                        ]
                """ Convert amount to EUR """
                if dividend["currency"] == "EUR":
                    dividend["amountEUR"] = dividend["amount"]
                else:
                    date = dividend["dateTime"][0:8]
                    currency = dividend["currency"]
                    if date in rates and currency in rates[date]:
                        rate = float(rates[date][currency])
                    else:
                        for i in range(0, 6):
                            date = str(int(date) - 1)
                            if date in rates and currency in rates[date]:
                                rate = float(rates[date][currency])
                                print(
                                    "There is no exchange rate for "
                                    + str(dividend["dateTime"][0:8])
                                    + ", using "
                                    + str(date)
                                )
                                break
                            if i == 6:
                                sys.exit(
                                    "Error: There is no exchange rate for " + str(date)
                                )
                    dividend["amountEUR"] = dividend["amount"] / rate
                dividends.append(dividend)
        for ibCashTransaction in ibCashTransactions:
            if (
                ibCashTransaction.tag == "CashTransaction"
                and ibCashTransaction.attrib["dateTime"].startswith(str(reportYear))
                and ibCashTransaction.attrib["type"] == "Withholding Tax"
            ):
                closestDividend = None
                for dividend in dividends:
                    if (
                        dividend["dateTime"][0:8]
                        == ibCashTransaction.attrib["dateTime"][0:8]
                        and dividend["symbol"] == ibCashTransaction.attrib["symbol"]
                        and dividend["transactionID"]
                        < ibCashTransaction.attrib["transactionID"]
                    ):
                        if (
                            closestDividend is None
                            or dividend["transactionID"]
                            > closestDividend["transactionID"]
                        ):
                            closestDividend = dividend
                if closestDividend:
                    closestDividend["tax"] = -float(ibCashTransaction.attrib["amount"])
                    """ Convert amount to EUR """
                    if ibCashTransaction.attrib["currency"] == "EUR":
                        closestDividend["taxEUR"] = closestDividend["tax"]
                    else:
                        date = ibCashTransaction.attrib["dateTime"][0:8]
                        currency = ibCashTransaction.attrib["currency"]
                        if date in rates and currency in rates[date]:
                            rate = float(rates[date][currency])
                        else:
                            for i in range(0, 6):
                                date = str(int(date) - 1)
                                if date in rates and currency in rates[date]:
                                    rate = float(rates[date][currency])
                                    print(
                                        "There is no exchange rate for "
                                        + str(ibCashTransaction.attrib["dateTime"][0:8])
                                        + ", using "
                                        + str(date)
                                    )
                                    break
                                if i == 6:
                                    sys.exit(
                                        "Error: There is no exchange rate for "
                                        + str(date)
                                    )
                        closestDividend["taxEUR"] = closestDividend["tax"] / rate

    """ Merge multiple dividends or payments in lieu of dividents on the same day from the same company into a single entry """
    mergedDividends = []
    for dividend in dividends:
        merged = False
        for mergedDividend in mergedDividends:
            if dividend["dateTime"][0:8] == mergedDividend["dateTime"][0:8] and (
                dividend["securityID"] == mergedDividend["securityID"]
                or dividend["symbol"] == mergedDividend["symbol"]
            ):
                mergedDividend["amountEUR"] = (
                    mergedDividend["amountEUR"] + dividend["amountEUR"]
                )
                mergedDividend["taxEUR"] = mergedDividend["taxEUR"] + dividend["taxEUR"]
                merged = True
                break
        if merged == False:
            mergedDividends.append(dividend)
    dividends = mergedDividends

    """ Get securities info from IB XML """
    securities = []
    for ibSecuritiesInfo in ibSecuritiesInfoList:
        if ibSecuritiesInfo is None:
            continue
        for ibSecurityInfo in ibSecuritiesInfo:
            if ibSecurityInfo.attrib["conid"]:
                for dividend in dividends:
                    if ibSecurityInfo.attrib["conid"] == dividend["conid"]:
                        dividend["description"] = ibSecurityInfo.attrib["description"]

    """ Generate Doh-Div.xml """
    envelope = xml.etree.ElementTree.Element(
        "Envelope", xmlns="http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"
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
    workflow = xml.etree.ElementTree.SubElement(header, "edp:Workflow")
    if test == True:
        xml.etree.ElementTree.SubElement(workflow, "edp:DocumentWorkflowID").text = "I"
    else:
        xml.etree.ElementTree.SubElement(workflow, "edp:DocumentWorkflowID").text = "O"
    xml.etree.ElementTree.SubElement(envelope, "edp:AttachmentList")
    xml.etree.ElementTree.SubElement(envelope, "edp:Signatures")
    body = xml.etree.ElementTree.SubElement(envelope, "body")
    Doh_Div = xml.etree.ElementTree.SubElement(body, "Doh_Div")
    if test == True:
        dYear = str(reportYear + testYearDiff)
    else:
        dYear = str(reportYear)
    xml.etree.ElementTree.SubElement(Doh_Div, "Period").text = dYear
    xml.etree.ElementTree.SubElement(Doh_Div, "EmailAddress").text = taxpayerConfig[
        "email"
    ]
    xml.etree.ElementTree.SubElement(Doh_Div, "PhoneNumber").text = taxpayerConfig[
        "telephoneNumber"
    ]
    xml.etree.ElementTree.SubElement(Doh_Div, "ResidentCountry").text = taxpayerConfig[
        "residentCountry"
    ]
    xml.etree.ElementTree.SubElement(Doh_Div, "IsResident").text = taxpayerConfig[
        "isResident"
    ]

    dividends = sorted(dividends, key=lambda k: k["dateTime"][0:8])
    for dividend in dividends:
        if round(dividend["amountEUR"], 2) <= 0:
            continue
        Dividend = xml.etree.ElementTree.SubElement(body, "Dividend")
        xml.etree.ElementTree.SubElement(Dividend, "Date").text = (
            dYear + "-" + dividend["dateTime"][4:6] + "-" + dividend["dateTime"][6:8]
        )
        if "taxNumber" in dividend:
            xml.etree.ElementTree.SubElement(
                Dividend, "PayerIdentificationNumber"
            ).text = dividend["taxNumber"]
        if "description" in dividend:
            xml.etree.ElementTree.SubElement(Dividend, "PayerName").text = dividend[
                "description"
            ]
        else:
            xml.etree.ElementTree.SubElement(Dividend, "PayerName").text = dividend[
                "symbol"
            ]
        if "address" in dividend:
            xml.etree.ElementTree.SubElement(Dividend, "PayerAddress").text = dividend[
                "address"
            ]
        if "country" in dividend:
            xml.etree.ElementTree.SubElement(Dividend, "PayerCountry").text = dividend[
                "country"
            ]
        xml.etree.ElementTree.SubElement(Dividend, "Type").text = "1"
        xml.etree.ElementTree.SubElement(Dividend, "Value").text = "{0:.2f}".format(
            dividend["amountEUR"]
        )
        xml.etree.ElementTree.SubElement(
            Dividend, "ForeignTax"
        ).text = "{0:.2f}".format(dividend["taxEUR"])
        if "country" in dividend:
            xml.etree.ElementTree.SubElement(Dividend, "SourceCountry").text = dividend[
                "country"
            ]
        if "reliefStatement" in dividend:
            xml.etree.ElementTree.SubElement(
                Dividend, "ReliefStatement"
            ).text = dividend["reliefStatement"]
        else:
            xml.etree.ElementTree.SubElement(Dividend, "ReliefStatement").text = ""

    xmlString = xml.etree.ElementTree.tostring(envelope)
    prettyXmlString = minidom.parseString(xmlString).toprettyxml(indent="\t")
    with open("Doh-Div.xml", "w", encoding="utf-8") as f:
        f.write(prettyXmlString)
        print("Doh-Div.xml created")


if __name__ == "__main__":
    main()
