variables = {
    "INT_VECTORS": ["bojovnici","nakupneceny"],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["N","Z","M","magia","kuzlo"],
    "STRS": [],
    "FLOATS": []
}

def solve(N,Z,M,bojovnici,nakupneceny,magia):
	M = max(bojovnici)
	sucet = 0
	D = 0
	for i in range(1,N+1):
		if D%2:
			D = (D*magia+sucet%i+47+len(str(D)) ) % 1000
		else:
			D = (D*len(str(sucet))+i%47+magia*31+sucet%len(str(magia)))%1000
		sucet += D
	return (sucet//M + (sucet%M!=0))

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"N": 3, "M": 1, "bojovnici": [20], "nakupneceny":[100], "Z":1000000, "magia":321},
        # output
        {"magia": solve(3,1000000,1,[20],[100],321)}
    ),
]

real_input_output_pairs = [
    ( # sample 00
        # input
        {"N": 3, "M": 1, "bojovnici": [20], "nakupneceny":[100], "Z":1000000, "magia":321},
        # output
        {"magia": solve(3,1000000,1,[20],[100],321)}
    ),
]

import random
def RI(a,b):
	return random.randint(a,b)

def sprav_vstup(N,Z,M,bojovnici,nakupneceny,magia):
	dict_vstup = {"N":N,"Z":Z,"M":M,"bojovnici":bojovnici,"nakupneceny":nakupneceny,"magia":magia}
	dict_vystup = {"magia":solve(N,Z,M,bojovnici,nakupneceny,magia)}
	real_input_output_pairs.append((dict_vstup,dict_vystup))	

tc = 10
for _ in range(tc):
	N = RI(1,100)
	Z = RI(10**7,10**9)
	M = RI(1,10**4)
	bojovnici = [RI(1,10000) for _ in range(M)]
	nakupneceny = [RI(1,100) for _ in range(M)]
	magia = RI(1,1000)
	sprav_vstup(N,Z,M,bojovnici,nakupneceny,magia)

 #Z = D_{i-1}
 #bojovnici[0]=sum(D)
 #bojovnici[1]=momentalna sekunda
 #kuzlo = pomocna premenna
vzorak = [
    ("M=max(bojovnici);Z=0;bojovnici=[0,1];nakupneceny=[];","Python"), 
    ("kuzlo:= Z mod 2;","Pascal"),
    ("IF kuzlo IS NOT ZERO GOTO 9","Rust"),
    ("Z=Z*len(str(bojovnici[0]))+bojovnici[0]%len(str(magia))","Python"),
    ("Z += bojovnici[2] mod 47+magia*31;Z:=Z mod 1000;","Pascal"),
    ("kuzlo:=N-bojovnici[2];bojovnici[2]+=1;bojovnici[1]+=Z;","Pascal"),
    ("IF kuzlo IS NOT ZERO GOTO 2","Rust"),
    ("IF N IS NOT ZERO GOTO 12","Go"),
    ("Z=(len(str(Z))+47+bojovnici[0]%bojovnici[1]+Z*magia)%1000","Python"),
    ("kuzlo:=N-bojovnici[2];bojovnici[2]+=1;bojovnici[1]+=Z;","Pascal"),
    ("IF kuzlo IS NOT ZERO GOTO 2","Rust"),
    ("magia = bojovnici[0] / M + (bojovnici[0]%M!=0);","C++")
]

