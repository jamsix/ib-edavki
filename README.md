# InteractiveBrokers -> FURS eDavki konverter
_Skripta, ki prevede XML poročilo trgovalnih poslov v platformi InteractiveBrokers v XML format primeren za uvoz v obrazca Doh-KDVP in D-IFI v eDavkih Finančne uprave_

Poleg pretvorbe vrednosti skripta naredi še konverzijo iz tujih valut v EUR po tečaju Banke Slovenije na dan posla.

## Uporaba

### Izvoz poročila v platformi InteractiveBrokers

1. V meniju **Reports** odpri **Flex Queries**
1. Na desni strani ob **Custom Flex Queries** klikni ikono za konfiguracijo (Configure).
1. V **Activity Flex Query Templates** klikni **+** (Create).
1. Vpiši poljuben **Query Name**.
1. Kot **Date Period** izberi **Custom Date Range**.
1. Izberi najstarejši mogoč **From Date** in najnovejši mogoč **To Date**.
1. Pod **Sections** klikni na **Trades**.
1. Pod **Options** označi **Executions** in **Closed lots**.
1. Odkljukaj vse parametre na seznamu.
1. Vse ostale nastavitve pusti tako kot so.
1. Na dnu klikni **Save**
1. Na dnu klikni *Continue* in nato *Create*.
1. V pogledu **Reports > Flex Queries** se je pojavil novo narejeni report. Klikni **Run**, shrani XML.

### Konverzija IB poročila v popisne liste primerne za uvoz v eDavke

Na računalniku imej **python 2.x**.

```
./ib-edavki.py [-h] [-y report-year] [-t] ib-xml-file
```

Skripta po uspešni konverziji v lokalnem direktoriju ustvari dve datoteki:
* Doh-KDVP.xml (datoteka namenjena uvozu v obrazec Doh-KDVP - Napoved za odmero dohodnine od dobička od odsvojitve vrednostnih papirjev in drugih deležev ter investicijskih kuponov)
* D-IFI.xml (datoteka namenjena uvozu v obrazec D-IFI - Napoved za odmero davka od dobička od odsvojitve izvedenih finančnih instrumentov)

#### -y <leto> (opcijsko)
Leto za katerega se izdelajo popisni listi. Privzeto trenutno leto.

#### -t (opcijsko)
eDavki ne omogočajo dodajanje popisnih listov za tekoče leto, temveč le za preteklo. Parameter *-t* spremeni datume vseh poslov v preteklo leto, kar omogoča uvoz popisnih listov in **informativni izračun davka** že za tekoče leto. Konverzija iz tuje valute v EUR je kljub temu opravljena na pravi datum posla.

**Pozor: namenjeno informativnemu izračunu, ne oddajaj obrazca napolnjenega s temi podatki!**

### Uvoz v eDavke
1. V meniju **Dokumenti > Nov dokument** izberi obrazec Doh-KDVP (za trgovanje z vrednostnimi papirji na dolgo) ali D-IFI (za trgovanje z vrednostnimi papirji na kratko in trgovanje z izvedenimi finančnimi inštrumenti).
1. Izbira obdobja naj bo lansko leto.
1. Vrsta dokumenta naj bo **O**. Če si za preteklo leto že oddal obrazec, pa želiš le testno narediti izračun davka za tekoče leto, izberi **I**.
1. Izberi **Nov prazen dokument**.
1. Klikni **Uvoz popisnih listov** in izberi ustrezno datoteko (normal.xml za obrazec Doh-KDVP, derivate.xml za obrazec D-IFI) in klikni **Uvozi**.
1. Na seznamu popisnih listov se bo pojavil po en popisni list za vsak vrednostni papir (ticker).
1. Klikni na ime vrednostnega papirja in odpri popisni list.
1. Klikni **Izračun**.
1. Preveri če vse pridobitve in odsvojitve ustrezajo dejanskim. Zaloga pri zadnjem vnosu mora biti **0**.
