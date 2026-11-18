# Dve po sebe idúce čítania supravodivého qubitu

Pri zvýšení nastavenia výkonu z −21 na −15 dBm sa na odložených záznamoch zlepšilo rozpoznanie pripravovaného stavu prvým čítaním z 87,6 % na 92,0 %. Druhé čítanie súhlasilo s prípravou pri 420 z 500 a 417 z 500 pokusov. Pri softvérovom zhoršení prvého čítania zostal druhý výsledok každého z 500 pokusov totožný.

| Nastavenie | Prvé čítanie súhlasí s prípravou | Druhé čítanie súhlasí s prípravou | Čítania navzájom nesúhlasia |
|---|---:|---:|---:|
| Fyzicky −21 dBm | 87,60 % | 84,00 % | 17,20 % |
| Fyzicky −15 dBm | 92,00 % | 83,40 % | 11,00 % |
| −15 dBm, zhoršenie podľa nezávislej kalibrácie | 85,33 % | 83,40 % | 17,36 % |
| −15 dBm, presné opisné zladenie na odložených prvých čítaniach | 87,60 % | 83,40 % | 15,71 % |

## Vstupy a analýza

Použitý archív má publikovaný MD5 `ced1ed4af893ad064045900903e19a17`. Súborom k 7a zodpovedá 20 nastavení výkonu, dve prípravy a 40 000 jednotlivých IQ vzoriek na súbor. Súbory k 7b obsahujú 13 nastavení s oboma prípravami a 501 párov stôp na prípravu a výkon. Štyri pomocné súbory označené „test“ sú mimo analýzy. Počty 501 v štandardných súboroch zodpovedajú rozmerom polí a pôvodnému notebooku. Ide o súbory z rozdielnych akvizícií. Medzi 7a a 7b sme nespájali jednotlivé pokusy. [Dáta a notebooky autorov](https://zenodo.org/records/8004359) · [Hassani a kol., opis dvoch čítaní](https://pmc.ncbi.nlm.nih.gov/articles/PMC10323121/)

Pred výpočtom porovnávaných výsledkov sme vybrali nastavenia zo súborov označených −21 a −15, zaznamenané v ten istý deň. Každá príprava a výkon má v párovom porovnaní jednu akvizíciu. Z prvého IQ kanála sme spriemerovali vzorky 22–32 a 41–51 vrátane (číslovanie od 1 podľa výpočtu prahov v notebooku autorov). Pre každé nastavenie sme na prvom čítaní natrénovali rozdelenie podľa bližšieho z dvoch priemerov v IQ rovine a ten istý dekodér použili aj na druhý impulz. Menovateľ zahŕňa všetky odložené riadky vrátane vzájomne nesúhlasných čítaní. Triedy označujú zamýšľanú prípravu g/e. Dekodér rozlišuje dve triedy, pričom prípadný únik na inú hladinu môže priradiť jednej z nich.

V každom súbore sme riadky číslovali od nuly. Zvyšok po delení štyrmi 0 označuje trénovanie, 1 kalibráciu softvérového zhoršenia a 2 alebo 3 záverečné vyhodnotenie. V párovej sérii tak vyšlo 126, 125 a 250 riadkov na prípravu. V samostatnej sérii 7a vyšli odložené vernosti 89,76 % a 91,56 %, pričom empirické prenosové kapacity binárneho dekodéra boli 0,3640 a 0,4099 natu na použitie. Všetky výkonové krivky, matice zámen a počty párov podľa prípravy sú vo výslednom JSON. Hodnoty kapacity sú odhady zo vzorky pre daný dekodér.

## Čo znamená dosiahnuté zladenie

Na kalibračných riadkoch sme našli stochastickú maticu K, ktorá spĺňa WₕK = Wₗ. Pravdepodobnosť preklopenia prvého výsledku g → e je 8,76 %, opačným smerom 7,13 %. V tabuľke sú očakávané hodnoty softvérového zhoršenia, vypočítané priamo cez obe možnosti zmeny symbolu. Druhé čítanie ostáva zachované na úrovni každého pokusu. Na odložených riadkoch zostal pri prvom čítaní rozdiel −2,27 percentuálneho bodu voči fyzickému nízkemu výkonu. Pri nezhode medzi čítaniami dosiahol rozdiel +0,16 bodu (95 % interval −3,85 až +4,13 bodu).

Na opisné porovnanie pri presne rovnakej vernosti sme dodatočne zladili obe podmienené chybovosti prvého čítania priamo na vyhodnocovaných riadkoch. Táto matica používa prvý výsledok a prípravu, pričom k druhému výsledku pri odhade nepristupuje. Dáva pravdepodobnosti zmeny 8,42 % a 2,06 %. Získaná nezhoda 15,71 % je o 1,49 bodu nižšia ako fyzicky nameraných 17,20 %. Toto opisné zladenie neposkytuje ďalšiu nezávislú skúšku prenositeľnosti matice.

## Druhý výsledok a obmedzenia

Pri príprave g sa druhé čítanie klasifikovalo ako e v 23/250 prípadoch pri −21 dBm a 17/250 pri −15 dBm. Pri príprave e vyšlo e v 193/250 a 184/250 prípadoch. Súhrnný rozdiel v správnom rozpoznaní prípravy pri druhom čítaní je −0,60 bodu (95 % interval −5,0 až +4,0). Intervaly pochádzajú z 20 000 bootstrapových prevzoriek párov, osobitne podľa výkonu a prípravy, s pevným dekodérom aj maticou zhoršenia. Nezahŕňajú neistotu medzi akvizičnými sériami ani pomalý drift.

Pri fyzickej zmene výkonu sa menia oba čítacie impulzy. Rozdiel druhého výsledku preto môže obsahovať chybu druhého čítania, relaxáciu, rušenie prvým impulzom aj drift. Priemerná nezhoda prvého a druhého výsledku sama neurčuje pravdepodobnosť fyzického skoku medzi hladinami. Tento dvojstavový súbor pri jednom časovom odstupe neposkytuje čas nástupu straty v Boseho–Hubbardovom prstenci.

## Reprodukcia

```text
python analyze.py "Source Data _ full_version.zip" > results.json
```

Výpočet bol vykonaný s Pythonom 3.12, NumPy 2.5.5 a SciPy 1.18.1. Nezávislá analýza Astra 6.2 reprodukovala počty, kalibračnú maticu a nezhody v hlavnom porovnaní.
