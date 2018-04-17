variables = {
    "INT_VECTORS": ["intv"],
    "STR_VECTORS": ["strv"],
    "FLOAT_VECTORS": ["floatv"],
    "INTS": ["intt",],
    "STRS": ["strr"],
    "FLOATS": ["floatt"]
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"intv": [1,2,3,4], "strv": ["abcd","sf"], "floatv": [0.1,0.2,0.3], "intt": 10, 
        "floatt":0.001, "strr":"ddgf"},
        # output
        {"intv": [1,2,3,4], "strv": ["abcd","sf"], "floatv": [0.1,0.2,0.3], "intt": 10, 
        "floatt":0.001, "strr":"ddgf"},
    ),
    ( # sample 00
        # input
        {"intv": [1,2,3,4], "strv": ["abcd","sf"], "floatv": [0.1,0.2,0.3], "intt": 10, 
        "floatt":0.001, "strr":"ddgf"},
        # output
        {"intv": [1,2,3,4], "strv": ["abcd","sf"], "floatv": [0.1,0.2,0.3], "intt": 10, 
        "floatt":0.001, "strr":"ddgf"},
    ),
    ( # sample 00
        # input
        {"intv": [1,2,3,4], "strv": ["abcd","sf"], "floatv": [0.1,0.2,0.3], "intt": 10, 
        "floatt":0.001, "strr":"ddgf"},
        # output
        {"intv": [1,2,3,4], "strv": ["abcd","sf"], "floatv": [0.1,0.2,0.30000000001], "intt": 10, 
        "floatt":0.0010000000001, "strr":"ddgf"},
    )
]

real_input_output_pairs = [
]

vzorak = [
    ("","Python")
]