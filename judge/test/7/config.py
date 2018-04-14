variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["N","rozkladac"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"N":44},
        # output
        {"N":47}
    ),
]

real_input_output_pairs = [
    ( # input 01
        # input
        {"N":44},
        # output
        {"N":47}
    ),
]

def notprime(N):
	i = 2
	while i*i<=N:
		if N%i==0:
			return True
		i+=1
	return (N==1)		

def solve(N):
	while notprime(N):
		N+=1
	return N

def sprav_vstup(N):
	vstup = {"N":N}
	vystup = {"N":solve(N)}
	real_input_output_pairs.append((vstup,vystup))	

sprav_vstup(1)
sprav_vstup(47)

tc = 20
MAXN = 1000
import random
for i in range(tc):
	sprav_vstup(random.randint(1,MAXN))

vzorak = [
    ("rozkladac = 0;","Rust"),
    ("N+=(1==N);for(int i=2;i*i<=N;++i)if(N%i==0)rozkladac=1;","C++"),
    ("N++;","C++"),
    ("IF rozkladac IS NOT ZERO GOTO 1","Go"),
    ("N = N-1;","Rust")
]
