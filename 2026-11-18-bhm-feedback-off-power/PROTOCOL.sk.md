# Posun straty pri vypnutej spätnej väzbe

Návrh hlavného merania počíta s 280 nezávislými prípravami v každom z dvoch fyzických nastavení. Kalibrácie a kontroly rušenia sa robia osobitne. Podkladom je simulácia s troma bozónmi v šesťmiestnom prstenci, prípravou |300000⟩ a monitorovaným miestom 1 (indexovanie od nuly). Počas tohto kroku sa získali výpočty sily testu. Hardvérové dáta zatiaľ chýbajú. [Pôvodné predpovede](../2026-11-18-bhm-apparatus-capacity/predictions.json)

## Pred prvým hlavným behom

1. Hardvérovo rozpojiť vetvu od výstupu registra k aktuátoru straty. Nezávisle zaznamenať priebeh na vstupe aktuátora aj pri prepínaní nastavení. Prípravu, pole, geometriu, časovanie a detektor strát ponechať spoločné. Zdokumentovať každý trvajúci fyzický kontakt registra s uzlom.
2. V režime L a H zmerať celú prenosovú maticu registra vrátane nečitateľných symbolov. Pre predpovedané časy musia intervaly kapacity spolu s neistotou referenčnej dynamiky zachovať príslušné prvé prekročenie. Pri nominálnej dynamike sú prípustné intervaly približne od 0,72835 do 0,83101 natu pre L a od 1,00134 do 1,06850 pre H (horný okraj otvorený). Overiť aj pravdepodobnosti kliku pre skutočné kapacity. Kapacity v takomto intervale zaručujú rovnaký časový krok, no sila pulzu aj pravdepodobnosť straty sa v ňom menia.
3. Z nezávislých kalibračných impulzov určiť oneskorenie, rozptyl času, účinnosť a falošné kliky pre obe nastavenia. Zafixovať dve disjunktné okná po korekcii latencie, v jednotkách pôvodnej simulácie [0,375; 0,425) a [0,525; 0,575). Tým sú predpovedané časy v strede okien. Skontrolovať presluch medzi oknami, rozdielne účinnosti, predčasné straty a mŕtvy čas. Ak nie sú zanedbateľné, zahrnúť ich do rozdelenia prvého kliku a rozpočet prepočítať pred hlavným meraním.
4. Na kontrolných kópiách zmerať zmeny tunelovania, interakcie, zahrievania a rozfázovania spôsobené fyzickým zapisovacím impulzom. Kontrolný impulz s rovnakou elektromagnetickou záťažou a neaktívnym zápisom pomáha zmerať presluch. Vypnutie elektronickej spätnej väzby samo nevylučuje bežné spätné pôsobenie pretrvávajúcej disperznej väzby. Dobu odozvy a časový krok 0,05 treba kalibrovať oddelene. Väzobná konštanta sama neurčuje dobu integrácie pri zadanej vernosti.

## Fyzická zmena a párová softvérová kontrola

Vopred náhodne premiešať vyvážené poradie L a H. Zaslepiť vyhodnotenie strát, oddelene archivovať detekciu atómov, symbol registra a identifikátor každého pokusu. Po audite, ešte pred zberom dát, volíme pre primárny výsledok prvý klik v zjednotení oboch okien. Každý pridelený pokus ostáva v menovateli. Ak nemá klik v oknách, rozlišujeme klik výlučne mimo okien a beh bez kliku. Pôvodné pravidlo prvého kliku od času nula vyhodnotíme na rovnakých behoch ako analýzu citlivosti. Fyzická predčasná strata alebo mŕtvy čas detektora môžu zabrániť neskoršiemu kliku pri oboch pravidlách. Zmenu efektívnych pravdepodobností treba zahrnúť do kalibrácie a výpočtu sily. Časové rozlíšenie výsledku určuje šírka okien.

Z archívu H vytvoriť druhú kópiu. Po skončení behu nezávisle pre každý výstupný symbol s pravdepodobnosťou r zameniť symbol za jeden z dvoch ostatných, každý s pravdepodobnosťou 1/2. Pre plánované symetrické matice vyjde 0,99(1−r) + 0,005r = 0,92, teda r = 14/197. Výsledná matica má v očakávaní rovnaké riadky ako L. Pri reálnej asymetrii treba vopred overiť, či existuje stochastická matica K spĺňajúca W_H K = W_L v rámci kalibračnej neistoty. Pre kontrolu uložiť seed a verziu spracovania.

Znova prehnať obe kópie H tým istým vyhodnotením. Každému identifikátoru musí patriť totožný čas a výsledok straty. Odchýlka znamená, že výber pokusov, bránovanie alebo spájanie údajov závisí od softvérového symbolu. H a jeho kópia sú párová kontrola analýzy. Porovnanie L s degradovanou kópiou H má tie isté atómové výsledky a rovnaký menovateľ ako L proti H.

## Primárne rozhodnutie

V skorom okne porovnať podiely na všetky pokusy jednostranným Fisherovým exaktným testom v smere L > H, v neskorom v smere H > L. V oboch musí vyjsť p ≤ 0,05. Ide o jeden spoločný nárok, že platia oba smery. Ak aspoň jeden smer neplatí, pravdepodobnosť nesprávneho potvrdenia oboch je najviac 5 %. Predpokladom sú nezávislé, rovnako distribuované opakovania v každom fyzickom nastavení. Veľkosť vzorky je fixná, bez priebežného zastavovania. Hlásiť absolútne počty, podiely a rozdiely s intervalmi v oboch oknách, plné histogramy a samostatne výsledok kontroly H na tej istej kópii dát. [Definícia jednostranného Fisherovho testu](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html)

## Počet nezávislých príprav

Pôvodný model dáva pravdepodobnosť aspoň jednej straty 0,06113423 v skorom okne L a 0,05448375 v neskorom okne H. Pre model detektora označuje η účinnosť zaznamenania udalosti v správnom okne a b nezávislú pravdepodobnosť falošného kliku v každom okne. Pre signál s pravdepodobnosťou p vyjde v jeho okne s = 1 − (1 − ηp)(1 − b). V L sú pravdepodobnosti prvého kliku v skorom a neskorom okne (s_L, (1−s_L)b). V H sú (b, (1−b)s_H). Tento príklad predpokladá zanedbateľný presun signálu medzi oknami a žiadne konkurenčné prvé kliky mimo nich.

| Scenár detekcie | Minimum na nastavenie | Hlavné behy spolu | Sila pri jednom behu menej na nastavenie | Sila pri minime |
|---|---:|---:|---:|---:|
| Ideálna, η = 1, b = 0 | 157 | 314 | 89,8329 % | 90,1828 % |
| Modelová, η = 0,80, b = 0,005 | 267 | 534 | 89,9515 % | 90,1095 % |

Pre praktický návrh 280 + 280 je modelová sila 91,9663 %. V tomto scenári má L očakávané podiely klikov 5,3663 % a 0,4732 % v skorom a neskorom okne, H má 0,5000 % a 4,8127 %. Výpočet použil presné hypergeometrické kritické hodnoty a podmienenú binomickú sumu cez počty klikov v opačných oknách oboch ramien. Tento postup rešpektuje závislosť spôsobenú započítaním iba prvého kliku. V každom podmieňujúcom rozdelení má vynechaný chvost hmotnosť pod 10⁻¹⁴. Minimum sme určili kontrolou všetkých menších počtov. Nezávislý výpočet Astra 6.2 reprodukoval obidve minimá aj hodnoty sily pri hraničných počtoch. [Reprodukovateľný výpočet pre Python](power.py)

Kladný výsledok lokalizuje časový presun do dvoch predurčených okien. Špecifickosť pre ITHKOR závisí aj od vylúčenia konvenčného rušenia a presnosti predpovede počtov. Nesplnenie oboch testov vyhodnotiť spolu s intervalmi efektu a kalibračnými podmienkami. Pri platnosti navrhovaného modelu a 560 behoch je pravdepodobnosť nesplnenia spoločného kritéria približne 8 %.

## Uzamknutie softvéru a dát

Pred meraním archivovať verziu protokolu a [evaluate.py](evaluate.py), spoločnú latenciu v tikoch a SHA-256 náhodného prideľovacieho kľúča. Kľúč uchová oddelený správca. Ak kalibrácia vyžaduje rôzne latencie alebo inú štatistickú schému, vyžaduje to novú verziu protokolu pred meraním. Analytik dostane súbor JSONL s jedným riadkom na každý pokus, vrátane prázdnych záznamov detektora. Príklad riadka je `{"id":"x001","symbol":2,"click_ticks":[120000,550000],"recorded_until_tick":2500000}`. ID je nepriehľadné, bez príznaku nastavenia. Symbol je 0, 1, 2 alebo `null` pri nečitateľnom registri. Časy sú nezáporné celé tiky od spoločného štartu, milión tikov na časovú jednotku. Posledné pole označuje skutočne zaznamenaný koniec akvizície. Analýza po odčítaní latencie pokrýva čas 0 až 2,5 vrátane. Predpokladá priebežný záznam všetkých klikov, aj po prvom impulze detektora.

V nasledujúcich príkazoch nahradiť hodnoty v lomených zátvorkách vopred zaznamenanými údajmi. SHA-256 je zapísaný malými písmenami. Slepá fáza spracuje identickým postupom originál aj kópiu všetkých pokusov, aby nepotrebovala poznať H. Semeno generátora je súčasťou skriptu. Správca uloží odtlačok výsledného súboru lock.json ešte pred odovzdaním kľúča analytikovi. Na reprodukciu zachovať pôvodné bajty vstupov a súborov, verziu Pythonu a tieto odtlačky oddelene od výstupného adresára.

```text
python evaluate.py freeze --raw trials.jsonl --key-sha256 <sha256-pridelenia> --latency-ticks <latencia> --kind hardware --out lock.json
python evaluate.py report --raw trials.jsonl --key assignments.jsonl --lock lock.json --lock-sha256 <sha256-zaslepeneho-locku> --out report.json
```

Kľúč má pre každý pokus práve jeden riadok, napríklad `{"id":"x001","arm":"H"}`. Skript overí identitu všetkých 560 pokusov, úplnosť deklarovaného záznamu a rozdelenie 280 + 280. Zmenené dáta, nezhodné odtlačky, nadbytočný či chýbajúci pokus alebo už existujúci cieľový súbor zastavia výpočet. Softvérová kontrola porovná dvojice časov a kategórií toho istého pokusu. V reporte zobrazí počet pozmenených symbolov H a ich prechody. Overuje túto linku od vstupného logu po výsledok. Výber vykonaný ešte pred exportom logu potrebuje nezávislý záznam akvizície.

Výsledný JSON obsahuje počty a menovatele, histogramy časov, jednostranné Fisherove p-hodnoty a oba rozdiely podielov s jednotlivo interpretovanými 95 % Newcombovými intervalmi. O primárnom výsledku rozhoduje `primary_first_in_windows.both_directions_pass`. Citlivosť a párová kontrola majú vlastné polia. Podmienka spoločnej nulovej hypotézy všeobecne nedáva pravdepodobnosť falošného potvrdenia 0,25 %. Napríklad pre 280 + 280, bez signálu a so samotným nezávislým pozadím 0,5 % na okno vychádza z multinomickej sumy približne 0,00136 %. [Newcombe, 1998](https://pubmed.ncbi.nlm.nih.gov/9595617/)
