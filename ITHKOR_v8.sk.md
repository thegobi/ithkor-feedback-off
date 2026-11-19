# ITHKOR v8 — Lokálna informačná kapacita a rast entropie

19. november 2026 · Technický návrh a stav dôkazov

**Hypotéza.** Oblasť $R$ má fyzikálnu kapacitu $C(R)$, ktorá ohraničuje rast jej von Neumannovej entropie $S(\rho_R)=-\mathrm{Tr}(\rho_R\ln\rho_R)$. Návrh dáva dve odlišné merateľné predpovede: časové okno straty častice v otvorenom prstenci a zmenu presunov cez hranicu dvojice v prstenci s pevným počtom častíc. Obe čakajú na laboratórny test. Hardvérové údaje nižšie overujú postup kontroly odčítania.

**Vzťah k v7.** Predošlá verzia uzavrela starší model po negatívnom teste jeho minimálneho variantu na Q109. V8 zavádza nové predpoklady pre Boseho–Hubbardov prstenec. Pôvodný negatívny výsledok naďalej platí pre testovaný variant.

Šesť číslic v zápise prípravy udáva obsadenia uzlov 0 až 5. Časy sú od prípravy v jednotkách $\hbar/J_{\rm in}$, kde $J_{\rm in}$ je referenčná amplitúda vnútorného preskoku. Vo výpočtoch $\hbar=J_{\rm in}=1$. Prirodzené logaritmy dávajú entropiu v natoch a kapacitu kanála v natoch na použitie.

## 1. Odvodené hranice lokálnych zásahov

V sektore troch bozónov na šiestich uzloch je redukovaný stav blokovo diagonálny podľa počtu $n$ v $R$. Pre pravdepodobnosti $p_n$ a normalizované bloky $\rho_n$ platí

$$S(\rho_R)=H(p_n)+\sum_{n:p_n>0}p_n S(\rho_n)\ \geq\ H(p_n).$$

Na jedinom uzle sú bloky jednorozmerné. Nepodmienená lokálna operácia zachovávajúca každé obsadenie preto entropiu nezníži. Pokles vyžaduje zmenu $p_n$, napríklad odchod častice zo sledovaného uzla. Presun cez hranicu uzla je možný aj pri zachovaní počtu v celom prstenci. [Odvodenie pre jeden uzol](2026-11-18-bhm-entropy-clamp/DERIVATION.sk.md)

Na dvojici $R=\{0,1\}$ každá lokálna unitárna operácia zachová spektrum $\rho_R$. Fáza $\pi$ na uzle 0 tak obráti vnútorný prúd pri rovnakej entropii. Úplné odfázovanie v báze obsadení je zmes fázových unitárnych operácií, takže z konkávnosti entropie vyplýva $S_{\rm po}\ge S_{\rm pred}$. V simulovanom príklade pri $t=0{,}60$ klesol prúd z 2,39133 na nulu a entropia vzrástla z 0,80295 na 1,88715 natu. Pri rovnakých $p_n$ bola jej dolná hranica 0,80244 natu. [Výpočet dvojice](2026-11-19-bhm-two-sites/results.json)

## 2. Vetva A — otvorený prstenec a externý register

**Postulát.** Pri uzle 1 prstenca pripraveného v $|300000\rangle$ je trojstavový register. Jeho kalibrovaný kanál $W$ má kapacitu $C_{\rm op}=\max_p I(X;Y)$. Stotožnenie $C(R)=C_{\rm op}$ pre jedno použitie a spustenie stratového impulzu pri prvom nadprahovom vzorkovaní sú dodatočné fyzikálne predpoklady. Signál z registra do aktuátora je fyzicky odpojený. Zvyšná väzba registra, klasický presluch, zahrievanie a zmeny tunelovania potrebujú nezávislé kontroly.

**Predpoveď.** V symetrickom kanáli sú pri spoľahlivosti $F$ obe nesprávne odpovede rovnako pravdepodobné. Pri kroku 0,05 vychádzajú tieto prvé zásahy. Pravdepodobnosť straty zahŕňa každý beh vrátane behov bez udalosti. [Zapečatené predpovede v1.0.0](https://github.com/thegobi/ithkor-feedback-off/blob/334da54a6d8f9a98c17efb182d545f05683bf7f6/2026-11-18-bhm-apparatus-capacity/predictions.json)

| Nastavenie | $F$ | Kapacita (nat/použitie) | Čas zásahu | Pravdepodobnosť aspoň jednej straty |
|---|---:|---:|---:|---:|
| L | 92 % | 0,76439 | 0,40 | 6,1134 % |
| H | 99 % | 1,03568 | 0,55 | 5,4484 % |

**Navrhované meranie.** 560 nezávislých príprav (280 L + 280 H), kalibrácie osobitne. Prvý klik v zjednotení okien $[0{,}375;0{,}425)$ a $[0{,}525;0{,}575)$ sa ráta na všetky pridelené pokusy. Oba jednostranné Fisherove testy musia dosiahnuť $p\le0{,}05$, v skorom okne L > H a v neskorom H > L. Pri účinnosti detektora 80 % a nezávislom pozadí 0,5 % na okno je vypočítaná sila spoločného kritéria 91,97 %. Platí pre uvedený model časovania a detekcie.

V zaslepenej fáze `evaluate.py freeze` spracuje záznamy a vytvorí súbor s odkazom na SHA-256 prideľovacieho kľúča. Správca uloží SHA-256 tohto súboru pred odovzdaním kľúča. Fáza `report` overí odtlačky, identitu pokusov a počty. V párovej softvérovej kontrole sa po akvizícii zhorší symbol H na čitateľnosť L. Každý atómový výsledok aj čas musia byť v oboch kópiách identické. [Protokol](2026-11-18-bhm-feedback-off-power/PROTOCOL.sk.md) · [Vyhodnotenie](2026-11-18-bhm-feedback-off-power/evaluate.py)

## 3. Vetva B — ventil na hranici dvojice v uzavretom prstenci

**Odvodenie.** Nech $H=H_R+H_Q+fV$, kde $Q$ je zvyšok prstenca, $V$ obsahuje hrany 1–2 a 5–0 (každá 0,65), vnútorná hrana 0–1 má silu 1 a interakcia $U=0{,}35$. Všetky členy zachovávajú celkový počet $N=3$. Pri danom okamžitom stave platí

$$\dot S=f\,g(\rho),\qquad g(\rho)=i\,\mathrm{Tr}\!\left([V,\rho](\ln\rho_R\otimes I_Q)\right).$$

Pri čiastočnej stope príspevok $H_Q$ vypadne a $H_R$ iba otáča lokálnu bázu. Logaritmus sa berie na nosiči s limitnou interpretáciou pri nulových vlastných hodnotách. Ak je na strope $g>0$, spoločný nezáporný násobiteľ musí byť v tom okamihu nulový, aby entropia ďalej nerástla. Dĺžku uzavretia ani hodnotu $C$ tento výpočet neurčuje.

**Dve postulované pravidlá.** Do uzavretého modelu prenášame číselné stropy L a H z vetvy A. Pri ostrom pravidle je $f=1$ do prvého dotyku $S=C$, potom trvalo $f=0$. Propagátor sa po uzavretí rozloží na $U_R\otimes U_Q$, takže celé lokálne spektrum aj entropia ostanú konštantné. Pri plynulom pravidle $f=\max(0,1-S/C)$ sa hranica zoslabuje od začiatku. Pre $S(0)<C$ je medzera $C-S(t)=[C-S(0)]\exp[-\int_0^t g(\rho(s))\,ds/C]$ v konečnom čase kladná pri ohraničenom $g$.

**Simulované podpisy.** Pre $|300000\rangle$ dosiahne ostré pravidlo nižší a vyšší strop v časoch 0,57024 a 0,81947. Nech $\Delta J$ označuje rozdiel stredného vnútorného prúdu $i(a_1^\dagger a_0-a_0^\dagger a_1)$ oproti nepozmenenému prstencu v tom istom čase. Pri vyššom strope v $t=0{,}75$ dáva ostré pravidlo $\Delta J=0$, plynulé $+0{,}306$. Pri nižšom strope v $t=2{,}50$ dáva plynulé pravidlo $-1{,}636$. Ide o rozdiely modelových priemerov pred započítaním meracieho šumu. [Výsledky ventilu](2026-11-19-bhm-boundary-valve/results.json)

### Prah alebo spoločný časovač?

**Zmena prípravy.** Pre každý strop ostal časovač nastavený podľa $|300000\rangle$. Po zmene prípravy na $|210000\rangle$ alebo $|111000\rangle$ sa prúd meral v časoch 0,75, 1,00, 1,50 a 2,50, vždy na 2 000 nových kópiách. Pri porovnaní so zapečatenými modelovými predlohami bez trénovania vyšla vyvážená úspešnosť 91,33 % a 99,20 % pri nižšom strope, 99,18 % a 99,95 % pri vyššom (v uvedenom poradí príprav). Vyvážená úspešnosť je priemer úspešností pri dvoch skutočných príčinách. Kalibráciu prístroja model považuje za známu. [Kontrolné súčty](2026-11-19-bhm-preparation-clock/freeze.sha256) · [Výsledky](2026-11-19-bhm-preparation-clock/results.json)

**Neskorá voľba.** Pri vyššom strope dostal stav $|210000\rangle$ v $t=0{,}30$ na uzle 0 impulz $+\pi/2$ alebo $-\pi/2$. Ostrý prah predpovedal zatvorenie v 0,71634 a 0,76344. Pri 8 000 meraniach prúdu na rozhodnutie klesla vyvážená úspešnosť z 80,28 % proti pôvodnému časovaču 0,60430 na 53,93 % proti spoločnému časovaču 0,758 zvolenému podľa ôsmich modelových priemerov. Predpovede boli lokálne uložené s kontrolným súčtom pred generovaním náhodných meraní. Vopred určená dolná hranica spoľahlivosti úspešnosti mala presiahnuť 70 % v každej triede. Pri preladenom časovači vnútorný prúd toto kritérium nesplnil. [Kontrolné súčty](2026-11-19-bhm-delayed-choice/freeze.sha256) · [Výsledky](2026-11-19-bhm-delayed-choice/results.json)

**Priama sonda hranice.** Okolo $t=0{,}74$ je podľa prahu otvorená už iba záporná vetva. Pasívna sonda odhadla zmenu priemeru $N_R=n_0+n_1$ medzi 0,72 a 0,76 na nezávislých kópiách. Pri 8 000 kópiách na rozhodnutie dosiahla vyváženú úspešnosť 86,1 % proti časovaču 0,758 a 77,4 % proti časovaču 0,7381 preladenému na počet častíc. Výsledok platí pre tento konkrétny výber. Najhorší prípad pre pasívnu sondu ostáva neurčený.

Ideálna párová kvantová nedemolačná sonda (QND) odčíta $N_R$ dvakrát na tej istej kópii. Výpočet zahŕňa projekciu po prvom čítaní. Signálom je zmena počtu medzi odčítaniami, takže presun a návrat môžu zostať skryté. Rozhodnutie v prospech prahu vyžaduje nula zmien pri kladnom a aspoň päť pri zápornom impulze. Pri 3 170 kópiách na znamienko (6 340 spolu, 12 680 odčítaní) má pravidlo citlivosť 90,0 %. Cieľom bolo zachytiť aspoň 90 % prahových prípadov pri najviac 5 % falošných poplachov. Tento rozpočet sa dopočítal po primárnom teste. Horná hranica falošného poplachu je 0,87 % pre každý čas v spojitej rodine spoločných pevných časovačov pri nezávislých prípravách, známych parametroch a bezchybnom čítaní. Každý taký časovač má jediný pevný čas pre všetky kópie a obe znamienka. Časovač losujúci čas osobitne pre každú kópiu je mimo tejto hranice. Časovač so znalosťou znamienka môže napodobniť obe uzavretia. [Protokol sondy](2026-11-19-bhm-boundary-probe/PROTOCOL.sk.md) · [Výsledky](2026-11-19-bhm-boundary-probe/results.json)

## 4. Hardvérové výsledky — overenie metodiky čítania

**Hassani a kol.** Na odložených pároch supravodivého qubitu klesla nezhoda čítaní pri zvýšení výkonu z −21 na −15 dBm zo 17,20 % na 11,00 %. Keď sa softvérovo zhoršilo iba prvé čítanie silnej vetvy, očakávaná nezhoda dosiahla 15,71 % pri opisnom zladení priamo na odložených dátach a 17,36 % pri nezávislej kalibrácii. Druhý výsledok každej kópie pritom ostal rovnaký. Pri fyzickej zmene výkonu sa menili oba impulzy. Samotná nezhoda preto neurčuje pravdepodobnosť fyzického preskoku. [Zenodo 8004359](https://zenodo.org/records/8004359) · [Výsledky](2026-11-18-zenodo-readout/results.json)

**Fluxóniový čip TU Delft.** Po fyzicky slabom prvom impulze (50 mV) dosiahla vyvážená vernosť pevného druhého čítania 70,14 %, po silnom (350 mV) 61,53 %. Po softvérovom zhoršení silného prvého čítania bola jeho vernosť na odloženej kalibrácii 60,92 % oproti 60,74 % pri slabom. Rozdiel druhého čítania 8,61 percentuálneho bodu (vnútrosériový 95 % interval 8,23–9,00) po odčítaní rozdielu kontrol s vynechaným prvým impulzom dosiahol 8,09 bodu (7,52–8,67). Prvé čítanie a verifikátor pochádzajú zo samostatných akvizícií. Porovnanie predpokladá prenositeľnú kalibráciu, zachytáva fyzický vplyv nastavenia impulzu a neurčuje jeho mikroskopickú príčinu. [Verejné dáta v2](https://data.4tu.nl/datasets/22122209-2f78-4a66-8d04-fe18ac8b244e/2) · [Výsledky zo surových dát](2026-11-18-fixed-verification/raw_results.json)

## 5. Otvorené postuláty a limity

**Energia prepnutia.** Pri ostrom uzavretí je zmena strednej energie okamžitého Hamiltoniánu $-\langle V\rangle$, teda −0,18080 a −0,24264 v jednotkách $J_{\rm in}$ pri nižšom a vyššom strope. Pri plynulom pravidle platí $d\langle H\rangle/dt=\dot f\langle V\rangle$. Zdroj alebo príjemca práce ostáva neurčený. Zachovanie troch častíc samo osebe neuzatvára energetickú bilanciu.

**Pôvod prahu.** Entropia redukovaného stavu opisuje štatistiku súboru rovnako pripravených kópií. Chýba mikroskopické odvodenie kapacity aj regulátora, ktorý by v jedinom uzavretom behu reagoval na túto entropiu a menil $f$.

**Reálna QND sonda.** Pri nezávisle overenej zatvorenej hranici treba zmerať pravdepodobnosť falošne hláseného presunu $p_{\rm err}$ a stanoviť jej maximálnu prípustnú hodnotu pre cieľovú citlivosť a falošný poplach. Pravidlo nulových zmien pri kladnom impulze je citlivé aj na ojedinelú chybu. Rozpočet pre laboratórium musí zahŕňať aj chyby prípravy, spätné pôsobenie sondy a časový rozptyl. Druhé čítanie pri 0,76 predchádza modelovému uzavretiu zápornej vetvy len o 0,00344 časovej jednotky.

**Empirický stav k 19. novembru 2026.** Medzi identifikovanými verejnými dátami zatiaľ chýba meranie posunu 0,40 → 0,55 pri fyzicky odpojenej spätnej väzbe aj priama sonda hraničného ventilu. Kladný výsledok by vyžadoval porovnanie s bežným spätným pôsobením prístroja a s časovačmi v presne vymedzenej triede. Dostatočne presné dáta nezlučiteľné s predpovedanými presunmi by spochybnili ostré pravidlo pri zvolenom strope a známych parametroch prstenca. Samotné nedosiahnutie štatistickej významnosti na taký záver nestačí. [Kontroly aparatúry](2026-11-18-capacity-fixed-probe/RESULTS.md)

## Čo je dokázané, čo je postulát a čo čaká na laboratórium

| Stav | Tvrdenie a rozsah platnosti |
|---|---|
| Odvodené | Bloková dolná hranica, lokálna unitárna invariantnosť, vymiznutie koherencií v báze obsadení pri úplnom odfázovaní a nerovnosť pre entropiu. Pre daný Hamiltonián platí $\dot S=f g(\rho)$ a po odpojení hranice sa lokálne spektrum zachováva. |
| Postulované | Fyzikálny strop $S\le C(R)$, priradenie kapacity registra, stratový impulz a obe pravidlá ventilu. |
| Simulované | Časy zásahov, prúdy, sila testu, rozlíšiteľnosť časovačov a výsledky ideálnej sondy pri uvedených modeloch. |
| Empiricky zmerané | Qubitové údaje ukazujú citlivosť nezhody na klasifikáciu a rozdiel výstupu pevného verifikátora po fyzicky odlišných impulzoch. |
| Čaká na laboratórium | Posun straty s odpojenou spätnou väzbou, priama sonda hranice s kalibrovaným šumom a energetická bilancia regulátora. |
