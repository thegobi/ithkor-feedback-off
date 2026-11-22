# Teoretická poznámka k v9

**Čo sa testuje.** Dve opačne orientované obálky tej istej zapisovacej väzby zasiahnu uzol v rozdielnom okamihu jeho vývoja. V hypotéze v9 rozhoduje o strate súbeh dvoch fyzických veličín. Väzba práve slabne a podmienená entropia uzla vzhľadom na register je ešte nad prahom. Predregistrovanou predpoveďou je zmena smeru rozdielu medzi obálkami pri zmene odfázovania registra. Všetky pravdepodobnosti v balíku sú simulácie pred hlavným meraním.

## Z čoho predpoveď vychádza

Zápis v ideálnom štandardnom modeli rozloží spoločný vývoj podľa troch vlastných stavov registra. Diagonálny blok s indexom `j` vidí lokálny potenciál `j g(t) n₁`. Čisté odfázovanie v tej istej báze tlmí len mimodiagonálne bloky. Redukovaný stav prstenca je súčtom diagonálnych blokov, preto je pre **danú obálku** v štandardnom modeli nezávislý od tejto rýchlosti odfázovania. Tvar obálky pritom môže zmeniť energiu aj obsadenia. Štandardný model s uvedeným Hamiltoniánom zachováva celkový počet atómov.

Presná časová reverzia reálnej obálky zachováva jej plochu, maximum, integrál štvorca a veľkosť Fourierovej transformácie. Príprava aj tunelovanie pokračujú v pôvodnom smere času. Rovnaké výkonové spektrum preto povoľuje rozdielne obsadenia vysokých energií počas pulzu. Únik počas pulzu môže byť fyzikálne reálny aj v bežnej otvorenej kvantovej sústave. Nezávislé počítanie atómov po pulze odstraňuje potrebu používať skoré kliky a ponecháva otázku skutočného zahrievania alebo vyrazenia atómu otvorenú. Pre interpretáciu je rozhodujúca aj kontrola bežných strát pri zmene spôsobu odfázovania registra.

## Čo je nový postulát

1. Mieru `S(R|A)` vyhodnocujeme z nepodmienenej spoločnej hustotnej matice oblasti a registra. Vývoj zahrnuje aj prípravy s fyzickou stratou. Pri výpočte pravdepodobnosti prvej straty stačí sledovať úbytok hmotnosti sektora s tromi atómami, pretože v modeli nie je zdroj častíc.
2. Prebytok nad pevným prahom a kladnú časť zápornej derivácie veľkosti väzby násobíme podľa rovnice v protokole. Referenčná amplitúda je kalibrované maximum celej použitej obálky. Hodnota prahu aj zisk pochádzajú z predchádzajúcej modelovej práce. Zisk bol kalibrovaný na skoršom plochom pulze, takže jeho amplitúda na kalibračnom prípade neposkytuje nezávislé overenie.
3. Stratu vykonáva lokálny skok `a₁`. Výber skoku, prahu a zákona pre jeho rýchlosť predstavuje fyzikálnu hypotézu. Samotná kvantová entropia žiadny zo skokov nevyberá.

Po dosadení rýchlosti pozdĺž konkrétneho riešenia má generátor nezáporné Lindbladove sadzby. Zachováva hermitovskosť, stopu a pozitivitu. Mapa zo vstupného stavu na výstup je nelineárna. Výrok o nezávislosti od vzdialenej voľby predpokladá miestne dostupný uzol aj register a sadzbu určenú ich **nepodmieneným** lokálnym stavom. Vzdialená neselektívna operácia na izolovanom systéme tento stav nemení. Počítanie samostatnej sadzby pre každý rozklad zmesi by definovalo inú dynamiku.

Hodnoty ε = 0,193567742 natu a λ = 1,68911 sme prevzali ako zadané čísla z predchádzajúceho výpočtu v9. Desatinné miesta ε určujú reprodukovateľnú hranicu v simulácii. Pre ε nemáme nezávislé experimentálne určenie ani neistotu. Predchádzajúca normalizácia λ používala skorú stratu približne 10 % pri plochom pulze. Všetky návrhové voľby aj obrat znamienka boli známe pred týmto balíkom. Nezávislým testom bude zber nových atómových príprav podľa uzamknutých pravidiel.

## Čo fyzicky znamená chyba pri koncovom počítaní

Nech `P` je predpovedaná pravdepodobnosť aspoň jednej straty v9. Pre experiment treba poznať dve podmienené pravdepodobnosti. Hodnota `b` je pravdepodobnosť zaznamenaného úbytku pri neprítomnosti straty v9. Zahŕňa aj možné bežné úniky z pasce. Hodnota `f` je pravdepodobnosť výsledku „tri atómy“ po skutočnej strate v9. Z pravidla o úplnej pravdepodobnosti potom vyplýva `q=b(1−P)+(1−f)P`. Napríklad pri bežnej strate s pravdepodobnosťou β na preživšej príprave, citlivosti s a špecificite c platí `b=(1−c)+(s+c−1)β`, `f=1−s`, pokiaľ detektor odpovedá rovnako na oba druhy straty. Pri β=0 a s=c=d dostávame nominálne tabuľky. Ak sa odpoveď mení s počtom chýbajúcich atómov, kvalifikácia musí pokryť každý dosiahnuteľný koncový počet.

Na skutočnom zariadení príčinu jednej straty z koncového snímku nevyčítame. Prenos hraníc z kalibračných a kontrolných príprav na hlavné prípravy je predpoklad experimentu. Správne znamienka na meraných počtoch môže vytvoriť aj bežný proces pôsobiaci v hlavných aj kontrolných prípravách. Stačí, aby sa v hlavných prípravách prejavil inou silou alebo aby jeho rozdiel unikol rozlišovacej schopnosti kontrol. Protokol preto osobitne vyhodnocuje, či interval nameraného rozdielu presahuje najväčší rozdiel vysvetliteľný kalibrovaným koncovým kanálom pri rovnakých fyzických mierach.

## Dve kontroly

Pri kontrole s tromi atómami na uzle 1 pripravíme stav priamo pri začiatku zápisu. Z počiatočného sektora vedú iba dva hraničné preskoky so spoločnou normou `v = sqrt(3(1² + 0,65²))`. Diagonálny zápis aj odfázovanie tento sektor zachovávajú. Pravdepodobnosť opustenia sektora do času `T` je najviac `sin²(vT)` pre testovaný čas. Entropiu počtu na uzle potom zhora ohraničuje `h₂(q) + q ln 3`, kde `q = sin²(vT)` a `h₂` používa prirodzený logaritmus. Keďže `S(R|A) ≤ S(R)`, toto dáva rezervu pod spúšťacím prahom počas celého pulzu.

Pri kontrole predhistórie dostanú oba registre rovnakú dobu prípravy a dekoherencie. Známy symbol 1 sa od symbolu 0 líši lokálnou diagonálnou fázovou transformáciou registra. Tá komutuje so zápisom aj odfázovaním. Obe entropie, rýchlosť straty a atómové výsledky sú preto v oboch vetvách identické. Samotná pravdepodobnosť straty môže byť v tejto kontrole kladná.

Numerický priesečník verností sa vzťahuje na pevne zvolenú obálku, prípravu, Lindbladov model a koncový ukazovateľ „menej ako tri atómy“. Úspech na dvoch koncových vernostiach potvrdzuje predpovedané poradie na nich. Na určenie polohy priesečníka z laboratórnych dát treba ďalšie vopred určené vernosti.
