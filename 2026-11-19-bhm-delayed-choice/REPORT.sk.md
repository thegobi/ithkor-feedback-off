# Predpoveď prahu po neskorom fázovom impulze

Obe vetvy začínajú v rovnakom stave 210000, s tým istým prstencom a stropom 1,035679 natu. Až v čase 0,30 sa zvolí fáza +π/2 alebo −π/2 na uzle 0. Impulz zachová počet častíc a okamžitú entropiu dvojice. Zmení ďalší priebeh previazania. Môže tiež zmeniť energiu a prúd. Preto každý mechanizmus vrátane otvorenej referencie dostane rovnaký impulz príslušného znamienka. Simulujeme obe možné voľby, náhodnosť v testovacích dátach pochádza z jednotlivých meraní prúdu.

| Fázový impulz | Kalibrácia časovača pre 210000 | Predpovedané zatvorenie na strope | Oneskorenie |
|---|---:|---:|---:|
| +π/2 | 0,60430 | 0,71634 | 0,11204 |
| −π/2 | 0,60430 | 0,76344 | 0,15914 |

Ide o časy v inverzných jednotkách vnútorného preskoku. Uzatvárajú sa len hrany 1–2 a 5–0. Impulz je pre časovač neskorou voľbou. Znamienko pozná vyhodnocovateľ, ktorý používa príslušnú modelovú referenciu a predlohu. Predpovede boli lokálne uložené pred vzorkovaním šumu. Model umelej inteligencie Astra 6.2 nezávisle potvrdil všetky tri časy aj osem rozdielov prúdu oproti kalibrovanému časovaču.

| ΔJ prahu mínus ΔJ kalibrovaného časovača | 0,75 | 1,00 | 1,50 | 2,50 |
|---|---:|---:|---:|---:|
| +π/2 | −0,00140 | +0,00036 | −0,01110 | −0,01826 |
| −π/2 | −0,03694 | −0,03642 | +0,03212 | +0,06168 |

Jedno rozhodnutie stálo **8 000 nezávislých kópií spolu** (dve znamienka × štyri časy × 1 000). Presné teoretické šablóny a otvorená referencia nečerpajú z rozpočtu. Pre každú pravú príčinu je v každom porovnaní 2 000 simulovaných rozhodnutí. Intervaly nižšie sú simultánne korigované Wilsonove intervaly pre jednotlivé triedy. Vyjadrujú len neistotu zo simulovaného vzorkovania.

| Kandidát na časovač | Správne, ak platí prah | Správne, ak platí časovač | Vyvážená úspešnosť |
|---|---:|---:|---:|
| Z kalibrácie pred impulzom, 0,60430 | 1607/2000 (78,04–82,47 %) | 1604/2000 (77,88–82,33 %) | 80,28 % |
| Jeden spoločný čas vybraný tak, aby čo najlepšie napodobnil prúdy, 0,758 | 1082/2000 (51,31–56,87 %) | 1075/2000 (50,96–56,52 %) | 53,93 % |

Spoločný čas 0,758 bol vybraný z 2 501 možností pri znalosti presných prahových predpovedí a oboch možných zásahov. Pri jeho voľbe sa nepoužili náhodné výsledky meraní ani skutočne zvolené znamienko. Minimalizácia bola vzhľadom na osem stredných prúdov a váhy určené prahovým modelom. Tento čas nie je univerzálne optimálny pre všetky pozorovateľné veličiny. Pri teste s ním nepresahuje absolútny rozdiel ôsmich stredných prúdov 0,00659. Časy samotných prahových zásahov sa od seba líšia o 0,04710; meranie prúdu nie je priamym meraním okamihu zatvorenia. Porovnanie vyradí kalibráciu 0,60430 podľa stanoveného kritéria precíznosti, ale pri tejto štatistike a rozpočte nedokáže spoľahlivo odlíšiť prah od vhodne zvoleného spoločného času. Časovač s prístupom k neskorému znamienku môže použiť dve rôzne hodnoty a reprodukovať prahové trajektórie presne.

Ide o test dvoch modelov s projektívnym šumom a známym Hamiltoniánom. Nevykonali sme laboratórne meranie, odhad kalibračnej chyby ani dôkaz samotného postulátu ITHKOR. Reprodukcia v tomto adresári vyžaduje NumPy a existujúce modely prstenca v projekte. `python late.py` vypíše predpovede a `python score.py` overí kontrolné súčty a zopakuje simuláciu.

**Recenzia modelom umelej inteligencie Fable 5.2.** Recenzent dostal protokol, predpovede, kód, výsledky a zhrnutie predošlého testu zmeny prípravy. Potvrdil interpretáciu neúspechu voči silnejšiemu časovaču a výpočet korekcie intervalov. Malý zvyškový signál je pri veľkom počte simulácií rozpoznateľný; pre jedno rozhodnutie zostáva hlboko pod dohodnutou úspešnosťou. Referencia sa pri porovnaní oboch predlôh algebraicky vyruší. Kontrola bez impulzu potvrdzuje konzistenciu kódu. Posudok tiež upozorňuje, že sme nevylúčili náhodné časovače ani regulátor s prístupom k fáze. Úplné znenie je vo fable-review.json.
