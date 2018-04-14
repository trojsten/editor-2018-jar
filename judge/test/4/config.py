variables = {
    "INT_VECTORS": ["vylepsi","urychlenie","teraz","potom"],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": ["N","naverbovanie","zlato","vestba","cena","iha","joj","kuk","lol","armada"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
    ({"zlato":20,"vestba":10,"cena":3,"naverbovanie":10,"N":3,"vylepsi":[10,5,4],"urychlenie":[4,3,1]},
     {"armada":2}),
]

real_input_output_pairs = [
  ({"zlato":20,"vestba":10,"cena":3,"naverbovanie":10,"N":3,"vylepsi":[10,5,4],"urychlenie":[4,3,1]},
     {"armada":2}),
]

def solve(args):
	zlato,vestba,cena,naverbovanie,vylepsenie,urychlenie = args
	N = len(vylepsenie)
	best = 0
	teraz = [0 for _ in range(zlato+1)]
	potom = [0 for _ in range(zlato+1)]
	
	for iha in range(N):
		for joj in range(zlato+1):
			potom[joj] = max(potom[joj],teraz[joj])
			if joj+vylepsenie[iha] <= zlato:
				potom[joj+vylepsenie[iha]] = max(potom[joj+vylepsenie[iha]],teraz[joj]+urychlenie[iha])
		teraz,potom = potom,teraz

	for iha in range(zlato+1):
		best = max(best,min(vestba//(max(1,naverbovanie-teraz[iha])),(zlato-iha)//cena))
	return best

nazvy = ["zlato","vestba","cena","naverbovanie","vylepsi","urychlenie"]

def sprav_vstup(args):
	vstup = {nazvy[i] : args[i] for i in range(len(args))}
	vstup["N"] = len(args[-1])
	vystup = {"armada": solve(args) }
	real_input_output_pairs.append( (vstup,vystup) )
		
sprav_vstup([10,5,2,1,[1],[1000]])
sprav_vstup([1,1000000000,2,1,[1],[1000000000]])
sprav_vstup([100,1,1,1000,[10,80,19],[900,1,98]])

tc = 15
import random
limit = [100,10000,20,10000]
for _ in range(tc):
	args = [ random.randint(1,limit[i]) for i in range(4) ]
	N = random.randint(1,20)
	args.append([random.randint(1,60) for _ in range(N) ])
	args.append([random.randint(1,5000) for _ in range(N) ])
	sprav_vstup(args)

TC = 10
LIMIT = [100,100,1,1000000000]
for _ in range(TC):
	args = [ random.randint(1,limit[i]) for i in range(4) ]
	N = random.randint(1,20)
	args.append([random.randint(1,60) for _ in range(N) ])
	args.append([random.randint(1,1000000000) for _ in range(N) ])
	sprav_vstup(args)
	 
vzorak = [ 
    ("teraz,potom=[[0 for _ in range(zlato+1)] for i in range(2)]","Python"),
    ("kuk=joj+vylepsi[iha];lol=teraz[joj]+urychlenie[iha];","C++"),
    ("if(kuk<=zlato)potom[kuk]=max(potom[kuk],lol);","C++"),
    ('joj+=1;kuk=(kuk<=zlato);',"C++"),
    ("IF kuk IS NOT ZERO GOTO 2","Go"), #dalsi stlpec
    ("iha+=1;kuk=(iha<N);joj=0;teraz=potom;","C++"), 
    ("IF kuk IS NOT ZERO GOTO 2","Go"), #dalsi riadok
    ("iha=zlato+1;","Rust"),
    ("joj=(zlato-iha+1)/cena;","C++"),
    ("kuk=vestba/(max(1,naverbovanie-teraz[iha-1]));","C++"),
    ("armada = max(armada,min(joj,kuk));iha--;","C++"),
    ("IF iha IS NOT ZERO GOTO 9","Go")
]


