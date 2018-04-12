variables = {
    "INT_VECTORS": ["lode"],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["nepouzijestentointnadarmo"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( # sample 00
        # input
        {"lode":[2,4,1,3]},
        # output
        {"lode":[1,3,2,4]}
    ),
]

real_input_output_pairs = [
    ( # input 1
        # input
        {"lode":[2,4,1,3]},
        # output
        {"lode":[1,3,2,4]}
    ),
]

def solve(lode):
	jedna = lode.index(1)
	lavy = (jedna-1+len(lode))%len(lode)
	pravy = (jedna+1)%len(lode)
	
	if lode[lavy] < lode[pravy]:
		lode = list(reversed(lode[:jedna+1])) + list(reversed(lode[jedna+1:]))
	else:
		lode = lode[jedna:] + lode[:jedna]

	return lode


def sprav_vstup(lode):
	dict_vstup = {"lode":lode}
	dict_vystup = {"lode":solve(lode)}
	real_input_output_pairs.append( (dict_vstup,dict_vystup) )

sprav_vstup([1])
sprav_vstup([6,5,4,3,2,1])
sprav_vstup([2,5,4,3,6,1])
sprav_vstup([1,2,3,4,5,6])
sprav_vstup([1,3,4,5,6,2])

import random
N = 10
MAXN = 100

for i in range(N):
	n = random.randint(1,MAXN)
	lode = [i for i in range(1,n+1)]
	random.shuffle(lode)
	sprav_vstup(lode)

vzorak = [ 
    ("for(int i=0;i<4;++i) lode.insert(lode.begin(),47);","C++"),
    ("lode[1]=lode.index(1)-4;lode[0]=len(lode)-4;","Python"),
    ("lode[2]=lode[(lode[1]+1)%lode[0]+4];","C++"),
    ("lode[3]=lode[(lode[1]+lode[0]-1)%lode[0]+4];","C++"),
    ("nepouzijestentointnadarmo = (lode[2]<lode[3]);","C++"),
    ("IF nepouzijestentointnadarmo IS NOT ZERO GOTO 11","Rust"),
    ("lode[4:lode[1]+5]=list(reversed(lode[4:lode[1]+5]))","Python"),
    ("lode[lode[1]+5:]=list(reversed(lode[lode[1]+5:]))","Python"),
    ("nepouzijestentointnadarmo := 47;","Pascal"),
    ("IF nepouzijestentointnadarmo IS NOT ZERO GOTO 12","Go"),
    ("lode[4:]=lode[lode[1]+4:]+lode[4:lode[1]+4]","Python"),
    ("for(int i=0;i<4;++i) lode.erase(lode.begin());","C++")
]


