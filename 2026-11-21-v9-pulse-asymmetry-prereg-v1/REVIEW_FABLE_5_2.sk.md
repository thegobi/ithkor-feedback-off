# Nezávislá oponentúra Fable 5.2

## Prvý posudok

Claude CLI, model potvrdený v poli modelUsage: claude-fable-5-2. Čas prijatia 2026-11-21T11:18:52+00:00. Identifikátor odpovede e1628a95-c149-449c-a9be-15f46fc445a2. Vstup tvorili všetky nižšie uvedené súbory v plnom znení. Nástroje recenzenta boli vypnuté.

- `PROTOCOL.sk.md` — `22761cac566ce3f875e185ba28213d78beb40db6969691354803f64947cf1988`
- `TEORIA.sk.md` — `9673005f4b8d238c230389869991e40a0006f310775d7b1a69819ddee7211eb4`
- `reproduce.py` — `046f303bbff803684f11336f88ff3a7f5d2991b3093dbb73a47928f63635abfc`
- `requirements.txt` — `6afb83d59515deb526c4879fe45c151289c53c8b2bd6c073dfcd3702132e51ac`
- `RESULTS.json` — `aade4d337b7c0e6813aa0911811a27a49e47d999dce6b0bc3011b20fa95c2628`

# Oponentúra ITHKOR v9

**Verdikt: balík nie je pripravený na lokálne vedecké zmrazenie; blokujú ho body B1–B4.** Všetko nižšie je statická kontrola (čítanie a ručný prepočet). Kód som nespustil a odtlačky SHA-256 som neoveril. `SHA256SUMS.txt` nie je priložený a existenciu verzií v `requirements.txt` neviem potvrdiť.

## 1. Fyzika, numerika, tabuľky: chybu som nenašiel (statická kontrola)

- **Pulz:** plocha je A, vrchol 2A/T a g₀,₁(x)=g₀,₉(1−x). `pulse` vracia −ġ/g_max a jeho integrál cez zostupnú hranu je 1 pre oba tvary. Sadzba r má jednotku 1/čas.
- **Hamiltonián:** hrany 1–2 a 5–0 majú 0,65, bozónové faktory a U/2 sedia, preskoky sa nezapočítavajú dvakrát.
- **Liouvillián:** `drive` = −ig(j·n_b − k·n_c), odfázovanie −κ len mimo diagonály, skok `kron(a,a)` s antikomutátorom −½{n₁,ρ}. Vzťah η=(3F−1)/2 je konzistentný s textom.
- **Entropia:** `conditional_entropy` počíta ΣS(τ_n)−S(Στ_n). Diagonalitu v n₁ oprávňuje superselekcia počtu.
- **Nulová kontrola:** ručne vychádza v=2,0658, sin²(vT)=0,010631 a hranica 0,07056. Argument je samokonzistentný, lebo r=0, kým C je pod prahom.
- **Čísla:** tabuľky koncových bodov, q a plánov sedia s `RESULTS.json`, vrátane súčtov sektorov, stredných N a súčinov síl.
- **Typ I:** prienik dvoch jednostranných testov s bránou H→L a pevným n drží ≤0,05 bez korekcie.
- **Dve vernosti:** text korektne netvrdí polohu koreňa; overujú len znamienka v dvoch bodoch. Jednoznačnosť koreňa však kód nekontroluje. `brentq` beží na jedinom intervale a lokálny sklon (≈1,53) sa líši od priemerného (≈0,83). Oprava: pridať do `physics_results` sken Δ(F) na mriežke.

## 2. Blokujúce body (pravidlá návrhu, nie kalibračné dáta)

**B1. Plán počtov je podľa vlastného pravidla nepoužiteľný.**
- Miesto: tabuľka „design" (sila 0,800006 a 0,800062) proti vete „ak spoločná sila pri najhorších prípustných parametroch klesne pod cieľ, profil sa nepoužije".
- Problém: rezerva je nulová, takže každá nenulová neistota d, F alebo pozadia vyradí oba profily.
- Chýba pravidlo výberu medzi 0,99 a 0,98, napríklad pre d=0,985 alebo d<0,98.
- `observed()` nemá člen pre bežnú stratu pozadia ani pre nesymetrickú citlivosť a špecificitu.
- Oprava: zmraziť algoritmus namiesto čísel, teda `search_design` v najhoršom rohu kalibračného intervalu. Vzorec rozšíriť na q=b+(1−b−f)P s predpísaným meraním b a f. Alternatívou je cieľová sila s rezervou.

**B2. Pravidlo chýbajúcich údajov je nezlučiteľné so silou.**
- Miesto: odsek o chýbajúcich výsledkoch proti predpokladu „úplné dáta".
- Hrubý normálny odhad pre d=0,99 pri 1 % chýbajúcich príprav a doplnení proti smeru: rozdiel v L klesne z 0,0193 na ≈0,009 a sila L z 0,81 na ≈0,3.
- V H klesne sila z 0,99 na ≈0,8.
- Oprava: vopred určiť rozpočet neúplnosti m, počítať n pri najhoršom doplnení a pri prekročení m vyhlásiť stupeň za nepotvrdzujúci.

**B3. Kontroly nemajú rozhodovacie pravidlá.**
- Miesto: sekcia „Diagnostické kontroly".
- Nulová kontrola, predhistória a odpojená väzba nemajú počty, číselné kritériá ani čas vzhľadom na odslepenie.
- „Rovnaké miery" v predhistórii bez ekvivalenčnej medze a n sú nefalzifikovateľné.
- O „porušení kvalifikácie" nie je určené, kto, kedy a podľa akých prahov rozhoduje. Neúspech sa tak dá dodatočne pripísať aparatúre.
- Oprava: doplniť n, medze a prekladanie kontrol v oboch stupňoch. O odchýlkach rozhodnúť zaslepene pred vydaním kľúča.

**B4. Text nezodpovedá kódu a definícia stavu je neurčitá.**
- Miesto: `run`, riadok `visibility *= eta**9`. Protokol dĺžku predfázy 9T ani príslušné predpovede (0,1424 a 0,1426; 0,2275 a 0,2521) neuvádza.
- „Nepodmienený stav" pri randomizácii nie je definovaný. Kód simuluje každý známy symbol a tvar zvlášť, zmes cez zaslepené pridelenie by dala iné C.
- Oprava: napísať, že ρ je podmienené všetkými zaznamenanými klasickými nastaveniami. Doplniť 9T a čísla do protokolu.

## 3. Medze interpretácie

- **Bežná strata napodobní každý stupeň zvlášť.** Strata úmerná ∫g·n₁dt zvýhodní neskorý vrchol, lebo ⟨n₁⟩ v okne rastie, a napodobní L. Mechanizmus zvýhodňujúci skorú ostrú hranu (dlhší čas na únik pred počítaním) napodobní H. Špecifické je len obrátenie.
- **F je zamenené s časom.** H a L sa zbierajú po sebe, takže zmena F splýva s driftom a presluchom generátora odfázovania. Kontrola s odpojenou väzbou stratu pri zapnutom g neodhalí. Oprava: prekladať kontrolné ramená so zapnutou väzbou v oboch stupňoch.
- **Mapa F→κ pripisuje celú nevernosť odfázovaniu počas kontaktu.** Vlastná predhistória ukazuje, že záleží na tom, kedy koherencia zanikne: pri H s η⁹ vopred je rozdiel 0,14243 proti 0,14263, teda efekt H mizne. Počiatočná viditeľnosť registra je skrytý parameter. Oprava: oddelene kalibrovať prípravu a odčítanie, pridať v₀ do modelu a tolerancií.
- **Presná nula H/slow je prahový jav.** Rezerva max(C−prah) sa nevykazuje. Pôvod prahu (9 platných číslic) a zisku nie je v balíku. Oprava: doplniť rezervu a citlivosť na prah, plochu, časovanie a F.
- **Nulová kontrola nerozlišuje model od štandardu.** Meria len bežné straty a pri trojitom obsadení pribúda trojčasticová rekombinácia. Analytická rezerva sa minie pri váhe n₁≠3 okolo 0,036 (ručný odhad), čo vyžaduje čistotu prípravy asi nad 97,5 %.

## 4. Experimentálne požiadavky

- **Detektor:** úplná matica zámen pre N=0…3; paritné zobrazovanie je vylúčené.
- **Tolerancia F:** L leží len 0,019 od koreňa. Odchýlka 0,005 zmení efekt L o približne 20–40 % a n zhruba o faktor 2.
- **Jednopásmový model:** nábeh trvá 0,005 ħ/J, jeho platnosť treba doložiť.
- **Randomizácia:** určiť schému, generátor a správu kľúča. Medzi H a L určiť pravidlo rekalibrácie d.
- **Analytický skript nie je zmrazený:** `fisher_greater` a `contrast_interval` sa nikde nevolajú. Obálka intervalov cez doplnenia nie je implementovaná a metóda intervalu rozdielu nie je v texte pomenovaná.
- **Drobnosti:** definovať označenie „10/90". Stĺpce „samostatne" výslovne označiť za nepotvrdzujúce.

## Záver

Balík nie je pripravený na lokálne vedecké zmrazenie. Jadro (Hamiltonián, Liouvillián, entropia, nulová hranica, tabuľky, typ I) je podľa statickej kontroly bez nájdenej chyby. Blokujú:

1. **B1** – nulová rezerva sily proti vlastnému vyraďovaciemu pravidlu, chýbajúce pravidlo výberu d a člen pozadia.
2. **B2** – neúplnosť bez rozpočtu a bez sily pri najhoršom doplnení.
3. **B3** – kontroly a kvalifikácia bez počtov, prahov a zaslepeného rozhodovania.
4. **B4** – nezdokumentované η⁹ a nedefinovaný súbor pre „nepodmienený" stav.

Po ich textovej oprave je návrh zmraziteľný; kalibračná príloha môže zostať oddelená.

## Odpoveď autorov na prvý posudok

- B1. Ponechali sme pôvodné počty ako nominálne výsledky. Pre hardvérovú štúdiu sú teraz vopred dané dva konzervatívne profily. Vyberie sa prvý, do ktorého sa zmestí celý nezávisle kalibrovaný rozsah. Sila sa prepočítava na najmenej priaznivom súbehu strát, pozadia a nesymetrických chýb počítania v štyroch bunkách.
- B2. Je dovolený najviac jeden chýbajúci výsledok na hlavné rameno. Pre toto maximum skript vypočíta dolnú hranicu sily a vyhodnotí smer aj jeho opak pri nepriaznivom doplnení. Nad limitom je výsledok nespôsobilý na potvrdenie aj na falzifikáciu. Skript vyhodnocuje tiež predpísané obálky Clopperových–Pearsonových intervalov.
- B3. Všetky štyri hlavné ramená sa zbierajú v spoločnom období. Preregistrácia určuje rozdelenie do blokov, kontrolné prípravy, menovatele, ekvivalenčné medze a 65 porovnaní vopred. Kontrolné dáta sa otvoria ako prvé. Výsledky L zostanú v úschove do úspechu H. Cena panelu aj jeho nominálne simulovaná priechodnosť sú oddelené od počtu a sily hlavných meraní.
- B4. Protokol špecifikuje priemerovanie vnútri fyzických nastavení. Obsahuje prípravu počas deviatich dôb zápisu, štyri predpovede a nezávislé kalibrovanie počiatočnej viditeľnosti aj straty koherencie počas kontaktu. Skript teraz dovoľuje meniť obe samostatne.
- Doplnené sú rezerva pod prahom v H pri pomalom nábehu, kontrola priesečníka jemnejším integrátorom, sken cez vernosti, citlivosť na parametre a zdroj fixných konštánt. Obmedzenia zahŕňajú prenos z kontrol na hlavné prípravy aj možnosť bežného fyzikálneho procesu závislého od tvaru pulzu a odfázovania. Príloha konkrétneho prístroja a nové hardvérové meranie zostávajú podmienkou experimentálneho záveru.

## Opakovaná oponentúra

Claude CLI, model potvrdený v poli modelUsage: claude-fable-5-2. Čas prijatia 2026-11-21T11:32:39+00:00. Identifikátor odpovede 080810be-6bf4-4d93-b412-0eb5552a1ac0. Vstup tvorili všetky nižšie uvedené súbory v plnom znení. Nástroje recenzenta boli vypnuté.

- `PROTOCOL.sk.md` — `481a4c4a318f5093de5bd8403d41afcdbd1f6412e69bd18d69598d986549b1a2`
- `TEORIA.sk.md` — `53d8696404fda4b6f05801f5c0dd28041b8adb90b06f9df510887b63540c76e7`
- `reproduce.py` — `1550997b9ea51dce4193778249ce833866ad651239d7efe5af398c6398088a06`
- `requirements.txt` — `6afb83d59515deb526c4879fe45c151289c53c8b2bd6c073dfcd3702132e51ac`
- `RESULTS.json` — `b9df0985edc6fc7682117be23554bc77f133ae6786607a2acd2f22d8c90ab803`

**Verdikt: balík je pripravený na lokálne vedecké zmrazenie.** Body B1–B4 sú uzavreté a novú blokujúcu chybu som nenašiel. Všetko nižšie je statická kontrola (čítanie a ručný prepočet): kód som nespustil, odtlačky som neoveril a `SHA256SUMS.txt` nie je priložený.

## Uzavretie B1–B4

- **B1:** Rohy q oboch profilov mi ručne vychádzajú zhodne s `RESULTS.json`, napríklad pre A je minimum L-slow 0,1174932 a maximum L-fast 0,1112846. Normálny odhad sily L dáva ≈0,875 (A) a ≈0,889 (B), v zhode s tabuľkou. Príklady d=0,985 a 0,978 sedia a argument monotónnosti je správny.
- **B2:** `adverse_fisher_power` zodpovedá textu (X−1 proti Y+1). Test x proti y+r je konzervatívny, takže typ I ≤0,05 na úrovni q drží. Nad rozpočet je stupeň nespôsobilý v texte aj v `score_blinded`.
- **B3:** 34 buniek, chvost 0,05/68, 65 porovnaní (2×24+17) a 147 456 príprav sedia s `control_gate`. Poradie kontroly → H → L je v texte aj v `main`.
- **B4:** η⁹ = 0,872823 a 0,316478 sedí. Stav je definovaný pre každú fyzickú prípravu a v₀ je oddelené od κ.

## Medze interpretácie (neblokujú)

1. **Smer sa testuje na q, nie na P.**
   - Miesto: profily A/B proti pravidlu smeru.
   - Prípustný rozdiel pozadia medzi tvarmi (0,011 v A, 0,012 v B) prevyšuje zaručený kontrast L v najhoršom rohu (0,0062 a 0,0049). Samotný úspech L preto neurčuje poradie P.
   - Neblokuje to, lebo typ I je formulovaný pre q a medza δ plynie z uzamknutého `plan.json`.
   - Oprava v aparátnej prílohe: uzamknúť δ pre každý stupeň a výrok o mechanizme viazať na dolnú hranicu `risk_difference_ci95` > δ.
   - Veta v `TEORIA.sk.md` „ak vzniká iba v hlavnej príprave“ je príliš úzka.
2. **Kontrolné medze sú hrubé.** Hodnoty 0,018, 0,025 a 0,10 sú porovnateľné s kontrastom L (0,019) alebo väčšie. Panel odhalí len hrubé odchýlky, čo text priznáva.
3. **Poloha koreňa.** Dve vernosti ju neoveria, len znamienka v dvoch bodoch. Text to tvrdí správne a sken nevylučuje ďalšie priesečníky.
4. **Prah a zisk.** Sú prevzaté bez nezávislého určenia, čo je priznané.

## Experimentálne požiadavky

- **Okná P sú oveľa prísnejšie než „prvé filtre“.**
  - Pri v₀=0,995 je H-fast 0,0416, nad hranicou okna 0,0397.
  - Pri F±0,002 je L-slow 0,1228 a 0,1169, mimo okna [0,1188; 0,1211].
  - Jednotlivo to znamená približne v₀ ≳ 0,998 a |δF| ≲ 0,0008, pri súbehu ešte menej.
  - Zlyhanie je bezpečné (zber sa nezačne), ale kvalifikovateľnosť je otvorená.
- **Rozpočet chýbania.** Jeden chýbajúci výsledok na 42 000–75 000 príprav je veľmi prísny; pravdepodobnosť nespôsobilého behu nie je v sile zahrnutá, čo text priznáva.
- **Profil B.** Dolná hranica 0,009 vyraďuje detektor s malým f a väčším b, takže zmiešaná kalibrácia nevyhovie žiadnemu profilu.
- **Drobnosť.** Označenie „10/90“ stále nie je v texte priradené k fast.

## Záver

Balík je pripravený na lokálne vedecké zmrazenie v dnešnom znení. Podmienky pre aparátnu prílohu pred zberom:

1. Uzamknúť δ a pravidlo výroku o mechanizme podľa bodu 1.
2. Doložiť obálku súčasných odchýlok vnútri okien P.

Experimentálny záver ostáva podmienený kvalifikáciou prístroja a novým meraním.

## Zapracovanie zvyšných spresnení

Po súhlase s lokálnym zmrazením sme do textu doplnili výslovné priradenie 10/90 = fast a 90/10 = slow. Rozšírili sme vysvetlenie bežného rušenia aj na prípady, keď pôsobí v kontrolných prípravách. Vopred sme odvodili hranicu δ z oddelených intervalov b a f pre každý stupeň. Vyhodnocovací kód ju počíta z uzamknutej kalibrácie a porovná ju s dolnou hranicou intervalu nameraného rozdielu. Tento sekundárny výstup nemení primárne rozhodnutie ani jeho plánovaciu silu. Kvalifikačnú obálku skutočnej aparatúry možno zostaviť až z jej kalibračných údajov.

## Opakovaná oponentúra

Claude CLI, model potvrdený v poli modelUsage: claude-fable-5-2. Čas prijatia 2026-11-21T11:34:45+00:00. Identifikátor odpovede 7d14319d-2b65-47c3-b4de-d928c8d38279. Vstup tvorili všetky nižšie uvedené súbory v plnom znení. Nástroje recenzenta boli vypnuté.

- `PROTOCOL.sk.md` — `c4340718dc2df9f6eeee7d90924b1f9b97c68b0dffd9f01fab419eb521c72596`
- `TEORIA.sk.md` — `f55b6bbdaa5f8a00dc207b159274dd8ecd445e68cb0a089ae9c816458d863ff0`
- `reproduce.py` — `97289d167fe1de4a96ab8a4b233c2e51d1144ba0a6ded2822ddfe2fb9b4e2b14`
- `requirements.txt` — `6afb83d59515deb526c4879fe45c151289c53c8b2bd6c073dfcd3702132e51ac`
- `RESULTS.json` — `b9df0985edc6fc7682117be23554bc77f133ae6786607a2acd2f22d8c90ab803`

**Verdikt: v troch spresneniach som nenašiel materiálnu chybu; súhlas s lokálnym zmrazením trvá.** Všetko je statická kontrola (čítanie a ručný prepočet), kód som nespustil a odtlačky som neoveril.

1. **10/90 = fast.** Text (a=0,1, nábeh v prvých 10 %), `PULSES["fast"]=.1`, hlavičky tabuliek aj smer testov (H: fast vyššie, L: slow vyššie) sú konzistentné.

2. **Bežný efekt aj na kontrolách.** Formulácia v `TEORIA.sk.md` je správna a zhodná s protokolom: prekročenie δ nevylučuje bežný únik, ak jeho prenos z kontrol nie je ohraničený.

3. **Hranica δ.** Z q=b+(1−b−f)P pri P_h≤P_l a 1−b−f>0 je maximum rozdielu pri P_h=P_l=P. Tam platí q_h−q_l=(1−P)(b_h−b_l)+P(f_l−f_h), čo je najviac max(b_h^max−b_l^min, f_l^max−f_h^min). Znamienka aj indexy v `score_blinded` sedia. Dolná hranica používa nepriaznivé doplnenie (x proti y+r). Fixtúra dáva δ=0,001 a ručne odhadnuté dolné hranice ≈0,022 (H) a ≈0,021 (L) ju prevyšujú.

**Medza interpretácie (neblokuje):** δ kryje aj bežnú stratu len v rozsahu, v akom ju zahŕňa kalibrovaný interval b. V profile A môže δ dosiahnuť 0,011, čo je viac než zaručený kontrast L, takže sekundárny výstup bude často nepreukazný. Text to priznáva.
