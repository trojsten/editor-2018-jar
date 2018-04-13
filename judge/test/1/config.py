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

def solve(a,b,abeceda):
	sz = min(len(a),len(b))
	if a == b[:sz]:
		return a
	if b == a[:sz]:
		return b
	for i in range(sz):
		if a[i] != b[i]:
			if abeceda.index(a[i]) > abeceda.index(b[i]):
				return b
			return a

N = 10
MAXLEN = 100
import random
for i in range(N):
	sz = random.randint(2,MAXLEN)
	string = ""
	for _ in range(sz):
		string += chr(ord('a')+random.randint(0,25))
	string2 = ""
	if i==0:
		string2 = string[:] # jeden vstup kde su rovnake
	else:
		usekni = random.randint(1,sz-1)
		string2 = string[:-usekni-1]	
		if i!=1: # i==1 je vstup kde jedno je prefixom druheho
			pridaj = random.randint(1,usekni)
			for _ in range(pridaj):
				string2 += chr(ord('a')+random.randint(0,25))
	tmpbeceda = [i for i in range(ord('a'),ord('z')+1,1)]
	random.shuffle(tmpbeceda)
	abeceda = ""
	for i in range(26):
		abeceda += chr(tmpbeceda[i])
	

	dict_vstup = {"dumbier":len(string), "zaklinadlo":string, "mandragora":len(string2), "recept":string2, "zaba":abeceda}
	dict_vystup = {"zaklinadlo":solve(string,string2,abeceda)}
	pair = (dict_vstup,dict_vystup)
	real_input_output_pairs.append(pair)

	dict_vstup = {"dumbier":len(string2),"zaklinadlo":string2,"mandragora":len(string),"recept":string,"zaba":abeceda}
	dict_vystup = {"zaklinadlo":solve(string,string2,abeceda)}
	pair = (dict_vstup,dict_vystup)
	real_input_output_pairs.append(pair)	

vzorak = [
    ("netopier = zaklinadlo[jedna] - recept[jedna];", "C++"),
    ("jedna := jedna + 1;", "Pascal"),
    ("IF netopier IS NOT ZERO GOTO 10", "Rust"),
    ("netopier:=1;", "Pascal"),
    ("if(jedna==mandragora){netopier=0;zaklinadlo=recept;}","C++"),
    ("if(jedna==mandragora||jedna==dumbier) netopier=0;","C++"),
    ("IF netopier IS NOT ZERO GOTO 1", "Rust"),
    ("netopier:=1;", "Pascal"),
    ("IF netopier IS NOT ZERO GOTO 100", "Go"),
    ("dumbier=zaba.index(recept[jedna-1])", "Python"),
    ("mandragora=zaba.index(zaklinadlo[jedna-1])","Python"),
    ("if (dumbier<mandragora) swap(zaklinadlo,recept);","C++")
]
