# Mení kapacita registra pri pevnom impulze výsledok druhého čítania?

Dve verejné štúdie umožňujú overiť časti porovnania. Na posúdenie ITHKOR by sme potrebovali meniť kapacitu susedného registra pri rovnakej príprave, rovnakom impulze na čipe a porovnateľnom teple a presluchu. Čas straty by muselo merať nezávislé druhé čítanie vo viacerých časoch. Takú kombináciu sme v skúmaných dátach nenašli.

## Arnold a kol.

Na obr. 2 zachytávajú dva prijímače ten istý odrazený mikrovlnný impulz súčasne. Z histogramov 10 000 príprav každého stavu vychádza úspešnosť mikrovlnnej vetvy 88,685 % a optickej 85,535 %. Prah sme v každej vetve vybrali podľa najlepšej vyváženej presnosti na archivovaných histogramoch. Z dvojstavových matíc zámen vychádza Shannonova kapacita takto dekódovaného kanála 0,34350 a 0,28798 natu na použitie. Tieto hodnoty opisujú čitateľnosť výstupu. Obe vetvy sledovali jeden fyzický priebeh qubitu. [Článok, obr. 2 a 4](https://www.nature.com/articles/s41567-024-02741-4) · [Archív meraní](https://zenodo.org/records/14033026)

Na obr. 4a autori merali ten istý qubit dvakrát mikrovlnným prijímačom. Počas prvého čítania aplikovali optický impulz. Menili frekvenciu opakovania pri pevnom jednotlivom impulze. Pre každé čítanie sme nastavili osobitný smer a prah na párnych indexoch pri 10 Hz a pri všetkých frekvenciách použili rovnaké pravidlo. Výsledky pochádzajú z nepárnych indexov, 25 000 príprav každého stavu na frekvenciu. Úspešnosť je priemer úspešností pre oba pripravené stavy. Výsledok druhého čítania sa porovnáva s prípravou bez triedenia podľa prvého výsledku. Rozdelenie podľa indexov nekontroluje dlhodobý drift medzi nastaveniami.

| Optické impulzy za sekundu | Prvé čítanie | Kapacita prvého dekódovaného kanála (nat) | Druhé čítanie |
|---:|---:|---:|---:|
| 10 | 94,58 % | 0,4962 | 90,96 % |
| 50 | 93,63 % | 0,4675 | 90,22 % |
| 250 | 88,36 % | 0,3374 | 85,02 % |
| 500 | 82,90 % | 0,2384 | 79,22 % |
| 1 000 | 76,10 % | 0,1457 | 71,76 % |

Pokles druhého výsledku medzi krajnými nastaveniami je 19,208 percentuálneho bodu pred zaokrúhlením. Častejšie pulzy zvýšili priemernú tepelnú záťaž. Autorský model založený na relaxácii a nezávisle zmeranom tepelnom vybudení dobre opisuje nameraný priebeh. Tieto merania neposkytujú samostatný odhad účinku zmeny kapacity registra. [Článok, obr. 4](https://www.nature.com/articles/s41567-024-02741-4)

Reprodukcia vyžaduje Python 3.11+, NumPy a SciPy. Z archívu vyššie stiahnite pôvodný ZIP. Príkaz skontroluje jeho kontrolný súčet a vypíše hodnoty oboch porovnaní.

```sh
python analyze.py AllopticalSCQreadout_data.zip
```

## van Thiel a kol.

Pri rovnakom mikrovlnnom čítacom impulze zmenili autori výkon lasera v samostatnom prevodníku. V tabuľke k obr. 3 sa pri prechode z 3,1 na 31 µW zvýšila presnosť prvého čítania zo 70,08 % na 81,42 %. V samostatnej kontrole k obr. 4 zisťovali koherenciu qubitu s vypnutým laserom a pri 3,1 µW. Priemer fitovaných časov podľa označení v zošite bol približne 9,03 a 8,97 µs. Pre vyšší výkon 31 µW táto kontrola chýba. Z týchto dvoch obrázkov preto nemožno zostaviť dvojicu druhých výsledkov pre rovnaké nastavenia ako na obr. 3. [Článok](https://www.nature.com/articles/s41567-024-02742-3) · [Zdrojové zošity](https://zenodo.org/records/14293253)
