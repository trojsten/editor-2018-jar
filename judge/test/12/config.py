

variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": ["bojovisko"],
    "FLOAT_VECTORS": [],
    "INTS": ["N","wololo","modry","cerveny","modrocerveny","priest"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
   (
     {"N":3,"bojovisko":[ "pPP","PPp","KsP" ] },
     {"wololo": 3 }
 )
]

real_input_output_pairs = [
  (
     {"N":3,"bojovisko":[ "pPP","PPp","KsP" ] },
     {"wololo": 3 }
 )
]

def solve(N,mapa):
	wololo = 0
	for i in range(N):
		modry = True
		for c in mapa[i]:
			if c=='p' and modry:
				modry,wololo = False,wololo+1
			elif c=='P' and modry == False:
				modry,wololo = True,wololo+1
				
	return wololo

def sprav_vstup(N,mapa):
	vstup = {"N":N,"bojovisko":mapa}
	vystup = {"wololo":solve(N,mapa)}
	real_input_output_pairs.append((vstup,vystup))

import random
def randstring(N):
	res = ""
	for _ in range(N):
		r = random.randint(1,4)
		if r==1: res += 'p'
		elif r==2: res += 'P'
		elif r==3: res += chr(random.randint(ord('a'),ord('z')))
		else: res += chr(random.randint(ord('A'),ord('Z')))
	return res

sprav_vstup(1,["p"])
sprav_vstup(1,["P"])
sprav_vstup(1,["o"])

tc = 10
MAXLEN = 20
for i in range(tc):
	N = random.randint(1,MAXLEN)
	mapa = [randstring(N) for _ in range(N)]
	sprav_vstup(N,mapa)
	
vzorak = [
    ("priest=N;","Rust"),
    ("modry=1;cerveny=N;","C++"),
    ("modrocerveny=(modry&&bojovisko[priest-1][N-cerveny]=='p');","C++"),
    ("modrocerveny+=(!modry&&bojovisko[priest-1][N-cerveny]=='P');","C++"),
    ("IF modrocerveny IS NOT ZERO GOTO 12","Rust"),
    ("cerveny-=1;","Rust"),
    ("IF cerveny IS NOT ZERO GOTO 3","Go"),
    ("priest-=1;","Rust"),
    ("IF priest IS NOT ZERO GOTO 2","Go"),
    ("priest=1;","Rust"),
    ("IF priest IS NOT ZERO GOTO 100","Go"),
    ("wololo+=1;modry=!modry;modrocerveny=0;","C++"),
    ("IF wololo IS NOT ZERO GOTO 6","Go")
]
