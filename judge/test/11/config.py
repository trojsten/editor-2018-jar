

variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": [],
    "FLOAT_VECTORS": [],
    "INTS": [],
    "STRS": ["General","Plukovnik","Podplukovnik","Strateg","Spion","Programator",
"Velmajstermaxisupergeneralveduci","Nadpodpredzadplukovnikazarovendokoncaajgeneral"],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( {"General":"Zaba","Plukovnik":"Vlejd","Podplukovnik":"Baska","Strateg":"Matus","Spion":"Ralbo","Programator":"Hodobox",
"Velmajstermaxisupergeneralveduci":"Misof","Nadpodpredzadplukovnikazarovendokoncaajgeneral":"Korman"},
      {"General":"Matus","Plukovnik":"Baska","Podplukovnik":"Zaba","Strateg":"Ralbo","Spion":"Hodobox","Programator":"Vlejd",
"Velmajstermaxisupergeneralveduci":"Korman","Nadpodpredzadplukovnikazarovendokoncaajgeneral":"Misof"}
    ),
]

real_input_output_pairs = [
   ( {"General":"Zaba","Plukovnik":"Vlejd","Podplukovnik":"Baska","Strateg":"Matus","Spion":"Ralbo","Programator":"Hodobox",
"Velmajstermaxisupergeneralveduci":"Misof","Nadpodpredzadplukovnikazarovendokoncaajgeneral":"Korman"},
      {"General":"Matus","Plukovnik":"Baska","Podplukovnik":"Zaba","Strateg":"Ralbo","Spion":"Hodobox","Programator":"Vlejd",
"Velmajstermaxisupergeneralveduci":"Korman","Nadpodpredzadplukovnikazarovendokoncaajgeneral":"Misof"}
    ),
]


nazvy = ["General","Plukovnik","Podplukovnik","Strateg","Spion","Programator","Velmajstermaxisupergeneralveduci",
"Nadpodpredzadplukovnikazarovendokoncaajgeneral"]	

def solve(A):
	A = [ A[3],A[2],A[0],A[4],A[5],A[1],A[7],A[6] ]
	return { nazvy[i] : A[i] for i in range(8) }

def sprav_vstup(velkostmapy,mapa):
	vstup = {"velkostmapy":velkostmapy,"mapa":mapa}
	vystup = {"vyska":solve(velkostmapy,mapa,"vyska"),"dlzka":solve(velkostmapy,mapa,"dlzka")}
	real_input_output_pairs.append((vstup,vystup))	

tc = 5
MAXVELKOST = 10
import random
def randstring():
	sz = random.randint(1,MAXVELKOST)
	res = ""	
	for _ in range(sz):
		res += chr(random.randint(ord('A'),ord('Z')))
	return res

for i in range(tc):
	tituly =  [randstring() for _ in range(8)]
	vstup = {nazvy[i] : tituly[i] for i in range(8)}
	vystup = solve(tituly)
	real_input_output_pairs.append((vstup,vystup))
	
vzorak = [
    ("swap(Spion,Nadpodpredzadplukovnikazarovendokoncaajgeneral);","C++"),
    ("swap(Spion,Velmajstermaxisupergeneralveduci);","C++"),
    ("swap(Spion,Nadpodpredzadplukovnikazarovendokoncaajgeneral);","C++"), #ti dvaja su uz done
    ("General,Strateg,Spion = Strateg,Spion,General","Python"),
    # strateg general done, general je v spionovi
    ("swap(Spion,Podplukovnik);swap(Spion,Plukovnik);","C++"),
    ("swap(Spion,Programator);","C++")
]
