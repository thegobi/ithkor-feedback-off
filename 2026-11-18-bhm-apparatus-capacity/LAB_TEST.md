# Ako previesť predpoveď na meranie

## Čo fyzicky meniť

Kandidátom je miestny trojstavový pamäťový register. Jedným možným ovládačom je amplitúda jeho zapisovacieho impulzu pri pevnej dĺžke zápisu, uchovania aj čítania. Merateľnou vlastnosťou je spoľahlivosť prenosu symbolu od pripraveného vstupu po fyzický výstup registra. Počet troch spektroskopických hladín určuje iba hornú hranicu tejto kapacity.

Register je pridaná súčasť navrhovanej aparatúry. Tri viazané jednočasticové orbitály samotnej pasce nedávajú strop troch hodnôt obsadenia. Aj jeden orbitál môže v tomto modeli obsahovať nula, jeden, dva alebo tri bozóny. Pre geometrickú alternatívu by bolo potrebné nezávislé pravidlo spájajúce objem alebo povrch s kapacitou.

Pred meraním strát premiešať poradie známych vstupných symbolov a zmerať celú maticu P(výstup | vstup) v každom nastavení. Zachovať aj nečitateľné výsledky ako osobitný výstup. Fixovať hranicu kanála, čas jedného použitia aj dekodér. Pre asymetrickú maticu vypočítať maximum vzájomnej informácie cez vstupné rozdelenia. Najjednoduchšia realizácia vyžaduje tri dostupné vstupy a prenos bez pamäte medzi opakovaniami. V trojstavovom supravodivom obvode už experimentátori namerali asymetrickú priraďovaciu maticu. To dokladá uskutočniteľnosť kalibračnej metódy na inej platforme. [Chen et al., výsledná matica na obr. 4b](https://www.nature.com/articles/s41534-023-00689-6)

## Podmienky pre predpoveď času

Čísla v protokole pochádzajú zo symetrických modelových matíc. Pred odkrytím strát vypočítať z nezávislej kalibrácie interval pre kapacitu a z kontrolnej, neporušenej dynamiky interval pre entropiu aj neistotu hodín. V ideálnom modeli zachová nízke nastavenie čas 0,40 pre kapacity medzi 0,72835 a 0,83101 natu a vysoké nastavenie čas 0,55 pre kapacity medzi 1,00134 a 1,06850 natu (uvedené okraje sú zaokrúhlené). Ak intervaly zasahujú do ďalšieho kroku, vopred uviesť viac prípustných časov. Časy sa vzťahujú na hodiny s krokom 0,05.

## Ako rozhodnúť medzi vysvetleniami

Náhodne striedať obe fyzické nastavenia pri identickej príprave. Nezávisle skontrolovať parametre Hamiltoniánu, dekoherenciu, pozadie a účinnosť detekcie strát pri oboch amplitúdach. Kalibrovať oneskorenie detektora ešte pred testom. Predpovedané impulzy ležia na hraniciach časových košov a aj krátke oneskorenie môže presunúť klik do susedného koša. Archivovať výsledky všetkých opakovaní vrátane behov bez kliku.

Prvá kontrola zmení dekódovanie až na kópii uloženého signálu. Fyzická aparatúra a už zaznamenané straty ostávajú identické. Tak sa overí, či sa hlásená kapacita dá posunúť obyčajnou zmenou analýzy. Druhá kontrola fyzicky odpojí spätnú väzbu na atómy pri zachovaní lokálnej záťaže a preverí presluch zapisovacieho impulzu. Samostatný beh so zapnutým naprogramovaným stratovým impulzom slúži ako pozitívna kontrola. Špecifická predpoveď vyžaduje posun pri fyzickej zmene registra aj bez riadiaceho impulzu. Tieto hardvérové kontroly zatiaľ neboli vykonané.
