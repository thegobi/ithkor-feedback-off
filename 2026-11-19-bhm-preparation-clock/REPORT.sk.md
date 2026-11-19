# Zoplo to podľa hodín alebo podľa stavu dvojice?

Na tej istej príprave 300000 sú oba modely totožné. Po zmene prípravy ostrý prah v oboch testovaných prípadoch predpovedal skoršie zatvorenie oboch hraničných väzieb. Časovač bol pri každom strope pevne nastavený podľa 300000. Vnútorný preskok, počiatočné hraničné preskoky, interakcia aj časy čítania zostali pre všetky prípravy rovnaké. Všetky trajektórie mali tri častice.

Pred simulovaním meraní sme uložili protokol, určili časy z entropie nerušeného vývoja a zapísali kontrolné súčty do freeze.sha256. Ide o vopred uloženú lokálnu predpoveď. Výpočet nemal prístup k žiadnym novým laboratórnym meraniam.

| Strop (nat) | Príprava | Pevný časovač | Predpoveď prahu | Posun prahu oproti hodinám | Vyvážená úspešnosť |
|---:|---|---:|---:|---:|---:|
| 0,76439 | 210000 | 0,57024 | 0,46405 | −0,10619 | 91,33 % |
| 0,76439 | 111000 | 0,57024 | 0,33612 | −0,23412 | 99,20 % |
| 1,03568 | 210000 | 0,81947 | 0,60430 | −0,21518 | 99,18 % |
| 1,03568 | 111000 | 0,81947 | 0,43591 | −0,38356 | 99,95 % |

Šesť číslic určuje počty bozónov na uzloch 0 až 5. Jednotkou času je inverzný vnútorný preskok pri ℏ = 1. Presné modelové rozdiely prúdu medzi prahom a časovačom boli:

| Strop | Príprava | 0,75 | 1,00 | 1,50 | 2,50 |
|---|---|---:|---:|---:|---:|
| nižší | 210000 | +0,03836 | +0,03289 | +0,00155 | +0,00037 |
| nižší | 111000 | +0,05134 | +0,06561 | +0,03862 | −0,03423 |
| vyšší | 210000 | +0,06139 | +0,08727 | +0,01816 | −0,02376 |
| vyšší | 111000 | +0,05288 | +0,10330 | +0,10584 | −0,07897 |

Obe vetvy majú tú istú nerušenú referenciu pre danú prípravu. Preto rozdiel ich odchýlok ΔJ je zároveň rozdiel ich prúdov. Výstup results.json obsahuje aj samostatné odchýlky každej vetvy od referencie. Astra 6.2 nezávisle potvrdila všetky časy a všetkých 16 rozdielov prúdu.

Pri každej novej kombinácii sa skórovalo 2 000 simulovaných rozhodnutí z každej príčiny, vždy so 4 × 2 000 meraniami na jedno rozhodnutie. Žiadne trénovanie. Počty správnych rozhodnutí pre prah a časovač v poradí tabuľky sú 1833/1820, 1996/1972, 1989/1978 a 1999/1999 (vždy z 2000 v každej vetve). Najnižšia dolná hranica súčasne korigovaných Wilsonových intervalov bola 89,09 %, nad vopred zvolenou hranicou 70 %. Intervaly vyjadrujú neistotu simulovanej úspešnosti pri pevnej príprave a parametroch. Pre kontrolnú 300000 sme pri oboch stropoch overili zhodu všetkých siedmich pravdepodobností výsledkov prúdu vo všetkých štyroch časoch. Pri rovnako pravdepodobných príčinách je úspešnosť optimálneho rozlíšenia 50 %.

**Význam pre experiment.** Všetky štyri čítania sa pri nižšom strope uskutočnili po oboch zásahoch. Tam vidíme stopu času zásahu v následnom prúde. Najsilnejšia kombinácia je vyšší strop a 111000; najslabšia je nižší strop a 210000, kde je na konci rozdiel už len 0,00037. Ide o simulácie dvoch konkrétnych pravidiel na známych prípravách s projektívnym šumom. Rozhodovanie používalo presné modelové predlohy a referencie. Prístrojová neistota, drift a chyba prípravy v tomto rozpočte nie sú zahrnuté. Prepínač naprogramovaný osobitne podľa každej prípravy by výsledok prahu mohol presne zopakovať.

Reprodukcia z tohto adresára: `python predict.py` vypíše časové predpovede. `python measure.py` skontroluje uložené súčty, vykoná simuláciu a vypíše výsledky. Vyžaduje NumPy a pôvodný výskumný projekt. Podrobnosti sú v PROTOCOL.sk.md.
