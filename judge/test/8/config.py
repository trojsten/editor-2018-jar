variables = {
    "INT_VECTORS": ["hrdinovia","darebaci"],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["N","M","utok","strategia","obrana","vitazstvo"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"N":3,"M":3,"hrdinovia":[8,2,2],"darebaci":[3,7,3]},
        # output
        {"N":2}
    ),

    (
	{"N":3,"M":3,"hrdinovia":[4,2,1],"darebaci":[2,3,1]},
	{"N":2}
    )
]

real_input_output_pairs = [
    ( # input 1
        # input
        {"N":3,"M":3,"hrdinovia":[8,2,2],"darebaci":[3,7,3]},
        # output
        {"N":2}
    ),

    (
	{"N":3,"M":3,"hrdinovia":[4,2,1],"darebaci":[2,3,1]},
	{"N":2}
    )
]

def solve(N,M,hrdinovia,darebaci):
	hrdinovia = list(reversed(hrdinovia))	
	darebaci = list(reversed(sorted(darebaci)))
	while N>0 and M>0:
		damage = M
		while damage and N>0:
			uber = min(damage,hrdinovia[N-1])
			hrdinovia[N-1] -= uber
			damage -= uber
			if hrdinovia[N-1]==0:
				N -= 1
				hrdinovia = hrdinovia[:N]
		damage = N
		while damage and M>0:
			uber = min(damage,darebaci[M-1])
			darebaci[M-1] -= uber
			damage -= uber
			if darebaci[M-1]==0:
				M -= 1
				darebaci = darebaci[:M]

	return N
			


def sprav_vstup(N,M,hrdinovia,darebaci):
	dict_vstup = {"N":N,"M":M,"hrdinovia":hrdinovia,"darebaci":darebaci}
	dict_vystup = {"N":solve(N,M,hrdinovia,darebaci)}
	real_input_output_pairs.append((dict_vstup,dict_vystup))


import random
def RI(a,b):
	return random.randint(a,b)

tc = 10
for _ in range(tc):
	N = RI(1,100)
	M = RI(1,80)
	hrdinovia = [RI(1,100) for _ in range(N)]
	darebaci = [RI(1,100) for _ in range(M)]
	sprav_vstup(N,M,hrdinovia,darebaci)

vzorak = [ 
    ("darebaci=list(reversed(sorted(darebaci)))","Python"),
    ("reverse(hrdinovia.begin(),hrdinovia.end());","C++"),     
    ("utok:=M;","Pascal"), 
    ("strategia=(N==0);if(N)obrana=min(utok,hrdinovia[N-1]);","C++"), #darebaci utocia
    ("IF strategia IS NOT ZERO GOTO 100","Rust"),
    ("utok-=obrana;hrdinovia[N-1]-=obrana;","C++"),
    ("if(!hrdinovia[N-1]){N--;hrdinovia.pop_back();}","C++"),
    ("IF utok IS NOT ZERO GOTO 4","Rust"),
    ("utok:=N;","Pascal"),
    ("strategia=(!M);if(M)obrana=min(utok,darebaci[M-1]);","C++"),				
     #hrdinovia utocia
    ("IF strategia IS NOT ZERO GOTO 100","Rust"),
    ("utok-=obrana;darebaci[M]-=obrana;","Pascal"),
    ("if(!darebaci[M-1]){M--;darebaci.pop_back();}","C++"),
    ("IF utok IS NOT ZERO GOTO 10","Rust"),
    ("IF N IS NOT ZERO GOTO 3","Rust"),
    
]

