# Čo spraví hranica dvojice pri strope entropie?

Pri vypnutí oboch hraničných preskokov sa entropia dvojice presne ustáli. Prúd vnútri dvojice zostane v okamihu prepnutia spojitý a následne sa môže od nerušeného prúdu odchýliť v oboch smeroch. Plynulé zoslabovanie preskokov tiež rešpektuje strop, ale má iný podpis už pred časom ostrého prepnutia.

## Odvodenie a nové postuláty

Pôvodný Hamiltonián rozdelíme na H = H_R + H_Q + f V. Oblasť R tvoria uzly 0 a 1, Q je zvyšok prstenca. V obsahuje oba pôvodné hraničné preskoky 1–2 a 5–0 so silou 0,65. Vnútorný preskok 0–1 má po celý čas silu 1. Príprava je |300000⟩ a U = 0,35. Výpočet prebieha v úplnej 56-rozmernej báze troch bozónov.

Pre stav ρ je entropia dvojice S = −Tr(ρ_R ln ρ_R). Pri danom okamžitom stave závisí jej časová derivácia od f lineárne:

$$\dot S = f g(\rho),\qquad
g(\rho)=i\,\mathrm{Tr}\!\left([V,\rho](\ln\rho_R\otimes I_Q)\right).$$

Príspevok H_Q sa pri čiastočnej stope stratí a H_R iba mení lokálnu bázu. Vzťah platí na nosiči stavu, pri nulových vlastných hodnotách sa použije limita. Pre konečný rozmer a ohraničené V je okamžitá rýchlosť previazania ohraničená (v Schmidtovej báze sú členy typu √p ln p v limite konečné). Ak pri S = C vychádza g > 0 a dovolíme iba spoločné nezáporné násobenie oboch väzieb, podmienka ďalšieho nerastu vyžaduje v tomto okamihu f = 0. To je odvodená podmienka v zvolenej rodine dynamík.

- **Nový postulát o kapacite.** S dvojice porovnávame s jednorazovou Shannonovou kapacitou symetrického trojstavového registra. Hodnoty C = 0,764391 a 1,035679 natu sú prenesené z predošlého modelu s F = 0,92 a 0,99. Hamiltonián šiestich uzlov ich neurčuje.
- **Nový postulát o mechanizme.** Stav dvojice reguluje spoločný reálny násobiteľ oboch hraničných preskokov. Entropia opisuje rozdelenie výsledkov na opakovaných prípravách. Mikroskopický prvok, ktorý by takto reagoval v jedinom uzavretom prstenci, sme neodvodili.
- **Dve alternatívne pravidlá.** Ostré pravidlo ponechá f = 1 až do prvého dotyku so stropom a potom drží f = 0. Trvanie uzavretia je súčasťou tohto postulátu. Plynulé pravidlo používa f = max(0, 1 − S/C) od začiatku. Pri ňom platí pred dosiahnutím stropu C − S(t) = [C − S(0)] exp(−∫g dt/C); v konečnom čase tak zostáva kladná medzera. Entropia môže aj klesať.

## Predpovede

Časy sú absolútne od prípravy v jednotkách inverzného vnútorného preskoku. ΔJ je rozdiel od prúdu nerušenej trajektórie pri tom istom čase pre operátor i(a₁†a₀ − a₀†a₁). Tabuľka obsahuje presné stredné hodnoty modelu po zaokrúhlení.

| Pravidlo a C | t = 0,75 | 1,00 | 1,50 | 2,50 |
|---|---:|---:|---:|---:|
| Ostré, 0,76439 | +0,217 | +0,584 | +0,629 | −1,600 |
| Plynulé, 0,76439 | +0,360 | +0,672 | +0,595 | −1,636 |
| Ostré, 1,03568 | 0 | +0,264 | +0,507 | −1,354 |
| Plynulé, 1,03568 | +0,306 | +0,586 | +0,526 | −1,519 |

Pri ostrom pravidle sú prvé dotyky v časoch 0,570243 a 0,819473. Tesne pred nimi rástla S rýchlosťou 1,323 a 0,855 natu za časovú jednotku. Následne sa propagátor rozkladá na U_R ⊗ U_Q, takže celé spektrum ρ_R zostáva rovnaké. Pri plynulom pravidle boli najvyššie vzorkované entropie do t = 2,5 rovné 0,67160 a 0,82966 natu. Nerušený prstenec už v čase 1,5 dosiahol 1,29414 natu.

**Energia a pôvod signálu.** Všetky varianty zachovávajú presne tri častice. Pri ostrom prepnutí sa však stredná energia okamžitého Hamiltoniánu zmení o −0,18080 a −0,24264 v jednotkách vnútorného preskoku. Plynulá zmena obdobne dáva d⟨H⟩/dt = ḟ ⟨V⟩. Energetická bilancia regulátora zostáva otvorená. Pre túto známu prípravu by obyčajné naprogramovanie rovnakého priebehu väzby vytvorilo rovnakú krivku. Na rozlíšenie príčin treba vopred meniť prípravu pri rovnakom vonkajšom programe a kontrolovať skutočnú väzbu.

**Overenie.** Ostré pravidlo používa spektrálnu propagáciu, čas priesečníka vypočíta bisekciou; zhoda pri polovičnom vyhľadávacom kroku je lepšia ako 10⁻¹¹. Astra 6.2 nezávisle získala rovnaké časy, prúdy a prácu prepnutia zo Schmidtových hodnôt. Pri plynulom pravidle sme zmenšili krok RK4 z 0,005 na 0,0025. V štyroch uvedených časoch sa ΔJ zmenilo najviac o 4,1 × 10⁻⁹. Ide o jeden model a jednu prípravu bez šumu merania. Kalibrácia 8 000 meraní z umelej fázovej poruchy nebola pre tento mechanizmus overená.

Reprodukcia: `python boundary_valve.py` (NumPy; pôvodné bázy a operátory sa načítajú z výskumného projektu). Úplné hodnoty obsahuje `results.json`.
