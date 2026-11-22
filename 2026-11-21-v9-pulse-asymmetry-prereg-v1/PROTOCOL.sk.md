# Obrátenie poradia strát pri časovo zrkadlených pulzoch

**ITHKOR v9 · lokálny návrh predregistrácie · 21. november 2026.** Otázkou je, či presunutie maxima zápisového pulzu zo začiatku na koniec obráti svoj vplyv na pravdepodobnosť straty pri zmene vernosti fyzického registra. Číselné predpovede boli známe pri návrhu experimentu. Potvrdzujúci test vyžaduje nové, nezávislé hardvérové prípravy. Pred zberom treba datovať a uzamknúť túto verziu, kalibračnú prílohu, plán počtov a zaslepený kľúč pridelenia.

## Príprava a zásah

V jednotkách $\hbar=J_{\rm in}=1$ pripravíme tri bozóny v stave $|300000\rangle$ na šesťuzlovom Boseho–Hubbardovom prstenci číslovanom od 0. Hamiltonián má členy $-J_{ij}(a_i^\dagger a_j+a_j^\dagger a_i)$ na susedných hranách a $(U/2)\sum_i n_i(n_i-1)$, kde $U=0{,}35$. Na hranách 1–2 a 5–0 je $J_{ij}=0{,}65$, na ostatných 1. Po voľnom vývoji do $t=0{,}40$ pripojíme na $T=0{,}05$ čerstvý trojhladinový register v stave $(|0\rangle+|1\rangle+|2\rangle)/\sqrt3$. Väzba je $g(t)n_1\otimes K$, $K=\operatorname{diag}(0,1,2)$, bez kompenzačného poľa. Register počas kontaktu lokálne odfázujeme v báze $K$. Pre pevný kalibračný vstup 0, 1 alebo 2 platí pri odčítaní vo Fourierovej báze $\kappa T=-\ln[(3F-1)/2]$. Kalibrovaný vstup 3 dá rovnaký koncový symbol ako 0. V hlavnom behu sa počas pulzu nič neodčítava a žiaden výstup neriadi stratu.

Položme $x=(t-0{,}40)/T$, $A=2\pi/3$. **10/90 (fast)** označuje nábeh počas prvých 10 % a dobeh počas zvyšných 90 % pulzu, teda $a=0{,}1$. **90/10 (slow)** má nábeh počas 90 % a dobeh počas 10 %, teda $a=0{,}9$. Pre obe obálky je

$$
g_a(t)=\frac{A}{T}
\begin{cases}
1-\cos(\pi x/a),&0\le x\le a,\\
1+\cos(\pi(x-a)/(1-a)),&a<x\le1,\\
0,&\text{inak}.
\end{cases}
$$

Pulzy majú rovnakú plochu $A$, vrchol $g_{\max}=2A/T$ a navzájom zrkadlené časové stopy. Prstenec sa počas zápisu ďalej vyvíja.

## Testovaná hypotéza

Pre spoločný stav pri pevných fyzických nastaveniach $\rho$ prstenca a registra označme $\tau_n=\operatorname{Tr}_{\rm prstenec}[(\Pi_{n_1=n}\otimes I)\rho]$, $0\le n\le3$. Pre oblasť $R$ (uzol 1) a register $\mathcal A$ vypočítame podmienenú entropiu $C=S(R|\mathcal A)=\sum_n S(\tau_n)-S(\sum_n\tau_n)$. Použijeme $S(M)=-\operatorname{Tr}M\ln M$ aj pre nenormalizované bloky. Pre každú zaznamenanú prípravu, fyzické nastavenie registra, zadaný symbol a tvar pulzu berieme súbor cez všetky možné výstupy registra a histórie straty. Zaslepený kľúč určuje prístup analytika k dátam. Fyzické ramená pri výpočte hustotnej matice zostávajú oddelené. Lokálna strata na uzle 1 je dodatočný modelový postulát. S $[z]_+=\max(0,z)$ a $P_j=I\otimes|j\rangle\langle j|$ má tvar

$$
\dot\rho=-i[H_{\rm BH}\otimes I+g_a n_1\otimes K,\rho]
 +\kappa\sum_j\mathcal D[P_j]\rho
 +r\mathcal D[a_1\otimes I]\rho,\qquad
r=1{,}68911\,[-\dot g_a/g_{\max}]_+\,[C-0{,}193567742]_+ ,
$$

kde $\mathcal D[L]\rho=L\rho L^\dagger-\{L^\dagger L,\rho\}/2$. Prah má jednotku nat. Prah aj násobiteľ sú fixné pre všetky ramená. Pri odpojenom pulze je $r=0$. Ideálny štandardný model s uvedeným Hamiltoniánom a samotným odfázovaním zachováva celkový počet. Lokálne obsadenie sa pritom môže meniť tunelovaním.

## Koncové meranie a predpoveď

Na konci jediného zápisu v $t=0{,}45$ zmeriame **celkový** počet atómov na šiestich uzloch. Primárny výsledok prípravy je $Y=\mathbf1\{N(0{,}45)<3\}$. Sekundárne vykážeme histogram $N=0,1,2,3$ a priemer. Konečná strata sama neurčuje miesto ani čas odchodu atómu.

<!-- generated:endpoints -->
| Rameno registra | P(strata) 10/90 | P(strata) 90/10 | Priemer N 10/90 | Priemer N 90/10 |
|---|---:|---:|---:|---:|
| H | 0,03857791 | 0,00000000 | 2,9609127 | 3,0000000 |
| L | 0,10023966 | 0,11994349 | 2,8961984 | 2,8749031 |

Modelový priesečník je pri F = 0,93894920. Spoločná pravdepodobnosť straty je 0,08365236.
<!-- /generated:endpoints -->

Dva plánované stupne testujú opačné znamienka. Experimentálny odhad polohy koreňa vyžaduje samostatný vopred určený plán s ďalšími hodnotami $F$.

Koncový detektor má v nominálnom príklade bez ďalšieho pozadia rovnakú citlivosť aj špecificitu $d$. Pozorovaná miera je $q=(1-d)+(2d-1)P(Y=1)$. Vernosť $F$ sa meria na registri, $d$ na atómovom detektore. Toto sú pravdepodobnosti kladného výsledku koncového merania.

<!-- generated:readout -->
| Presnosť d | H 10/90 | H 90/10 | L 10/90 | L 90/10 |
|---|---:|---:|---:|---:|
| 0,99 | 0,04781 | 0,01000 | 0,10823 | 0,12754 |
| 0,98 | 0,05703 | 0,02000 | 0,11623 | 0,13515 |
<!-- /generated:readout -->

## Počty, zaslepenie a rozhodnutie

Nasledujúca tabuľka reprodukuje návrhové počty pri dokonale známych chybách, nezávislých prípravách a úplných dátach. „Samostatne“ je počet na test jedného smeru. „Spoločne“ je nominálny počet pre prienik dvoch nezávislých testov. Sú to referenčné výpočty. Pre skutočný potvrdzujúci experiment sa používajú vyššie počty z časti o neistote kalibrácie.

<!-- generated:design -->
| Presnosť d | H samostatne | L samostatne | H spoločne | L spoločne | Celkom spoločne | Spoločná sila |
|---|---:|---:|---:|---:|---:|---:|
| 0,99 | 269 | 3545 | 571 | 3651 | 8444 | 0,800006 |
| 0,98 | 371 | 3897 | 766 | 4056 | 9644 | 0,800062 |
<!-- /generated:design -->

**Poradie rozhodnutí.** Štyri hlavné ramená zozbierame súbežne v spoločnom kalendárnom čase, s náhodne premiešanými prideleniami. Údaje H a L sa archivujú oddelene. Po uzamknutí všetkých meraní, diagnostiky a kľúčov v stupni 1 odslepujeme iba H. Jednostranným Fisherovým exaktným testom pri p ≤ 0,05 overíme, či 10/90 dáva častejšie stratu než 90/10. Iba po kvalifikovanom úspechu H otvoríme nezávislé dáta L a tým istým testom overíme opačný smer. Ak H neprejde, L ostane uzamknuté pre potvrdzujúcu analýzu. Spoločný podpis vyžaduje splnenie oboch podmienok. Počty, kalibrácia a pravidlá ostanú uzamknuté počas oboch rozhodnutí.

## Počty hlavného experimentu a podmienky sily

Pôvodné tabuľky s rovnakou špecificitou a citlivosťou 0,99 alebo 0,98 opisujú ideálny výpočet pri úplných dátach. Prevádzkové počty hlavného experimentu určuje nasledujúci postup. Intervaly sú tolerancie návrhu. Ich splnenie musí nezávisle doložiť aparátna kalibrácia ešte pred prvou hlavnou prípravou.

Pre každú zo štyroch buniek osobitne nech P označuje pravdepodobnosť straty pripísanej testovanému mechanizmu, b pravdepodobnosť kladného terminálneho výsledku pri neprítomnosti takej straty a f pravdepodobnosť záporného terminálneho výsledku pri jej prítomnosti. Platí q=(1−P)b+P(1−f). Parameter b zahŕňa bežnú fyzickú stratu i falošne kladný odpočet. Pri pozadí s pravdepodobnosťou u a pri podmienenej falošnej pozitivite e₀ a citlivosti s_bg je b=(1−u)e₀+u s_bg. Samotná referencia troch atómov pred detektorom neurčuje u ani b. Pre b treba aj nezávislé fyzikálne kontroly pozadia s rovnakým trvaním a zaťažením v príslušnej bunke, pre f známe stratené častice a odstupňované referencie N=0,1,2. Z neurčitého zloženia sektorov či dráh sa použije obálka. Každý rozdiel podmienok voči cieľovej bunke vrátane straty pri zapnutom g musí mať zdôvodnenú hornú medzu pred odslepením. Ak samotné kontrolné dáta nedovoľujú ohraničiť b alebo f v danej bunke, kalibrácia neprešla. Efekt mechanizmu a pozadie, ktoré sa takto nedajú identifikovať, sa nesmú odčítať z hlavného signálu.

Prevádzkové tolerancie pre fyzikálne P sú H-fast [0,0375; 0,0397], H-slow [0; 0,0011], L-fast [0,0991; 0,1014] a L-slow [0,1188; 0,1211]. Do každej musí úplne vojsť vopred vypočítaný interval zahŕňajúci neistoty prípravy, F, časovania, plochy a tvaru aj ostatných fyzikálnych kalibrácií. Pre profil A musí byť kalibračný interval každého b aj f v každej bunke v [0; 0,011]; pre B v [0,009; 0,021]. Vyberie sa prvý vyhovujúci profil v poradí A, B, inak sa hlavný experiment nezačne. Napríklad symetrické bodové d=0,985 pri nulovom dodatočnom pozadí pripúšťa B, d=0,978 žiadny. Rozhodujú celé intervaly vrátane neistoty a bežnej straty. Profil, počty, štyri predikčné intervaly q z užších kvalifikovaných medzí, zdroje neistôt a kľúč sa uzamknú pred zberom. Počas experimentu možno kvalifikáciu iba stratiť. Kalibrácia nesmie prepnúť profil alebo zúžiť predpovede po pozretí koncových dát.

<!-- generated:robust -->
| Profil | H na tvar | L na tvar | H + L spolu | Sila H | Sila L | Spoločná sila |
|---|---:|---:|---:|---:|---:|---:|
| A | 2100 | 42000 | 88200 | 0,999740 | 0,874860 | 0,874632 |
| B | 2800 | 75000 | 155600 | 0,998816 | 0,888753 | 0,887701 |
<!-- /generated:robust -->

Výpočet preverí všetky rohy trojrozmerného rozsahu (P,b,f) v každej bunke. Pozorovaná pravdepodobnosť q je multilineárna, preto jej minimum a maximum ležia v rohoch kvádra. Kritický jav jednostranného Fisherovho testu je rastúci v počte pozitívnych v predpovedanom vyššom ramene a klesajúci v druhom. Aj po nepriaznivom doplnení teda najmenšia sila nastane pri dolnej hranici q vyššieho ramena a hornej hranici q nižšieho. Parametre štyroch buniek sa môžu meniť nezávisle. Spoločná dolná medza je pravdepodobnosť latentnej udalosti, ktorá zabezpečí úspech oboch stupňov pre každý povolený vzor chýbania. Je súčinom pravdepodobností udalostí v dvoch nezávislých úplných vzorkách. Platí aj pri účelovej voľbe chýbajúcich výsledkov naprieč blokmi, pokiaľ v žiadnej bunke nechýba viac než jeden. Podmieňuje sa platnosťou kalibrácie, kontrol a rozpočtu neúplnosti ako vopred garantovaných prevádzkových podmienok; tabuľka nezahŕňa pravdepodobnosť úspechu kvalifikácie, prevádzkového výpadku či informatívneho vyradenia celého behu. Náhodné nezávislé binomické pokusy sú predpoklad; spoločný neobmedzený drift znemožňuje túto interpretáciu.

Rozpočet je nanajvýš jeden chýbajúci výsledok na každé hlavné rameno. Všetky pridelenia ostávajú v menovateli a neexistujú náhrady. Pri strate nad rozpočet alebo nesprávnom pridelenom počte sa stupeň označí za nepotvrdzujúci. Ak by v úplných dátach bolo X a Y pozitívnych, najhoršia strata jednej informácie v každom smere dá max(0,X−1) a min(n,Y+1). K týmto extrémom sa dá dospieť zneprístupnením jedného kladného a jedného záporného výsledku, ak existujú. Skript sčíta pravdepodobnosti úspechu pri tejto dvojici po dvoch binomických zákonoch. Numerické vynechanie chvostov má pravdepodobnosť nanajvýš 2,01×10⁻¹⁴ na stupeň. Bez ohľadu na informatívnosť chýbania významnosť skúšky nemení nepriaznivé doplnenie, lebo zamietnutie vyžaduje úspech pri každom doplnení.

Pre skutočné dáta s x pozorovanými stratami a m chýbajúcimi vo vyššom ramene a y stratami, r chýbajúcimi v nižšom, smerový test použije x oproti y+r pri p≤0,05. Opačný test použije y oproti x+m pri p≤0,025. Predpovedaným vyšším ramenom je v H fast a v L slow. Každý zo štyroch vopred plánovaných podielov dostane dvojstranný 98,75 % Clopperov–Pearsonov interval rozšírený cez všetky doplnenia (dolná hranica z x, horná z x+m). Bonferroniho súhrnné pokrytie štyroch latentných podielov je aspoň 95 % pred výberom stupňa; nevzniká tvrdenie o podmienenom pokrytí po výsledku H. Pri prieniku s vopred uzamknutým intervalom q je predpoveď zlučiteľná v tomto zmysle; prázdny prienik kvalifikovanej bunky je kvantitatívny rozpor. Hranice, ktoré sa iba dotýkajú, majú neprázdny prienik. Pre rozdiel rizík sa navyše uvedie opisný konzervatívny 95 % interval zo štyroch jednostranných Clopperových–Pearsonových medzí s chvostom 0,0125 a obálkou doplnení; ide o pokrytie jedného kontrastu. Smerový výsledok, opačný smer a rozpor číselnej predpovede sa vykážu osobitne. Pri kvalifikačnej odchýlke majú intervaly a p-hodnoty opisný význam.

V spoločnom náhodne premiešanom zbere vzniknú H a L z odlišných fyzických príprav. Hlavná vzorka obsahuje všetky štyri skupiny aj pri neúspechu H. Pred vydaním kľúča sa uzamknú agregáty a nezávislé verdikty kvalifikácie. Súbor L zostane v oddelenej úschove a analytik ho smie otvoriť iba po kvalifikovanom úspechu H pri vopred určenom teste. Po neúspechu H sa L neotvorí a spoločný podpis nebol potvrdený. Zachová sa rodinná hranica 0,05 pre falošné potvrdenie spoločného smeru testom prieniku podmienok a Bonferroniho hranica 0,05 pre aspoň jeden opačný smer (dva možné testy po 0,025).

## Zber, slepé kontroly a vydanie kľúčov

**Čo dokazuje smerový test.** Hlavný test sa týka pozorovaných mier $q$. Aparátna príloha pred zberom uzamkne ešte jednu hranicu pre každý stupeň. Označme očakávane vyššie rameno ako h a nižšie ako l. Z nezávislých kalibračných intervalov pre pozadie a zámenu určíme $\delta=\max(0,b_h^{\max}-b_l^{\min},f_l^{\max}-f_h^{\min})$. Ak fyzická miera $P_h\le P_l$, pri kladnej citlivosti kanála $1-b-f$ je rozdiel pozorovaných mier najväčší pre rovnaké $P$ a tam je afinný v $P$. Jeho maximum na [0,1] teda nepresiahne $\delta$. Ak dolná hranica 95 % intervalu rozdielu v danom stupni prevýši uzamknuté $\delta$, samotné prípustné chyby tohto kanála nevysvetlia smer. Vyhodnocuje sa to sekundárne pre každý uskutočnený stupeň. Uvedená sila sa vzťahuje iba na primárne testy $q$. Aj prekročenie oboch hraníc pripúšťa skutočný bežný fyzikálny únik napodobňujúci v9, pokiaľ jeho prenos z kontrol nie je spoľahlivo ohraničený.

**H a L sú dva stupne analýzy.** V jednej akvizícii sa prekladajú všetky štyri hlavné kombinácie vernosti a tvaru. Akvizícia má dve po sebe idúce epochy. V každom hlavnom ramene pridelíme do prvej epochy dolnú celú polovicu pevného počtu a do druhej zvyšok. V každej epoche rozloží správca pridelenia všetky typy vrátane kontrol do 32 časových blokov. Počty jedného typu rozdelí rovnomerne (zvyšok po jednom do prvých blokov) a zoznam každého bloku nezávisle premieša generátorom NumPy PCG64 s jedným tajným 128-bitovým semenom z operačného systému. Pred prvou prípravou uloží odtlačky semena, zoznamu a kľúčov. Riadenie dostane recept podľa ID, vyhodnocovateľ koncového počtu dostane iba ID. Každá príprava používa nový nezávislý stav.

Pre ideálnu nulovú kontrolu so stavom $|030000\rangle$ pri začiatku zápisu platí $S(R)=0$. Počas celého pulzu dáva tunelovanie hornú hranicu $S(R|A)\leq0{,}07056$ natu. Tak zostáva fyzická predpoveď nula pri oboch tvaroch a oboch vernostiach. Odvodenie je v TEORIA.sk.md.

**Kontrolný panel.** V tabuľke sú počty na jednu epochu. Každý riadok s označením „4“ zahŕňa všetky kombinácie H/L × fast/slow v tej istej epoche. Rovnaké koncové počítanie a slepé priradenie platia pre celý panel.

| Príprava | Počet nastavení | Príprav na nastavenie |
|---|---:|---:|
| Známe tri atómy v referenčnej príprave pri koncovom odčítaní, bez zápisu | 1 | 8 192 |
| Nulová kontrola, tri atómy na uzle 1 pripravené priamo v 0,40, väzba zapnutá | 4 | 8 192 |
| Hlavná atómová príprava, riadenie registra a rovnaká záťaž, fyzická väzba zápisu odpojená | 4 | 4 096 |
| Hlavná atómová príprava, väzba zapnutá, predhistória so symbolom 0 | 4 | 2 048 |
| Tá istá kontrola so symbolom 1 | 4 | 2 048 |

Oba symboly predhistórie majú rovnakú prípravnú fázu dĺžky $9T$ s rovnakým odfázovaním. Dve epochy vyžadujú **147 456 kontrolných príprav navyše** (73 728 na epochu). Prípravy pre nezávislú vstupnú kalibráciu sa účtujú osobitne.

Po ukončení oboch epoch sa uzamknú terminálne počty, neúplnosť a telemetria všetkých pokusov. Nezávislý správca vydá **najprv iba kontrolný kľúč**. V každej z 34 kontrolných buniek je výstupom príznak pozorovaného $N<3$. Pri $n$ prideleniach, $x$ zistených udalostiach a $m$ chýbajúcich je dolná hranica Clopperovho–Pearsonovho intervalu z $x$ a horná z $x+m$. Každý chvost má pravdepodobnosť $0,05/68$. Pre rozdiel buniek $i-j$ použijeme interval $[L_i-U_j,U_i-L_j]$. Celá rodina intervalov má pri nezávislých binomických prípravách pokrytie aspoň 95 % aj pri zdieľanej referencii.

Spôsobilosť kontrol vyžaduje, aby **celý interval každého** nasledujúceho rozdielu ležal medzi $-M$ a $+M$ vrátane krajov. Medze sú absolútne rozdiely pravdepodobností a slúžia na odhalenie odchýlok danej veľkosti.

- V každej epoche porovnáme každú zo štyroch zapnutých nulových kontrol s referenciou a všetkých šesť dvojíc týchto kontrol medzi sebou, $M=0,018$. Pre odpojené kontroly zopakujeme rovnakých desať porovnaní s $M=0,025$.
- V každej epoche pre každú dvojicu vernosti a tvaru porovnáme zapnuté kontroly s predhistóriou 0 a 1, $M=0,10$. Táto kontrola identifikuje hrubú závislosť od prípravného symbolu. Reziduálne vplyvy na úrovni hlavného kontrastu ňou nemožno vylúčiť.
- Medzi epochami porovnáme každú zo 17 buniek s tou istou prípravou v druhej epoche. Uplatní sa $M=0,018$ pre referenciu a nulové kontroly, $0,025$ pre odpojenú väzbu a $0,10$ pre predhistórie.

Takto vznikne 65 pevne určených porovnaní. Neplatný počet alebo kľúč, chýbajúca bunka, nesplnená medza, hardvérová odchýlka za uzamknutou toleranciou alebo neúplná kvalifikačná príloha dávajú stav **nespôsobilé**. Dôvod a všetky kontrolné intervaly sa zaznamenajú ešte pred sprístupnením ktoréhokoľvek hlavného kľúča. Hlavné výsledky nespôsobilej štúdie sa zverejnia opisne podľa pôvodného pridelenia. Neslúžia na potvrdzujúci výrok ani na vyvrátenie modelu. Pri spôsobilom paneli a splnených vstupných kritériách sa sprístupní najskôr H. Až jeho úspech otvára L na potvrdzujúci test; po neúspechu H treba vykázať, že L bolo zozbierané a jeho potvrdzujúci test sa neuskutočnil. Údaje sa zachovajú aj v tomto prípade. Opakovaná kalibrácia po H nesmie spätne zmeniť priradenie, profil, menovatele ani kvalifikačné rozhodnutie.

**Pravdepodobnosť úspechu kontrol.** Pri nezávislých binomických pokusoch, nulových fyzických stratách v referenčných, odpojených a nulových kontrolách, nominálnych stratách predhistórie, presnom symetrickom detektore a úplných dátach prešlo panelom 19 439 z 20 000 simulovaných štúdií pre $d=0,99$ a 19 072 pre $d=0,98$ (PCG64, semeno 20261121). Ide o samostatný plánovací výpočet. Hlavná smerová sila uvádzaná v tabuľke nezahŕňa toto rozhodnutie, spôsobilosť fyzikálnej kalibrácie ani prevádzkové straty údajov. Pri nulovej kontrole prechod znamená iba zhodu s referenciou v určenej medzi.

## Kvalifikácia pred prvou hlavnou prípravou

Pred získaním kvalifikačných dát sa datuje aparátna príloha s protokolom meraní, počtami, algoritmom prenosu na hlavné prípravy a pravidlami tvorby spoločnej kalibračnej oblasti s pokrytím aspoň 99 % pre štyri bunky. Neistoty modelu prenosu sa uvádzajú osobitne. Schválenie prílohy na základe hlavných výsledkov je neprípustné. Uvedené 95 % intervalové krytie pri hodnotení číselnej predpovede platí pre pravdivé kalibračné hranice; ak zohľadníme aj možnosť ich štatistického zlyhania, z jednoduchého súčtu chýb vyplýva dolná hranica spoločného krytia 94 % za platnosti modelu prenosu. Smerová a číselná falzifikácia sa vykážu ako dva osobitné výsledky.

Kalibračný tím ešte pred začiatkom uzamkne surové dáta, plán meraní, metódy súčasných intervalov neistoty, neistotu prenosu riadenia na uzol a výsledné prípustné fyzikálne a detekčné intervaly. Rovnaké medze platia v oboch epochách. Každý pridelený pokus musí mať stopu alebo odkaz na nemennú stopu a funkčnú telemetriu; pri preukázanom výpadku sa postupuje podľa pevnej kvalifikačnej brány. Poradie rozhodnutí je dané týmito kritériami.

1. Na nezávislých dátach oddeliť prípravu registra, jeho fyzické odfázovanie počas zápisu a chyby Fourierovho odčítania. Zmerať populácie a reálnu aj imaginárnu časť príslušných koherencií pred kontaktom, priebeh viditeľnosti počas kontaktu a maticu odčítania na pevných vstupoch. Pre každý pár hladín použiť normalizovanú viditeľnosť $V_{jk}=|\rho_{jk}|/\sqrt{\rho_{jj}\rho_{kk}}$. Spodná spoločná hranica počiatočnej viditeľnosti čerstvého registra musí byť aspoň 0,99. Pre predhistóriu sa zahrnie samostatne zmerané odfázovanie počas $9T$. Do dynamiky vstupuje rozsah celej počiatočnej matice a odhad $\kappa$ zo samostatného priebehu viditeľnosti. Sústredenie nerozlíšenej chyby prípravy alebo dekódovania do $\kappa$ nekvalifikuje prístroj. Spodná hranica pravdepodobnosti správnej atómovej prípravy nulovej kontroly musí byť aspoň 0,995; aj s neistotou musí horná hranica $S(n_1)$ zostať pod prahom počas celého zápisu.
2. Pre obe obálky musí kalibračný rozsah plochy a vrcholu pri uzle ležať do ±0,5 % nominálu. Po zarovnaní na uzamknutý začiatok a po časovom zrkadlení prípustný horný rozdiel stôp musí byť najviac $0,005g_{\max}$ a rozdiel derivácií so zmeneným znamienkom najviac 1 % nominálnej maximálnej absolútnej derivácie. Započíta sa šírka pásma sondy, oneskorenie aj neistota medzi vzorkami. Overí sa jednopásmový režim pri najkratšej nábehovej alebo zostupnej hrane; kalibračný odhad excitácií mimo pásma a ich detekcie treba zahrnúť do limitov odozvy. Tieto technické medze sú len prvý filter.
3. Do vopred uzamknutých fyzikálnych intervalov štyroch strát sa musí zmestiť obraz **celého** kalibrovaného rozsahu pre skutočné časovanie, tvary, $\kappa$, počiatočný stav, väzby a zahrnuté chyby. V prílohe musí byť reprodukovateľná obálka s rezervou na numerickú chybu; samotný konečný zoznam bodov bez medziľahlej hranice alebo zhoda pri nominále nepostačujú. Rovnako musia úplné matice zámen $N=0,1,2,3$ a nezávislé merania pozadia spĺňať pevné detekčné hranice z návrhu sily pre všetky štyri ramená. Paritné odčítanie bez rozlíšenia požadovaných počtov ich nespĺňa. Tolerancie zahrnujú možné rozdiely v zahrievaní, presluchu odfázovania, úniku, rekombinácii pri trojitom obsadení a odozve počítania. Ak priestor parametrov vrátane neistoty nemožno overiť, štúdia zatiaľ nie je spôsobilá na hlavný zber. Samotný lokálny balík nepriraďuje spôsobilosť žiadnemu prístroju.

## Stav registra, zaslepenie a predhistória

Pre každú zaznamenanú fyzickú prípravu (vrátane vernosti, konkrétnej obálky, prípravy atómov, symbolu predhistórie a počiatočnej viditeľnosti) má model vlastný spoločný stav. Ten pri výpočte entropie zahŕňa všetky nepozorované výsledky registra a strát **v tejto príprave**. Pridelenie ramena dočasne nepozná hodnotiteľ. Spriemerovanie stavov cez zaslepený kľúč by generovalo inú nelineárnu predpoveď.

Počiatočný register pre symbol \(\ell\) má stav \(\rho_A(0)=v_0|f_\ell\rangle\langle f_\ell|+(1-v_0)I/3\), \(\langle j|f_\ell\rangle=e^{-2\pi i\ell j/3}/\sqrt3\). Hlavné ramená používajú \(\ell=0,v_0=1\). V samostatnej diagnostike predpíšeme registrovaný symbol \(\ell=0\) alebo 1 počas náhradného zápisu trvania \(T=0{,}05\) a potom uchováme register \(8T=0{,}40\) bez väzby s hlavným prstencom. Odfázovanie s tým istým \(\kappa\) beží celých \(9T\). Prstenec na začiatku hlavného zápisu je v oboch prípadoch pripravený rovnako a nekorelovaný s registrom. Počas hlavného zápisu pokračuje odfázovanie, takže násobiteľ mimodiagonálneho prvku v čase \(s\) je \(v_0e^{-\kappa s}\). Diagnostická počiatočná viditeľnosť \(v_0=[(3F-1)/2]^9\) je 0,872823 pre H a 0,316478 pre L. Pre oba symboly vychádza H fast/slow 0,14243210 a 0,14262506, L fast/slow 0,22754886 a 0,25208762. Príčina rovnosti dvojice symbolov je unitárna premena registra diagonálna v báze K, s ktorou komutujú všetky zložky generátora. Redukované entropie a atómové pozorovateľné veličiny sa zachovajú. Pre H sa pri tejto predhistórii pôvodný kladný kontrast dokonca mierne obráti.

Pri ideálnom dekódovaní pevného vstupu a nominálnej ploche dá jediné koncové číslo \(F_{\rm end}=(1+2v_0e^{-\kappa T})/3\). Samo neurčuje \(v_0,\kappa\). Pred zberom treba odhadnúť počiatočnú koherenciu a priebeh straty viditeľnosti počas kontaktu na kalibračných dátach oddelene od matice fyzického čítania registra, overiť čisté odfázovanie pri stabilných populáciách a preniesť spoločnú neistotu do predpovedí. Model pre ľubovoľné \(v_0\) predpokladá rovnomerné populácie a ten istý reálny násobiteľ všetkých mimodiagonálnych koherencií po odstránení známej fázy.

### Numerická rezerva H/slow a priesečník

Samostatná integrácia troch podmienených vlnových funkcií sledovala prospektívny bezstratový vývoj od maxima H/slow až po koniec zápisu. Na 1 025 rovnomerných časoch bolo najväčšie \(C=0{,}09434552\) nat pri \(s=0{,}045\), s odstupom 0,09922223 nat od prahu. Pre ľubovoľný čas medzi vzorkami je vzdialenosť stôp od najbližšieho presného vzorkovaného stavu najviac \(d=(\|H_{\rm BH}^{(3)}\|+6g_{\max}+\kappa)\delta t/2\), kde \(\delta t\) je rozstup vzoriek. Vyplýva to z odhadu komutátora a z toho, že odfázovací generátor je \(\kappa\) krát rozdiel projekčného odfázovania a identity. Kontrakcia čiastočnej stopy a kontinuitná hranica entropie v rozmeroch 12 a 3 dávajú odchýlku \(d\ln(11\cdot2)+2h(d)\le0{,}02293542\) nat. Po jej odčítaní zostáva numerická rezerva 0,07628681 nat pred prvým možným zopnutím. Odhad medzi presnými vzorkami je analytický; hodnoty na vzorkách pochádzajú z numerickej integrácie bez certifikovanej intervalovej chyby.

Pre hranicu zmeny oboch entropií používame prirodzený logaritmus a vzdialenosť \(\tfrac12\|\rho-\sigma\|_1\). [Audenaert, A sharp continuity estimate for the von Neumann entropy](https://doi.org/10.1088/1751-8113/40/28/S18)

Jemnejší integrátor s polovičným maximálnym krokom a desaťnásobne menšou relatívnou toleranciou vrátil \(F_\star=0{,}93894920\). Sken po 0,01 medzi 0,92 a 0,99 slúži na opis vypočítaných znamienok. Konečná sieť nevylučuje ďalšie priesečníky medzi bodmi.

Na tejto sieti je \(\Delta=P_\mathrm{fast}-P_\mathrm{slow}\) záporné pri 0,92 a 0,93 a kladné na šiestich bodoch od 0,94 po 0,99. Hodnota na sieti dosahuje 0,05848 pri 0,96 a klesá na 0,03858 pri 0,99; predpoklad monotónnosti by nadhodnotil výsledok skenu.

### Citlivosť bodových predpovedí

Vždy porušíme jediný nominálny predpoklad a prepočítame obe ramená. Pri posune dĺžky zachováme plochu aj fyzikálnu \(\kappa\), pričom koncové meranie nasleduje hneď po pulze. Pri posune plochy zachováme dĺžku aj \(\kappa\). Zmena prahu skúša citlivosť na verziu hypotézy. Prah zostáva pre potvrdzujúci experiment zmrazený.

| Zmena oproti nominálnej hodnote | \(\Delta_H\), menšia / väčšia hodnota | \(\Delta_L\), menšia / väčšia hodnota |
|---|---:|---:|
| \(F \pm 0,002\) | 0,03923 / 0,03794 | −0,02107 / −0,01824 |
| Plocha ±1 % | 0,03983 / 0,03738 | −0,01881 / −0,02071 |
| Dĺžka ±1 % | 0,03848 / 0,03867 | −0,01892 / −0,02047 |
| Prah ±0,005 nat | 0,04009 / 0,03715 | −0,02007 / −0,01931 |

Pri \(v_0=0,995\) a pôvodnej \(\kappa\) sú H fast/slow 0,04161 / 0,00000 a L fast/slow 0,10441 / 0,12441. Aj pri rovnakej **koncovej** vernosti, ak menšiu počiatočnú viditeľnosť vyváži menšie odfázovanie počas zápisu, sa predpovede zmenia na H 0,04053 / 0,00000 a L 0,10224 / 0,12022. Niektoré fyzické miery tým opúšťajú plánovaciu obálku, hoci sa zachovajú znamienka. Tabuľka obsahuje bodové zmeny po jednom parametri. Pre kvalifikáciu aparatúry treba pred hlavnými výsledkami ohraničiť miery aj pre súčasné odchýlky parametrov v nezávisle kalibrovanej oblasti.

## Reprodukcia

Na vyhodnotenie budúcich hardvérových dát má skript aj režim `--controls panel.json`. Pred načítaním hlavného súboru skontroluje počet a intervaly kontrolných meraní. Režim `--controls panel.json --score-plan plan.json --stage-h H.json --stage-l L.json` číta obsah súboru L až po kvalifikovanom úspechu H. Správca úschovy zabezpečí aj skutočné prístupové práva a podpisy súborov. Hlavné dáta, popisy skupín a prípravy musia byť archivované po jednotlivých pokusoch, aby bolo možné nezávisle overiť agregáciu.

Súbor `plan.json` má polia `profile` (A alebo B), `calibration` (pre každú bunku H_fast, H_slow, L_fast, L_slow dvojice dolnej a hornej hranice P, b, f), `codebook` (tieto štyri názvy priradené štyrom rôznym slepým kódom) a `qualified` (dve booleovské hodnoty H a L z uzamknutej nezávislej kontroly). Každý súbor stupňa obsahuje len svoje dva slepé kódy. Pod každým kódom sú tri nezáporné celé čísla `assigned`, `loss`, `missing`. Panel je pole záznamov s kľúčmi `epoch, family, F, shape, n, events, missing`. Vzor štruktúry jednotlivých kontrol a požadované menovatele určuje `control_gate`.

Z tohto priečinka spustite nasledujúce príkazy v prostredí Pythonu 3.12 s knižnicami podľa priloženého súboru. Samostatný skript zostaví Hamiltonián aj sektory s nulou až tromi atómami. Zapečatené balíky nepotrebuje.

```sh
python -m pip install -r requirements.txt
python -B reproduce.py --verify RESULTS.json --protocol PROTOCOL.sk.md --search-designs
```

Prepínač `--search-designs` znovu vyhľadá celé počty príprav. Bez neho program prepočíta fyziku, kontroly, silu uvedených plánov a porovná tabuľky. Parametrom `--output` možno zapísať nový JSON na inú cestu. Pri kontrole fyziky sa pripúšťa numerické zaokrúhlenie a tabuľky v dokumente sa kontrolujú pri uvedenej presnosti. Úplná stopa, hermitovskosť a minimálne vlastné číslo sú kontrolované na vrchole a na štyroch ďalších časoch každej hustotnou maticou vyhodnotenej zostupnej hrany. Súbor výsledkov obsahuje aj skúšku s jemnejším integrátorom a stavy pre obe predhistórie. Platnosť analytickej hranice a fyzikálne predpoklady vysvetľuje TEORIA.sk.md.

Lokálny manifest SHA256SUMS.txt umožňuje kontrolu totožnosti bajtov. Verejná časová pečiatka ani podanie do registra nie sú súčasťou tohto lokálneho balíka.
