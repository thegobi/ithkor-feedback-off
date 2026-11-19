# Vnútorný prúd a entropia dvoch uzlov

Na dvojici uzlov možno zastaviť prúd bez straty bozónu. Samotné rozladenie fázy však nie je kompresiou von Neumannovej entropie. V tomto teste entropia po rozladení vzrástla.

## Čo sa dá odvodiť

Pri pevnom celkovom počte častíc je lokálny stav dvojice blokovo diagonálny podľa počtu n častíc v oblasti. V jednom bloku môžu byť superpozície rôznych rozdelení n medzi uzly. Pri pravdepodobnostiach pₙ a normalizovaných blokoch ρₙ platí S(ρ_R) = H(pₙ) + Σ pₙ S(ρₙ). Preto H(pₙ) je dolná hranica pri zachovaní týchto pravdepodobností. Jediný uzol má v každom bloku jediný stav. Zatiaľ čo na dvoch uzloch pribudne vnútorný prúd, ľubovoľná unitárna operácia výlučne vo dvojici stále zachová celé spektrum ρ_R a tým aj jeho entropiu. Napríklad fáza π na uzle 0 obrátila znamienko prúdu bezo zmeny entropie.

Úplné rozladenie fázy v báze obsadení je priemerovanie lokálnych fázových unitárnych operácií. Z konkávnosti entropie vyplýva S(po) ≥ S(pred), aj pri čiastočnom rozladení zmiešaním s identitou. Taký kanál môže zachovať počet častíc a zároveň zmeniť energiu prstenca. Po nepozorovanom rozladení je globálny stav všeobecne zmiešaný a entropia dvojice už sama nemeria len previazanie so zvyškom.

## Malý výpočet

Použitý bol pôvodný šesťuzlový Hamiltonián v celom sektore N = 3 (56 bázových stavov), príprava |300000⟩, U = 0,35, preskok cez hranicu dvojice 0,65 a vnútorný preskok 1. Prahy sú prenesené z jednorazového trojstavového registra ako ilustračný predpoklad. Šesťuzlový Hamiltonián dvojici taký register nepriraďuje. Časy sú v jednotkách inverzného vnútorného preskoku, entropie v natoch. Presné stredné hodnoty sú bez meracieho šumu.

| C | Prvý vzostupný priesečník v zachytenom intervale | Prvá kontrola nad C (krok 0,05) | S pred | Minimum H(pₙ) pri pevnom pₙ | S po úplnom rozladení | J pred → po |
|---:|---:|---:|---:|---:|---:|---:|
| 0,76439 | 0,57024 | 0,60 | 0,80295 | 0,80244 | 1,88715 | 2,39133 → 0 |
| 1,03568 | 0,81947 | 0,85 | 1,06093 | 1,05702 | 2,12355 | 2,14290 → 0 |

Pri kroku 0,05 v oboch prípadoch samotné H(pₙ) prevyšuje strop. Ak rozdelenie počtu častíc v dvojici zostane rovnaké, taký prebytok sa nedá odstrániť ani úplným vyčistením vnútorných blokov. Záver o výške prebytku závisí od okamihu kontroly. Pri vyššom prahu a kroku 0,005 je v čase 0,820 už S > C, ale ešte H(pₙ) < C. Lokálna unitárna operácia ani vtedy entropiu nezníži.

Kontrolné úplné rozladenie dalo globálne stopové vzdialenosti 0,82737 a 0,86938 a zmeny očakávanej energie −0,57794 a −0,63967. Veľká odozva prúdu preto sama osebe neurčuje mechanizmus.

## Čo dokáže uzavretý prstenec

Ako kontrolný príklad sme na prvom nadprahovom vzorku jednorazovo aplikovali inverzný unitárny vývoj celého prstenca až po stav pri priesečníku a pokračovali s pôvodným Hamiltoniánom. Táto operácia zachováva počet častíc aj rozdelenie energie pôvodného Hamiltoniánu. Zapája preskoky cez hranicu dvojice. Návrat vopred známej trajektórie je konštrukcia závislá od prípravy, nie odvodený autonómny zákon. Po obnovení pôvodného vývoja môže dvojica hranicu znovu prekročiť.

Pri kroku 0,05 vyšlo d = 0,06142 a 0,06300. Odchýlky prúdu od nerušenej referencie sú pri oneskoreniach 0, 0,25, 0,50 a 1 po operácii:

| C | ΔJ(0) | ΔJ(+0,25) | ΔJ(+0,50) | ΔJ(+1) |
|---:|---:|---:|---:|---:|
| 0,76439 | −0,02333 | +0,06787 | +0,12228 | +0,08514 |
| 1,03568 | +0,06950 | +0,12539 | +0,12840 | +0,02819 |

Pri kroku 0,005 klesá d na 0,00983 a 0,00109. Pri kontrole presne na priesečníku by tento konkrétny zásah mal nulovú silu. Hodnota d ≥ 0,00914 bola nutnou podmienkou odozvy veľkosti približne 0,0548 z nerovnosti |ΔJ| ≤ 6d. Nie je to prah štatistickej detekcie. Klasifikátor s 8 000 meraniami nebol na týchto zásahoch testovaný.

**Otvorený postulát.** Pre skutočnú predpoveď treba nezávisle určiť význam kapacity dvojice a fyzikálnu väzbu so zvyškom prstenca, ktorá pri prahu obmedzí ďalší rast entropie. Samotná podmienka S = C neurčuje operáciu, znamienko prúdu ani konečnú veľkosť impulzu.

Reprodukcia z tohto adresára: `python run.py`. Skript používa NumPy a zdieľanú implementáciu pôvodného BHM prstenca.
