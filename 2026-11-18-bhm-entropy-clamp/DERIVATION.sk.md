# Čo sa dá odvodiť pre uzol 1

Pre R = jeden uzol na šesťuzlovom prstenci s troma bozónmi má lokálny počet hodnoty 0, 1, 2, 3. Pri pevnom celkovom počte sú zvyšné sektory s 3−n časticami navzájom ortogonálne. Redukovaný stav je preto diagonálny, s entropiou H(p) ≤ ln 4 v prirodzených jednotkách. Rovnosť je dosiahnuteľná. Ak kapacitu jednoducho stotožníme s logaritmom rozmeru, k jej prekročeniu nikdy nedôjde.

V03 zaviedol K_eff, kapacitnú nerovnosť a varianty kompresie Π_C. V7 (§§2, 3 a 8) dokumentuje neurčitosť váh, fyzikálnej kapacity, zdroja a projekcie. Voľba jediného uzla, K_eff = H(p), konkrétneho nižšieho C, spôsobu zistenia prekročenia, rodiny kanálov a pravidla výberu ich sily sú dodatočné predpoklady pre tento prstenec.

Lokálne rozfázovanie v báze počtu nemení žiadne p_n v okamihu zásahu. Pre kladný prebytok H(p)−C nemá rovnica H(p_po)=C v tejto rodine nijaké riešenie. Pri spojitom vývoji môže neskoršie premiestňovanie bozónov zmeniť p_n. Na presnom hladkom priesečníku je H=C a okamžitý prebytok nulový. Konečný pulz vyžaduje napríklad diskrétne kontroly či oneskorenie; spojitý regulátor vyžaduje zákon pre rýchlosť korekcie.

Pre lokálny fyzikálny kanál nezávislý od prípravy vzniká jednoduchý rozpor. Každý zo štyroch vlastných stavov počtu má nulovú entropiu. Kanál, ktorý ponechá všetky podprahové vstupy nezmenené, teda zachová tieto štyri projektory a z linearity aj ich rovnomernú zmes. Tá má entropiu ln 4. Pre 0<C<ln 4 tak univerzálna požiadavka na orezanie ľubovoľného neznámeho vstupu zlyhá. Riadenie pri známej príprave a známom časovom rozvrhu pridáva informáciu o stave.

Rovnica H(p_po)=C navyše neobmedzuje lokálnu fázu po operácii. Ak Φ dosiahne cieľ, potom e^(iπn₁) po Φ zachová rovnakú lokálnu entropiu a zmení znamienko okamžitého prúdu na spoji 0–1. Z rovnakej entropie teda nevyplýva jediný prúd. Pre zmiešaný výstup strata entropie uzla nie je automaticky stratou rovnako veľkého previazania uzla so zvyškom prstenca.

Zdroj: ITHKOR Master Theory v7 (24. október 2026, §§ 2, 3 a 8). Mierka predchádzajúcej umelej poruchy: výskumná správa z 18. novembra 2026, experiment bhm-capacity-current.

**Silnejší výsledok pre uzavretý prstenec.** Nech Q je zvyšok prstenca a P_Q(k) projektor na k bozónov v Q. Pre každý stav v sektore N=3 platí p_R(n)=Tr[P_Q(3−n)ρ_Q]. Ak operácia zachová celkový počet a ponechá ρ_Q nezmenené, zachová teda všetky p_R(n) a S_R. Každá nepostselektovaná lokálna stopu zachovávajúca operácia na R ponechá okamžite ρ_Q nezmenené. Čisto lokálne deterministické orezanie entropie jediného uzla preto v pevnom sektore nemá riešenie ani medzi všeobecnými lokálnymi kanálmi. Strata častíc, výber meracieho výsledku alebo väzba cez hranicu menia tieto predpoklady. Bežné premiestňovanie častíc medzi uzlami pôsobí cez hranicu R.
