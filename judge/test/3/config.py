variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["zlato","vestba","cena","naverbovanie","vylepsenie","urychlenie","armada"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"zlato": 100, "vestba": 50, "cena": 5, "naverbovanie": 10, "vylepsenie": 20, "urychlenie": 2},
        # output
        {"armada":8}
    ),
]

real_input_output_pairs = [
    ( # input 1
        # input
        {"zlato": 100, "vestba": 50, "cena": 5, "naverbovanie": 10, "vylepsenie": 20, "urychlenie": 2},
        # output
        {"armada":8}
    ),
]

def solve(premenne):
	zlato = premenne[0]
	vestba = premenne[1]
	cena = premenne[2]
	naverbovanie = premenne[3]
	vylepsenie = premenne[4]
	urychlenie = premenne[5]
	armada = 0
	while zlato > 0:
		stiham_vyrobit = vestba // naverbovanie
		vladzem_vyrobit = zlato // cena
		armada = max(armada,min(stiham_vyrobit,vladzem_vyrobit))
		zlato -= vylepsenie
		naverbovanie = max(1,naverbovanie - urychlenie)
	return armada

poradie = ["zlato","vestba","cena","naverbovanie","vylepsenie","urychlenie"]

rucne = [
	[1000,1000,1,1,1,1],
	[901,1,1,1000000000,9,10000000],
	[1000,1000000000,47,50000000,666,50000000],
	[1000,200,1,10000000,10,123456],
	[1000,200,1,10000000,10,125001],
	[1000,500,1000,501,1,500]
]

for vstup in rucne:
	dict_vstup = {}
	for i in range(len(poradie)):
		dict_vstup[poradie[i] ] = vstup[i]
	dict_vystup = {"armada":solve(vstup)}
	real_input_output_pairs.append((dict_vstup,dict_vystup))

N = 20
import random
MAX = [1000,10000,50,1000,300,100]
for _ in range(N):
	dict_vstup = {}
	vstup = []
	for i in range(len(poradie)):
		vstup.append(random.randint(1,MAX[i]))
		dict_vstup[poradie[i]] = vstup[i]
	dict_vystup = {"armada":solve(vstup)}
	real_input_output_pairs.append((dict_vstup,dict_vystup))

vzorak = [ 
    ("armada=max(armada,min(vestba//naverbovanie,zlato//cena))","Python"),
    ("naverbovanie=max(1,naverbovanie-urychlenie);","C++"),
    ("zlato-=vylepsenie; if zlato<0 then zlato:=0;","Pascal"),
    ("IF zlato IS NOT ZERO GOTO 1","Rust")
]
