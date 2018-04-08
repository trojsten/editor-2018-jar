Priecinok pre vsetky testy.

Mal by mat podpriecinky s cislami 1,2,3 .... pocet uloh. Cislo sa musi zhodovat s poradovym cislom ulohy v DB.

Na vyrobenie noveho prikladu treba vyrobit novi priecinok s cislom prikladu a do neho vyrobit subor `config.py` a subor `zadanie.txt`.
`zadanie.txt` obsahuje zadanie.
`config.py` definuje tri premenne `variables`, `sample_input_output_pairs`, `real_input_output_pairs`.
Pre priklad sa pozrite do `tests/0/config.py`.

Po napisani tohto configu preba pustit subor `python3 prepare_task.py --clean --generate --config <cesta ku knofigu>`.

Ak si chcete svoju ulohu aj odtestovat, mozte do configu pridat premennu `vzorak`, ktora defunuje kod vzoraku. 
Nasledne staci pustit `python3 prepare_task.py --clean --test --config <cesta ku knofigu>`.

Premenna `variables` ma tvar dictu s nasledovnymi klucmi. Hodnota pre kazdy kluc je list premennych (aj prazdny), ktore budu mat v tejto ulohe k dispozicii.
```
{
    "INT_VECTORS": ["koza", "capko"],
    "STR_VECTORS": ["vr", "rv"],
    "FLOAT_VECTORS": ["omg", "lol"],
    "INTS": ["bobek", "bobok"],
    "STRS": ["gold", "silver"],
    "FLOATS": ["wilager"]
}        """
```

Premenne `sample_input_output_pairs` a `real_input_output_pairs` su v principe rovnake, akurad jedvna vygeneruje sample a druha realne vstupy/vystupy.
Su to listy, kde kazdy element je dvojica: `input`, output. `input` je stav pamate na zaciatku (nacitane premenne). 
Premenna `output` je dict premennych, ktorych hodnotu na konci pozadujeme (a ich hodnota).
Napriklad ak chceme mat na zaciatku v premennej `koza` `[1,2,3]` a na konci sucet kozy v premennej `bobek`, tak jeden lement v `sample_input_output_pairs` bude:

```
({"koza":[1,2,3]}, {"bobek":6})
```

Podotykam, ze `config.py` je normalny pythonovy skript, takze sa v nom da normalne programovat (dane premenne mozy byt naplnene algoritmicky).