# Riešenie

V tejto vetve sa nachádzajú úlohy 10. týždňa, t.j. riešenia 9. cvičenia.

Súbor [array](https://github.com/MartinStevo/ppds/blob/tenthweek/array.py) obsahuje implementáciu násobenia prvkov matice.

Rozšírenie predchádzajúcej úlohy zo seminára, a teda práca s 2D polom sa nachádza v súbore [2Darray](https://github.com/MartinStevo/ppds/blob/tenthweek/2Darray.py)

Keďže cieľom cvičenia bolo vymyslieť a implementovať vlastnú úlohu, rozhodol som sa pre jpg codec. V súbore [jpg_codec](https://github.com/MartinStevo/ppds/blob/tenthweek/jpg_codec.py) môžeme vidieť jeho čiastočnú implementáciu. Prvým krokom je import obrázka a prevod do grayscale, nakoľko práca s jedným poľom je jednoduchšia. Ďalším krokom je diskrétna kosínusová transformácia. Na toto bola použitá knižnica scipy. Funkcia dct2 predstavuje využitie dct pre prácu s 2D poľom. Obdobne to platí aj pre idct2. Po aplikovaní dct sa každý výrez poľa 8x8 predelí kvantizačnou maticou. Toto prebieha s podporou CUDA. Výsledok by sa mal kódovať "po uhlopriečkach" do súboru. Nakoľko toto nie je cieľom cvičenia a ďalší krok by predstavoval import a dekódovanie, bolo kódovanie vynechané. Po vynásobení kvantizačnou maticou (opäť s podporou CUDA) je aplikovaná idct. Výsledný imshow obrázka pred a po potvrdzuje, že úloha bola správne implementovaná.
