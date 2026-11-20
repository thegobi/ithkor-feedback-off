# Kedy zostanú atómy za hranicou?

**ITHKOR-B-SPACED-1.0.0 · 20. november 2026 · návrh testu pred meraním na hardvéri.** Vo výsledkoch nižšie sa každý údaj o pohybe atómov získal simuláciou. Voľbu dvojice aj hlavného času sme urobili so znalosťou simulácie. Na skutočnej aparatúre sa dá predpoveď preveriť zaslepeným porovnaním.

Do prvého zo šiestich miest prstenca dáme tri atómy. Medzi prvými dvoma miestami a zvyškom vedú dve spojenia. Po každej prestávke register nakrátko zapíšeme a odpojíme. V jednej skupine rozlišuje tri kalibračné symboly s vernosťou 92 % (L), v druhej s 99 % (H). Výsledok zápisu počas pokusu nič neriadi. Po treťom zápise urobíme jednu snímku a spočítame atómy na prvých dvoch miestach. Aj prázdna dvojica je platný výsledok.

| Nastavenie | Prvé zatvorenie podľa návrhu | Počet v dvojici po 3. zápise | Po 4. zápise |
|---|---:|---:|---:|
| L, register celej dvojice | 0,90 | 2,59195 | 2,59195 |
| H, register celej dvojice | 1,35 | 2,41511 | 2,41511 |
| Trvalo otvorené spojenia, L aj H | žiadne | 2,41511 | 2,25323 |

V slabšie čitateľnom registri by sa hranica zavrela skôr a v dvojici by v priemere zostalo o **0,17684 atómu viac**. Štvrtá snímka na nových prípravách má vlastný význam. Až po nej sa predpoveď pre H od otvoreného prstenca líši o 0,16188 atómu. Samotná dvojica konečných priemerov neurčuje čas zatvorenia jednoznačne.

## Fyzikálny model a nové postuláty

Šesťuzlový Boseho–Hubbardov prstenec, tri bozóny, počiatočný stav |300000⟩. R tvoria uzly 0 a 1. Jednotky sú ℏ = Jᵢₙ = 1. Interakcia U = 0,35, hraničné preskoky na väzbách 1–2 a 5–0 sú 0,65, ostatné 1. Zachovávame ostré a trvalé odpojenie oboch väzieb aj celkový počet troch častíc. V primárnom teste nie je fázový impulz. Okamžitá zmena strednej energie samotného prstenca pri odpojení je −0,03477 v L a −0,03160 v H, v jednotkách Jᵢₙ. Zdroj alebo zásobník tejto práce ostáva fyzikálne otvorená otázka.

Po prestávke d = 0,40 nasleduje zápis šírky τ = 0,05 do čerstvého qutritu v rovnomernej superpozícii. Obe miesta sú naraz rovnako spojené s **jedným** registrom cez g(n₀+n₁)⊗diag(0,1,2). Počas zápisu tunelovanie pokračuje. Plocha gτ = 2π/3. Nevymieňame výkon pulzu medzi L a H. Mení sa iba odfázovanie registra v báze jeho interakcie, s κτ = 0,127833372 a 0,015113638. Pri pevnom počte splývajú symboly pre 0 a 3. Konečný detektor musí samostatne rozlíšiť skutočné počty. Používame prirodzené logaritmy.

**Nové predpoklady** sú priradenie kapacity tohto spoločného registra celej dvojici a skúšanie prahu iba na konci zápisu. Za kapacitu berieme Shannonovu kapacitu symetrického kanála pre tri pevné kalibračné vstupy, 0,764391 alebo 1,035679 natu na zápis. Pri prvom konci zápisu s S(ρᴿ) > C uzavrieme obe väzby. S počítame z nepodmieneného súboru príprav. Register spôsobuje zmiešanie, preto táto entropia zahŕňa aj klasickú neistotu. Predpis má nelineárnu závislosť od stavu súboru. V laboratóriu sa skutočné uzavretie má prejaviť spontánne, bez výpočtu entropie a bez príkazu aktuátoru.

Na otvorenej dráhe má S po prvých troch zápisoch hodnoty 0,54642, 0,84743 a 1,07007 natu. Diskrétne pravidlo dovolí prekročiť strop. Po uzavretí je rozdelenie Nᴿ nemenné. V kolektívnom modeli register po uzavretí pôsobí rovnako na všetky konfigurácie daného počtu, takže ďalší zápis zachová aj spektrum ρᴿ. Pri spojitom pravidle v8 s kapacitou aktívnou aj počas prestávky vychádzajú prvé prechody pri 0,79037 a 1,27775 a rozdiel 0,20896 atómu. Ide o numerické korene s rovnakým výsledkom pri dvoch hustotách mriežky.

## Čo predpovedá bežná fyzika

Pri rovnakom Hamiltoniáne a odpojenej spätnej väzbe diagonálne bloky spoločného stavu v báze registra prechádzajú tromi podmienenými unitárnymi vývojmi. Čisté odfázovanie registra pôsobí iba na mimodiagonálne bloky. Po sčítaní diagonálnych blokov má prstenec v oboch ramenách úplne rovnaký stav v každom čase. Absolútny pohyb atómov pritom samotný zápis výrazne mení. Táto presná nula medzi ramenami vyžaduje rovnaké fyzické pulzy, väzby, prípravu aj zvyšný šum. 

Ak register ponecháme len na uzle 1 ako vo Vetve A, už prvý zápis prekročí oba prahy. Oba priemery sú 2,76278. Register iba na uzle 0 dáva rovnako nulový rozdiel s priemerom 2,78807. Na jednom uzle zápis po zatvorení môže ďalej zvyšovať entropiu dvojice. Spoločná väzba na obidve miesta je experimentálne rozhodujúca.

## Ako urobiť hlavný test

1. Vopred určte 480 blokov. V každom urobte dve samostatné prípravy a náhodne určte poradie L/H. Použite rovnaké časovanie aj osvetlenie, skryte označenia pred spracovaním obrazov. Urobte jednu snímku celého prstenca hneď po skutočnom konci tretieho zápisu (nominálne t = 1,35). Primárne skóre je počet v dvojici, 0 až 3. Z rovnakej snímky uchovajte aj počet v celom prstenci. Zahrňte straty, všetky symboly registra a nulové počty. Chýbajúcu snímku označte ako chýbajúcu a hlavný test vykážte ako neúplný.
2. Pred odslepením uzamknite snímky, extrakciu počtov, párovanie a zoznam všetkých príprav. Po odslepení vyhodnoťte priemer párových rozdielov L−H a presnú jednostrannú randomizačnú skúšku s α = 0,05. Pozitivita sama neurčuje mechanizmus. Zverejnite priemery, histogramy oboch ramien a výsledky kontrol vrátane opačného smeru.
3. Pri 480 prípravách na rameno je simulovaná sila 99,13 % pri dokonalom detektore a 92,78 % pri nezávislej 90 % detekcii každej častice bez falošných zásahov. Pri druhej hodnote je 95 % interval neistoty samotného Monte Carla 91,93–93,54 % (4 000 syntetických experimentov). Pre reálny detektor pred zberom hlavných dát zmerajte úplnú maticu zámen vrátane dvojíc, trojíc a falošných zásahov a prepočítajte silu. Rozpočet 960 snímok zahŕňa iba hlavný test.

## Kontroly a hranice výkladu

- **Štvrtý cyklus.** Na oddelených prípravách odčítajte aj t = 1,80. Predpovedané histogramy pre 0/1/2/3 atómy sú v L (0,00583 / 0,05896 / 0,27263 / 0,66257), v H (0,01550 / 0,10328 / 0,33184 / 0,54938) a pri otvorenej hranici (0,02824 / 0,14857 / 0,36491 / 0,45828). Otvorenú referenciu možno použiť ako fyzickú kontrolu len na zariadení, ktoré ju vie nezávisle realizovať. Naprogramovaný spoločný časovač alebo rovnomerný náhodný výber uzavretia v cykle 2 či 3 nezávislý od ramena dáva nulový rozdiel. Časovač s prístupom k označeniu ramena dokáže signál presne kopírovať. Odpojte spätnú väzbu a archivujte riadiace priebehy.
- **Strata alebo chyba detekcie.** Spoločné uzavretie už v druhom cykle a následná 6,82 % nezávislá strata každej častice výlučne v H presne napodobní rozdiel regionálnych priemerov. V celom prstenci by chýbalo v priemere 0,205 atómu. Vyhodnoťte všetky miesta, prekalibrujte detektor v oboch režimoch a nezávisle zmerajte skutočné preskoky, rozladenie, straty a presluch. Snímka sama nerozlíši stratu od nedetekovania.
- **Časovanie.** Pri d ∈ {0,39; 0,40; 0,41} a τ ∈ {0,045; 0,05; 0,055} v každom z troch cyklov zostáva poradie cyklov 2/3 na všetkých 729 cestách. Pri párovo rovnakých časoch a kompenzovaných plochách je kontrast 0,16470 až 0,18943 atómu. Výsledok sa vzťahuje na túto diskrétnu mriežku.
- **Kalibrácia registra pri pohybe.** V simulácii necháme známe počiatočné konfigurácie tunelovať aj počas zápisu a potom prečítame Fourierovu bázu. Pri rovnomernom výbere konfigurácií v každom sektore a rovnakom zastúpení 0 a 3 v symbole 0 dostávame 0,76161 a 1,03048 natu. Oba výsledky ponechávajú cykly 2/3. Predpísané prahy vychádzajú z pevnej kalibrácie. Táto skúška skúma jeden konkrétny súbor pohybujúcich sa vstupov. Na čipe osobitne pripravte aj rozdielne rozdelenia rovnakého súčtu a zmerajte, či register skutočne číta celý pár rovnako.

Nezávislý kontrolný kód pripravil Fable 5.2 cez Claude CLI bez prístupu k prvému kódu. Lokálne porovnanie oboch výpočtov preverilo všetkých šesť nominálnych prípadov do 10⁻¹¹. Po druhej konzultácii sme pridali uzol 0, štvrtý cyklus, kontrolu straty a kalibráciu počas pohybu. Rozhodujúci ďalší krok je fyzicky overiť spoločnú väzbu a zhodu rušenia v L/H na zariadení. Test samotnej ITHKOR potom môže použiť vopred uloženú predpoveď.
