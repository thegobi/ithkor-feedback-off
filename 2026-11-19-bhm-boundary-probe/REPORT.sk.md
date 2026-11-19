# Okno medzi dvoma časmi uzavretia

V ostrom prahovom modeli sa pri pôvodnej príprave 210000 po fázovom impulze +π/2 zatvoria hrany 1–2 a 5–0 v čase 0,716338. Po −π/2 sa zatvoria v čase 0,763439. V čase 0,74 je teda hranica uzavretá iba v prvej vetve. Spoločný deterministický časovač bez znalosti znamienka dá pri oboch znamienkach ten istý stav prepínača. Preladený spoločný časovač nastavený na 0,758 má obe hranice ešte otvorené. Test nemenil impulz ani prípravu.

## Tok a neinvazívny odhad jeho priemeru

Pre N_R = n₀ + n₁ a H = H_cut + fV platí d⟨N_R⟩/dt = f ⟨i[V,N_R]⟩. Kladný tok smeruje do oblasti. Hodnotu sme overili aj centrálnou diferenciou časového priebehu. Nulový tok všeobecne nedokazuje nulovú väzbu; v týchto konkrétnych otvorených vetvách je tok dostatočne odlišný od nuly. Výpočet operátora s dosadeným f nie je nezávislým prístrojovým meraním koeficientu. Preto sme skórovali iba údaje získateľné tým istým číselným meraním N_R pre všetky hypotézy.

| Model | Tok v 0,74 po + | Tok v 0,74 po − | Δ⟨N_R⟩ cez [0,72; 0,76] po + | Δ⟨N_R⟩ po − |
|---|---:|---:|---:|---:|
| Prah | 0 | −0,97570 | 0 | −0,03902 |
| Časovač 0,758 | −1,09426 | −0,97570 | −0,04153 | −0,03702 |
| Stále otvorené | −1,09426 | −0,97570 | −0,04376 | −0,03902 |

Model umelej inteligencie Astra 6.2 nezávisle potvrdil všetky hodnoty tabuľky. Na nezávislých kópiách stačí merať počet častíc v dvoch časoch a vytvoriť rozdiel priemerov. Pri 8 000 prípravách aj odčítaniach na jedno rozhodnutie bolo správnych 1730/2000 pre prah a 1715/2000 pre časovač 0,758, vyvážená úspešnosť 86,13 %. Dodatočný nepriaznivý časovač 0,7381 zvolil jediný spoločný čas tak, aby napodobnil oba priemerné úbytky (mriežka 0,00005, štvorcové vzdialenosti vážené varianciou prahovej predlohy). Na nových simulovaných meraniach vyšla úspešnosť 77,43 % (1546 a 1551 z 2000). Je to konkrétny alternatívny časovač, bez tvrdenia o najhoršej možnej úspešnosti pasívnej klasifikácie.

## Dve odčítania tej istej kópie

Ako silnejší predpoklad sme zaviedli dokonalé opakovateľné odčítanie N_R bez rozlíšenia, na ktorom uzle sú častice. Ak je hranica zatvorená, nasledovné vnútorné preskoky tento počet nemôžu zmeniť. Ak je otvorená, pravdepodobnosť iného výsledku v druhom meraní počítame s projekciou po prvom odčítaní. Pre otvorenú zápornú vetvu sme skontrolovali entropiu po projekcii až do druhého odčítania. Na mriežke 0,00005 zostali maximá jednotlivých podmienených vetiev (0,68838) aj nepodmieneného súboru (0,97404) pod C = 1,03568. Uzavretá kladná vetva zostáva uzamknutá podľa pôvodného postulátu. Meranie je deštruktívne pre koherencie medzi rôznymi počtami, ale nezničí samotnú kópiu. Zmena počtu medzi odčítaniami je signálom čistého presunu; spätný preskok počas okna môže zostať nezachytený.

| Pravdepodobnosť odlišných počtov v dvoch čítaniach | +π/2 | −π/2 |
|---|---:|---:|
| Prah | 0 | 0,2520 % |
| Časovač 0,758 | 0,2372 % | 0,2276 % |

Pravidlo označí prah, keď pre plus nezaznamenáme žiadnu zmenu a pre mínus aspoň päť. Pri 2000 kópiách na znamienko (8000 odčítaní) má citlivosť 56,68 %. Pri 3170 kópiách na znamienko (6340 kópií, 12 680 odčítaní) má citlivosť 90,005 %. Počet 3170 sme dopočítali po primárnom teste, zo stanoveného pravidla a požiadavky aspoň 90 %. Je to nárok tohto pravidla v ideálnom modeli.

Pre ľubovoľný jeden spoločný pevný čas je pravdepodobnosť falošného poplachu v druhom prípade najviac 0,87 %. Pre časy pred 0,72 sú obe pravdepodobnosti zmeny nulové. Po 0,76 sú obe dané stále otvoreným vývojom. Vnútri okna, po prvom odčítaní, stačí vyvinúť projekčné vetvy otvoreným Hamiltoniánom do času prepnutia, keďže zvyšný vývoj zachová N_R. Pre kontrolu medzi bodmi mriežky sme použili |√p(t) − √p(t′)| ≤ ‖H_open‖ |t−t′|. Je to trojuholníková nerovnosť pre normu amplitúd zmeneného počtu po unitárnom vývoji. Pre každý bod mriežky sme binomickú pravdepodobnosť poplachu zhora ohraničili zmenšením p₊ a zväčšením p₋ o príslušnú rezervu v odmocninách. Hranica predpokladá nezávislé identické prípravy, rovnaký pevný čas pre všetky kópie a známe modelové parametre.

**Praktická hranica.** V rozpočte nie sú chyby odčítania, nesprávna príprava ani časový rozptyl pulzov. Nulová tolerancia zmien v kladnej vetve robí druhý test zvlášť citlivý na falošné zmeny počtu. Druhé odčítanie v 0,76 leží len 0,00344 časovej jednotky pred pôvodným záporným prahom. Časovač poznajúci znamienko môže prah napodobniť. Výsledky rozlišujú pravidlá v simulácii. Fyzikálna existencia entropického spínača zostáva otvorená.

Reprodukcia: `python probe.py`. Skript používa NumPy a súbory predchádzajúceho testu. Presné hodnoty poskytuje `results.json`.
