variables = {
    "INT_VECTORS": ["Hrany1","Hrany2","drevo"],
    "STR_VECTORS": ["sekera"],
    "FLOAT_VECTORS": [],
    "INTS": ["N","M","i","j","k","l","m"],
    "STRS": ["pouzivajmaopatrne"],
    "FLOATS": []
}

sample_input_output_pairs = [

]

real_input_output_pairs = [
  
]

def solve(N,M,Hrany1,Hrany2):
	return N-M

def sprav_vstup(subor,real):
	subor = "test/2/les/" + subor
	with open(subor,'r') as f:
		N,M = [int(x) for x in f.readline().strip().split()]
		Hrany1 = []
		Hrany2 = []
		for _ in range(M):
			a,b = [int(x) for x in f.readline().strip().split()]
			Hrany1.append(a)
			Hrany2.append(b)
	dict_vstup = {"N":N,"M":M,"Hrany1":Hrany1,"Hrany2":Hrany2}
	dict_vystup = {"N":solve(N,M,Hrany1,Hrany2)}
	real_input_output_pairs.append( (dict_vstup,dict_vystup))
	
	if real == False:
		sample_input_output_pairs.append( (dict_vstup,dict_vystup))

vstupy = ['h','g','c']

for i,limit in enumerate(vstupy,start=1):
	cur = 'a'
	while ord(cur) <= ord(limit):
		subor = '0' + str(i) + '.' + cur + ".in"
		sprav_vstup(subor,True)
		cur = chr(ord(cur)+1)
		

sprav_vstup("00.sample.a.in",False)

vzorak = [ 
    ("N=N-M;","Rust")
]



