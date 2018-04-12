variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["N","P","Vlejd","Baska","kopijnik","lukostrelec","delostrelec","musketier"],
    "STRS": ["V","B"],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"N":1,"P":47,"Vlejd":46,"Baska":48},
        # output
        {"V":"Baska"}
    ),
( # sample 01
        # input
        {"N":1,"P":47,"Vlejd":49,"Baska":48},
        # output
        {"V":"Remiza"}
    ),
( # sample 02
        # input
        {"N":3,"P":47,"Vlejd":14,"Baska":20},
        # output
        {"V":"Vlejd"}
    ),
( # sample 03
        # input
        {"N":123456789,"P":47,"Vlejd":14,"Baska":20},
        # output
        {"V":"Vlejd"}
    ),
]

real_input_output_pairs = [
    ( 
        # input
        {"N":1,"P":47,"Vlejd":46,"Baska":48},
        # output
        {"V":"Baska"}
    ),
( 
        # input
        {"N":1,"P":47,"Vlejd":49,"Baska":48},
        # output
        {"V":"Remiza"}
    ),
(
        # input
        {"N":3,"P":47,"Vlejd":14,"Baska":20},
        # output
        {"V":"Vlejd"}
    ),
( 
        # input
        {"N":123456789,"P":47,"Vlejd":14,"Baska":20},
        # output
        {"V":"Vlejd"}
    ),
]

def solve(args):
	N,P,Vlejd,Baska = args
	V = [False for i in range(Vlejd)]
	B = [False for i in range(Baska)]
	delostrelec = N
	kopijnik,lukostrelec=P%Vlejd,P%Baska
	while True:
		if kopijnik == lukostrelec:
			return "Remiza"
		if kopijnik > lukostrelec:
			delostrelec-=1
			lukostrelec = (lukostrelec*P)%Baska
			if delostrelec==0 or B[lukostrelec]:
				return "Vlejd"
			B[lukostrelec] = True
		else:
			N-=1
			kopijnik = (kopijnik*P)%Vlejd
			if N==0 or V[kopijnik]:
				return "Baska"
			V[kopijnik] = True

def sprav_vstup(N,P,Vlejd,Baska):
	dict_vstup = {"N":N,"P":P,"Vlejd":Vlejd,"Baska":Baska}
	dict_vystup = {"V":solve([N,P,Vlejd,Baska])}
	real_input_output_pairs.append((dict_vstup,dict_vystup))

import random
def RI(a,b):
	return random.randint(a,b)

N = 10

for i in range(N):
	sprav_vstup(RI(1,1000000000),RI(1,1000),RI(1,100),RI(1,100))
	sprav_vstup(RI(1,10),RI(1,1000),RI(1,100),RI(1,100))
# niektore C++ riadky su akoze v Go. ale Go mi nefunguje idk why :(
vzorak = [ 
    ("V=string(Vlejd,'0');B=string(Baska,'0');delostrelec=N;","C++"),
    ("kopijnik := P mod Vlejd; lukostrelec := P mod Baska;","Pascal"),
    ("if(kopijnik==lukostrelec){musketier=1;}else{musketier=0;}","C++"),
    ("IF musketier IS NOT ZERO GOTO 17","Rust"),
    ("if(kopijnik>lukostrelec){musketier=1;}else{musketier=0;}","C++"),
    ("IF musketier IS NOT ZERO GOTO 12","Rust"),
    ("N-=1;kopijnik:=(kopijnik*P) mod Vlejd;","Pascal"),
    ("musketier=(N==0 || V[kopijnik]=='1');","C++"),
    ("IF musketier IS NOT ZERO GOTO 19","Rust"),
    ("V[kopijnik]='1';","C++"),
    ("IF P IS NOT ZERO GOTO 3","Rust"),
    ("delostrelec-=1;lukostrelec:=(lukostrelec*P) mod Baska;","Pascal"),
    ("musketier=(delostrelec==0 || B[lukostrelec]=='1');","C++"),
    ("IF musketier IS NOT ZERO GOTO 18","Rust"),
    ("B[lukostrelec]='1';","C++"),
    ("IF P IS NOT ZERO GOTO 3","Rust"),
    ('V="Remiza";',"C++"),
    ('if(V!="Remiza"){V="Vlejd";}',"C++"),
    ('if(V!="Vlejd" && V!="Remiza"){V="Baska";}',"C++"),
    
]




