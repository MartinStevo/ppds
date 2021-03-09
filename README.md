# Riešenie

Prvou úlohou tohto zadania bolo implementovať ADT vypínač. Samostatný kód sa nachádza v súbore [lightswitch](https://github.com/MartinStevo/ppds/blob/thirdweek/lightswitch) a je použitý aj v úlohe
3 - problém čitateľov a zapisovateľov.

V súbore [readers_writers](https://github.com/MartinStevo/ppds/blob/thirdweek/readers_writers) môžeme vidieť implementáciu problému čitateľov a zapisovateľov. Problém vyhladovania bol riešený pomocou turniketu, a teda bol pridaný jeden semafor naviac.

Otázka 5: Nakoľko problém vyhladovania bol ošetrený, nedochádza k vyhladovaniu zapisovateľov. Samozrejme, ak počty sú rádovo odlišné: počet zapisovateľov (rádovo v jednotkách) a počet čitateľov (rádovo v tisícoch), zapisovateľ sa dostane k údajom neskôr, ale predsa dostane. 

Otázka 7: Vyhladovanie u čitateľov je nepravdepodobné. Už len z dôvodu, že čitatelia pristupujú k údajom naraz. S pomocou turniketu sa dostane na rad aj čitateľ, aj zapisovateľ.

Otázka 10: V súbore [readers_writers_vis](https://github.com/MartinStevo/ppds/blob/thirdweek/readers_writers_vis) je implementácia problému čitateľov a zapisovateľov, rozšírená o vykreslovanie grafov. Na 2D grafoch môžeme vidieť, že ak vyhladovanie zapisovateľov je ošetrené, závislosť počtu zápisov od počtu čitateľov nie je až tak vysoká. Jednotlivé behy programu trvali 20s a bol vybratý počet zapisovateľov [2](https://github.com/MartinStevo/ppds/blob/thirdweek/output/graph_two_writers.png), [5](https://github.com/MartinStevo/ppds/blob/thirdweek/output/graph_five_writers.png) a [10](https://github.com/MartinStevo/ppds/blob/thirdweek/output/graph_ten_writers.png). Cielene neboli do grafov vynesené počty zapisovateľov, ale počty zápisov. Počas behu programu bolo tiež overované, či zápisy vykonávajú všetci zapisovatelia. Správnosť implementácie potvrdzuje [táto snímka](https://github.com/MartinStevo/ppds/blob/thirdweek/output/ten_writers_output.png), kde môžeme vidieť, že pri 15 zápisoch sa vystriedalo všetkých 10 zapisovateľov.
Posledným bodom je súbor [readers_writers_vis_3D](https://github.com/MartinStevo/ppds/blob/thirdweek/readers_writers_vis_3D), kde výstupom je 3D graf. Do grafu boli vynesené počty čitateľov, zapisovateľov a čas zápisu. V porovnaní s predchádzajúcim kódom ostal čas čítania rovnaký (0,5s). Čas zápisu je náhodne generovaný v intervale <0,5;1>. Výstup môžeme vidieť na [3D_graph](https://github.com/MartinStevo/ppds/blob/thirdweek/output/3D_graph.png).
