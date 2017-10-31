Priecinok pre vsetky testy.

Mal by mat podpriecinky s cislami 1,2,3 .... pocet uloh. Cislo sa musi zhodovat s poradovym cislom ulohy v DB.
V kazdom priecinku subory .in a .out

Optimalne nazyvat subory rovanko ako to robime v ksp 01.in ... 10.in, a mat 00.sample.in, lebo pre ten sa im zobrazi
aj rozdiel oproti spravnej odpovedi.

Subor `.in` by mal vyzerat rovanko ako pamatove subory.
Pouzivajte funkciu `prepare_memory` z `runners.run_all`, ktora berie dict, kde poviete ake maju mat premmenne hodnoty,
a cestu-nazov zuboru do ktoreho sa memory ulozi.

Subor `.out` by mal byt json dump dictu, ze ake premenne maju mat ake hodnoty na konci.
