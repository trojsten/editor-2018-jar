variables = {
    "INT_VECTORS": [],
    "STR_VECTORS": ["mapa"],
    "FLOAT_VECTORS": [],
    "INTS": ["velkostmapy","dlzka","vyska","okuliare"],
    "STRS": [],
    "FLOATS": []
}

sample_input_output_pairs = [
    ( {"velkostmapy":5,"mapa":["HURAS","U####","S#TR#","E####","DKO!!"] },
      {"vyska":3,"dlzka":4}
    ),
]

real_input_output_pairs = [
   ( {"velkostmapy":5,"mapa":["HURAS","U####","S#TR#","E####","DKO!!"] },
      {"vyska":3,"dlzka":4}
    ),
]

	

def solve(velkostmapy,mapa,rozmer):
	if rozmer == "vyska":	
		vyska = 0
		for riadok in mapa:
			if '#' in riadok:
				vyska += 1
		return vyska
	elif rozmer == "dlzka":
		return max([riadok.count('#') for riadok in mapa])	
	else:
		print("CHYBNY ROZMER")
		


def sprav_vstup(velkostmapy,mapa):
	vstup = {"velkostmapy":velkostmapy,"mapa":mapa}
	vystup = {"vyska":solve(velkostmapy,mapa,"vyska"),"dlzka":solve(velkostmapy,mapa,"dlzka")}
	real_input_output_pairs.append((vstup,vystup))	

sprav_vstup(1,["#"])


def nahodnyznak():
	return chr(random.randint(36,91))

tc = 10
MAXVELKOST = 20
import random
for i in range(tc):
	velkost = random.randint(1,20)
	vyska = random.randint(1,velkost)
	dlzka = random.randint(1,velkost)
	mapa = ["" for _ in range(velkost)]
	for i in range(velkost):
		for j in range(velkost):
			mapa[i] += nahodnyznak()

	hornyriadok = random.randint(0,velkost-vyska)
	lavystlpec = random.randint(0,velkost-dlzka)
	
	mapa[hornyriadok] = mapa[hornyriadok][:lavystlpec] + '#'*dlzka + mapa[hornyriadok][lavystlpec+dlzka:]

	mapa[hornyriadok+vyska-1] = mapa[hornyriadok+vyska-1][:lavystlpec] + '#'*dlzka + mapa[hornyriadok+vyska-1][lavystlpec+dlzka:]


	for i in range(hornyriadok,hornyriadok+vyska):
		mapa[i] = mapa[i][:lavystlpec] + '#' + mapa[i][lavystlpec+1:lavystlpec+dlzka-1] + '#' + mapa[i][lavystlpec+dlzka:]

	sprav_vstup(velkost,mapa)

vzorak = [
    ("dlzka=max([r.count('#') for r in mapa])","Python"),
    ("for(auto x:mapa)vyska+=(count(x.begin(),x.end(),'#')>0);","C++")
]
