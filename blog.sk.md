# Kto zavrel dvere v kvantovom prstenci?

O 0,74 sa oplatí pozrieť na dvere. O chvíľu neskôr už bude v oboch prípadoch zavreté a z pohybu za dverami sa bude ťažko hádať, kto ich zatvoril. K tomuto zvláštnemu času sme sa dostali pri otázke, ktorú kladie ITHKOR: čo by sme videli, keby množstvo kvantovej informácie v malej oblasti malo fyzický strop?

## Pasca pre našu obľúbenú myšlienku

V počítači sme postavili šesť jamiek do kruhu a vložili do nich tri častice. Medzi susednými jamkami môžu preskakovať. Sledujeme dve jamky vedľa seba. Jeden z variantov hypotézy v8 hovorí, že keď ich previazanie so zvyškom prstenca dosiahne určenú hranicu, dva východy z dvojice sa zatvoria. Medzi oboma jamkami sa častice môžu pohybovať ďalej.

Háčik je v tom, aké ľahké je taký výsledok napodobniť. Stačí dať k východom obyčajný časovač. Keď poznáme začiatok pokusu, vieme mu nastaviť presne ten okamih, v ktorom majú podľa hypotézy zavrieť.

Preto sme začiatok ponechali rovnaký. Až počas behu sme v jednej verzii posunuli fázu kvantovej vlny o štvrť obrátky jedným smerom, v druhej opačným. Pre ostré zatvorenie a strop 1,036 natu sme vopred vypočítali, že hranica sa má zatvoriť v čase **0,7163** alebo **0,7634**. Časovač, ktorý sa o neskoršej voľbe nedozvie, má pre oba prípady stále iba jeden čas. Čísla sú v jednotkách určených rýchlosťou preskoku medzi jamkami.

## Ako nás časovač takmer oklamal

Najprv sme štyrikrát merali prúd *medzi dvoma jamkami*. Časovač nastavený na 0,758 sa podobal prahu tak dobre, že aj s 8 000 simulovanými meraniami na rozhodnutie sme správnu príčinu uhádli iba v **53,9 %** prípadov. Hoci sa východy zatvárali v rôznom čase, pohyb vnútri tento rozdiel prezrádzal len slabo.

Potom sme sa pozreli tam, kde sa obe vysvetlenia rozchádzajú. V čase **0,74** majú byť po jednom impulze východy zavreté a po druhom ešte otvorené. Na oddelených kópiách sme spočítali častice v dvojici tesne pred týmto okamihom a tesne po ňom. Simulácia zahŕňala náhodnosť kvantových výsledkov a predpokladala bezchybné odčítanie. Pri rovnakom rozpočte stúpla úspešnosť proti tomu istému časovaču na **86,1 %**. Keď sme dovolili časovaču vopred vybrať nový čas aj pre tento spôsob merania, zostalo **77,4 %**. Iné nastavenie môže dopadnúť aj horšie. [Výpočet a výsledky](https://github.com/thegobi/ithkor-feedback-off/blob/v8.0.0/2026-11-19-bhm-boundary-probe/REPORT.sk.md)

## Čo môže urobiť laboratórium

V8 dáva experimentátorom aj druhú možnosť. Vedľa prstenca umiestnia register s tromi rozlíšiteľnými stavmi a fyzicky odpoja spätnú väzbu. Ak práve kapacita tohto registra určuje strop, zlepšenie jeho čitateľnosti z 92 % na 99 % má posunúť nástup možnej straty častice z 0,40 na 0,55. Únik očakávame iba v malej časti behov. Preto sme zverejnili presný plán 560 hlavných opakovaní aj postup, ako výsledky vyhodnotiť naslepo. [Laboratórny protokol](https://github.com/thegobi/ithkor-feedback-off/blob/v1.0.0/2026-11-18-bhm-feedback-off-power/PROTOCOL.sk.md)

Na skutočnom čipe sa dá pomýliť už v tom, čo vlastne meranie pokazilo. V dátach z TU Delft sme softvérovo zhoršili výsledok silnejšieho prvého čítania, až bol približne taký čitateľný ako výsledok slabšieho. Pri pevnom druhom čítaní medzi nimi aj tak zostal rozdiel 8,61 percentuálneho bodu. Tento údaj ukazuje, prečo treba kontrolovať aj fyzický účinok impulzu. Čip v Delfte skúšal iné usporiadanie a otázka stropu v prstenci zostáva otvorená. [Rozbor dát TU Delft](https://github.com/thegobi/ithkor-feedback-off/blob/v1.0.0/2026-11-18-fixed-verification/REPORT.sk.md)

V rukách tak máme čas, miesto a postup merania aj čísla, pri ktorých priznáme neúspech. Pri meraní vnútorného prúdu sme si napríklad žiadali, aby aj dolná hranica odhadu úspešnosti presiahla 70 % pre každé z dvoch vysvetlení. Proti preladenému časovaču tento test nevyšiel. Stále nevieme, čo by v jedinom prstenci zistilo, že dosiahol strop, ani kam by pri zatvorení prešla energia. Obe otázky ostávajú vo v8 otvorené. Pri hraničnej sonde je prvý krok prostý: spočítať, koľkokrát prístroj ohlási presun, keď experimentátor vie, že dvere boli celý čas zavreté. [Prečítať ITHKOR v8](https://ithz.dev/downloads/ithkor-v8/sk.html) · [Kód a údaje k reprodukcii](https://github.com/thegobi/ithkor-feedback-off/releases/tag/v8.0.0)
