# Pevné záverečné čítanie fluxóniového qubitu

Pri fyzickom oslabení prvého impulzu z 350 na 50 mV záverečné čítanie rozpoznalo pripravený stav o 8,61 percentuálneho bodu častejšie. Na odložených údajoch mala softvérovo zhoršená kópia silného prvého čítania prakticky rovnakú vyváženú vernosť ako fyzicky slabé čítanie. Softvérová zámena prvého symbolu necháva všetky výsledky záverečného čítania silnej vetvy pôvodné.

| Prvý impulz | Vernosť prvého čítania na odložených kalibračných záberoch | Vernosť pevného záverečného čítania |
|---|---:|---:|
| 50 mV | 60,74 % | 70,14 % |
| 350 mV | 85,52 % | 61,53 % |
| 350 mV so softvérovým zhoršením | 60,92 % | 61,53 % |

Vernosť je priemer podielov správnych výsledkov pre dve rovnako zastúpené prípravy. Rozdiel v poslednom stĺpci má vnútrosériový 95 % interval 8,23 až 9,00 bodu. Pri príprave 0 dosiahlo slabé a silné budenie 86,00 % a 67,21 %, pri príprave 1 dosiahli 54,28 % a 55,85 %. V samostatných kontrolách s vynechaným prvým impulzom bol rozdiel medzi príslušnými blokmi 0,52 bodu. Po jeho odčítaní vychádza 8,09 bodu s intervalom 7,52 až 8,67.

## Čo bolo merané

Pred otvorením výsledkov sme zvolili publikovaný pracovný bod 140 mV toku a 350 mV budiacej amplitúdy a najnižšiu dostupnú amplitúdu 50 mV pri tom istom toku. Ide o napäťové nastavenia generátora. Prvý impulz trval 2 µs. Po ňom nasledovalo 3 µs čakania na vyprázdnenie rezonátora. Záverečný verifikátor používal v oboch vetvách rovnakých 350 mV, 1 µs dĺžku a 2 µs integráciu. Vybrali sme vetvu bez záverečnej operácie X. Astra 6.2 overila nastavenia aj v surových prístrojových záznamoch. [Predtlač, obr. 2 až 4](https://arxiv.org/html/2606.17866v1) · [Verejné dáta, verzia 2](https://data.4tu.nl/datasets/22122209-2f78-4a66-8d04-fe18ac8b244e/2)

Prvý impulz charakterizovali autori 25. apríla 2026. V samostatnom behu 1. mája aplikovali jeho fyzický ekvivalent a uložili výsledok verifikátora. Preto je možné vyhodnotiť rozdelenie druhého výsledku podľa prípravy a sily prvého impulzu. Archív pri týchto behoch neposkytuje spoločné rozdelenie dvoch zaznamenaných symbolov ani pravdepodobnosť druhého výsledku podmienenú prvým. Zladenie používa predpoklad prenositeľnosti aprílovej kalibrácie na májové nastavenie.

## Výpočet a nezávislá kontrola

Načítali sme sedem pôvodných HDF5 súborov z verejného ZIP archívu pomocou bajtových rozsahov. Skontrolovali sme mená, CRC32, číslovanie príprav a opakovaní. Pre každý výkon má prvá aj druhá séria 65 536 záberov na každú prípravu. Pri prvom čítaní sme na štvrtine opakovaní určili os v IQ rovine a jej deliaci prah. Na druhej štvrtine sme vypočítali stochastickú maticu K spĺňajúcu W₃₅₀ K = W₅₀. Pri silnom čítaní vymení symbol 0 za 1 s pravdepodobnosťou 38,41 % a symbol 1 za 0 s pravdepodobnosťou 30,86 %. Tabuľka dáva očakávanú vernosť tejto transformácie na dovtedy nepoužitej polovici záberov. Pre prípravy 0 a 1 sa podiel správnych prvých odpovedí v zhoršenej vetve líšil od slabej fyzickej o +0,52 a −0,16 bodu. Samostatné opisné zladenie oboch chybovostí priamo na odloženej vzorke dá presne 60,74 % v oboch vetvách. Pri oboch postupoch zostáva záverečný výsledok rovnaký.

Pre všetky májové série sme použili jediný dekodér natrénovaný na nezávislej referenčnej kalibrácii verifikátora z 29. apríla. Intervaly používajú 10 000 bootstrapových výberov blokov po 256 po sebe idúcich dvojiciach príprav v každej akvizícii. Odhadujú neistotu v dostupných súboroch. Dlhodobý drift medzi dátumami a reprodukovateľnosť na inom čipe ostávajú otvorené. Nezávislé spracovanie Astra 6.2 pomocou publikovaných tabuliek autorov dalo rozdiel 8,59 bodu, po kontrole s vynechaným impulzom 8,06 bodu. [Nezávislý výpočet](delft_notes.md)

Výsledok zachytáva rozdiel v klasickom výstupe pevného verifikátora po mikrovlnnom budení. Dekodér má dva výstupy a môže vyššie hladiny priradiť jednej z dvoch tried. Jeden čas čítania a samostatná kalibrácia prvého pulzu neumožňujú určiť okamih straty, izolovať vplyv kapacity od fyzickej sily impulzu ani priradiť rozdiel mechanizmu ITHKOR.

Na reprodukciu stačí spustiť `python raw_check.py` s knižnicami NumPy, h5py a requests. [Výpočet zo surových dát](raw_check.py) · [Výsledné matice a intervaly](raw_results.json)
