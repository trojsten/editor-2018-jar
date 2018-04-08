variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["dumbier", "mandragora","jedna","netopier"],
    "STRS": ["zaklinadlo","recept","zaba"],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"dumbier": 4, "zaklinadlo": "abcd", "mandragora": 5, "recept": "abefg", "zaba":"qwertyuiopasdfghjklzxcvbnm"},
        # output
        {"zaklinadlo": "abefg"}
    ),
]

real_input_output_pairs = [
    ( # input 1
        # input
        {"dumbier": 4, "zaklinadlo": "abcd", "mandragora": 5, "recept": "abefg", "zaba":"qwertyuiopasdfghjklzxcvbnm"},
        # output
        {"zaklinadlo": "abefg"}
    ),
]

vzorak = [
    ("jedna := 0;", "Pascal"),
    ("netopier = zaklinadlo[jedna] - recept[jedna];", "C++"),
    ("jedna := jedna + 1;", "Pascal"),
    ("IF netopier IS NOT ZERO GOTO 10", "Rust"),
    ("netopier=1;", "C++"),
    ("if(jedna==mandragora) {netopier=0; zaklinadlo=recept;}; if(jedna == mandragora || jedna==dumbier) {netopier=0; }", "C++"),
    ("IF netopier IS NOT ZERO GOTO 2", "C++"),
    ("netopier:=1;", "Pascal"),
    ("IF netopier IS NOT ZERO GOTO 100", "C++"),
    ("if zaba.index(recept[jedna-1]) < zaba.index(zaklinadlo[jedna-1]): zaklinadlo = recept", "Python"),
]