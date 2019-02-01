import random
import matplotlib.pyplot as plt

def randlist(n, a=0, b=10):
	final = []
	for i in range(n):
		final.append(random.randint(a, b))
	return final

def moyenne(l):
	somme = 0
	for i in l:
		somme = somme + i
	return somme/(len(l)*1.0)

def histo(l):
	final = dict()
	for i in l:
		compteur = 0
		for y in l:
			if(i == y):
				compteur = compteur + 1
		final[i] = compteur
	return final

def histo_trie(l):
	final = []
	inter = histo(l)
	key = inter.keys()
	val = inter.values()
	for i in range(len(key)):
		indice = 0
		mini = val[indice]
		enlever = key[indice]
		for j in range(len(key)):
			if(val[j] < mini):
				mini = val[j]
				enlever = key[j]
				indice = j
		final.append((mini, key[indice]))
		key.remove(enlever)
		val.remove(mini)
	return final

def paquet():
	final = []
	couleur = ["C","K","P","T"]
	for i in couleur:
		for j in range(1,14):
			final.append((j,i))
	return final

def meme_position(p,q):
	final = []

	for i in range(len(p)):
		if(p[i]==q[i]):
			final.append(i)
	return final

def proba(nombre):
	compteur = 0

	for i in range(nombre):
		a = paquet()
		b = paquet()
		random.shuffle(a)
		random.shuffle(b)
		compteur = compteur + len(meme_position(a,b))

	return compteur/(nombre*52.0)

def graph_proba():
	moyenne = []
	nombre = []
	for i in range(1000, 50000, 1000):
		nombre.append(i)
		moyenne.append(proba(i))
	plt.plot(nombre, moyenne)
	plt.show()

def de():
	return random.randint(1,6)

def proba_somme(k,n):
	final = []
	listesomme = []
	for i in range(n):
		somme = 0
		for j in range(k):
			somme = somme + de()
		listesomme.append(somme)
	inter = histo_trie(listesomme)
	for i,j in inter:
		final.append((j,i*100.0/n))
	return final

def roulette(distribution):
	distriBis = distribution
	lancer = random.random()
	pourcentage = []
	valeur = []
	print(distriBis)
	for i, j in distriBis:
		mini = distriBis[0]
		for x, y in distriBis:
			if(y < mini[1]):
				mini = (x, y)
		a, b = mini
		pourcentage.append(b)
		valeur.append(a)
		distriBis.remove(mini)
	pourcentage.append(distriBis[0][1])
	valeur.append(distriBis[0][0])
	for i in range(len(pourcentage)-1):
		if(lancer < pourcentage[i]):
			return valeur[i]
	return valeur[len(pourcentage)-1]

#liste = randlist(5)
#print(liste)
#print(moyenne(liste))
#print(histo(liste))
#print(histo_trie(liste))
#print(paquet())
#liste = paquet()
#random.shuffle(liste)
#print(liste)
#print(meme_position(paquet(), liste))
#print(proba(100000))
#graph_proba()
#print(de())
#print(proba_somme(2,5))
print(roulette([('P',0.7), ('F',0.3)]))