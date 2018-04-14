

variables = {
    "INT_VECTORS": ["utok"],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["N","M","teplo","zima","akurat","nazvyniesunahoda"],
    "STRS": [],
    "FLOATS": []
}

def solve(N,utok):
	teplo = N
	zima = -1
	while(teplo-zima>1):
		akurat = (teplo+zima)//2
		M = N
		ok = True
		for damage in utok:
			M = min(N,M+akurat-damage)
			if M <= 0: ok = False
		if ok:
			teplo = akurat
		else:
			zima = akurat
	return teplo

sample_input_output_pairs = [
   (
     {"N":10,"M":3,"utok":[3,9,1]},
     {"teplo":2}
 ),
   ( {"N":10,"M":5,"utok":[4,4,4,4,4]},
     {"teplo":3}
),
  ({"N":1234,"M":4,"utok":[911,47,666,420]},{"teplo":solve(1234,[911,47,666,420])})
]

real_input_output_pairs = [
(
     {"N":10,"M":3,"utok":[3,9,1]},
     {"teplo":2}
 ),
   ( {"N":10,"M":5,"utok":[4,4,4,4,4]},
     {"teplo":3}
),
  ({"N":1234,"M":4,"utok":[911,47,666,420]},{"teplo":solve(1234,[911,47,666,420])})
]
	

def sprav_vstup(N,utok):
	vstup = {"N":N,"M":len(utok),"utok":utok}
	vystup = {"teplo":solve(N,utok)}
	real_input_output_pairs.append((vstup,vystup))

sprav_vstup(11,[1,2,3,4])
sprav_vstup(100,[99])
sprav_vstup(100,[100])
sprav_vstup(100,[100,100,100,100,100])
sprav_vstup(17,[17 for _ in range(17)])
sprav_vstup(17,[17 for _ in range(16)])
sprav_vstup(11,[11 for _ in range(20)])

import random
tc = 20
MAXN = 1000000
MAXM = 20
for i in range(tc):
	N = random.randint(1,MAXN)
	M = random.randint(1,MAXM)
	utok = [ random.randint(0,N) for _ in range(M) ]
	sprav_vstup(N,utok)
	
vzorak = [
    ("teplo=N;zima=-1;","Rust"),
    ("akurat=(teplo+zima)/2;M=N;nazvyniesunahoda=0;","C++"),
    ("for x in utok:M=min(N,M+akurat-x);nazvyniesunahoda+=(M<1);","Python"),
    ("if(nazvyniesunahoda){zima=akurat;}else{teplo=akurat;}","C++"),
    ("akurat = (teplo-zima != 1);","C++"),
    ("IF akurat IS NOT ZERO GOTO 2","Go")
]
