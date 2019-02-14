import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


nom = ["aleatoire"]
l=[0.1,0.2,0.3]

def jouer(machine, levier):
	if(random.random() < machine[levier]):
		return 1
	else:
		return 0

def genere(nombre):
	machine = []
	gain = []
	esperance = []
	moyenne = []
	coups = []
	recolte = []
	for i in range(nombre):
		machine.append(random.random())
		gain.append(random.randint(1,500))
		esperance.append(0)
		moyenne.append(0)
		coups.append(0)
		recolte.append(0)
	return (machine, gain, esperance, moyenne, coups, recolte)

def uniformatisation(tableau):
	pas = 100/len(tableau)
	final = []
	for i in range(1,len(tableau)):
		final.append(pas*i)
	return final

def choixGagnant(esperance):
	m = esperance[0]
	indice = 0
	for i in range(len(esperance)):
		if(esperance[i] > m):
			indice = i
			m = esperance[i]
	return indice

def choisirAlea(data, explo=20):
	choix, esperance, coups, gagnant = data 
	temoin = random.randint(0,100)
	levier = 0
	for i in choix:
		if(temoin < i):
			return levier
		levier += 1
	return levier

def choisirGreedy(data, explo=20):
	choix, esperance, coups, gagnant = data
	if(np.sum(np.array(coups)) > explo):
		return gagnant
	else:
		return choisirAlea(data)

def choisirEGreedy(data, explo=20):
	choix, esperance, coups, gagnant = data
	if(np.sum(np.array(coups)) > explo):
		return choixGagnant(esperance)
	else:
		return choisirAlea(data)

def run(generation, algorithme, T, explo=20, show=True):
	print("-------Initialisation-------")
	machines, gain, esperance, moyenne, coups, recolte = generation
	print("machines: "+str(machines))
	print("gains par machines: "+str(gain))
	choix = uniformatisation(machines)
	total = 0
	gagnant = 0
	ya = []
	yb = []
	x = []
	print("\n\n\n-------TRAITEMENT-------")
	for i in range(T):
		#tableau de choix pour choisir uniformement les levier
		levier = algorithme((choix, esperance, coups, gagnant), explo)
		print("\nlevier: "+str(levier))
		resultat = jouer(machines, levier)
		print("resultat: "+str(resultat))
		coups[levier] = coups[levier]+1
		recolte[levier] = recolte[levier] + gain[levier]*resultat
		moyenne[levier] = recolte[levier]/coups[levier]
		esperance[levier] = recolte[levier]*1.0/gain[levier]/coups[levier]
		total += resultat*gain[levier]
		ya.append(esperance[levier])
		yb.append(machines[levier])
		x.append(i)
		if(i == explo):
			gagnant = choixGagnant(esperance)
	print("\n\n\n-------TERMINAISON-------")
	print("esperance: "+str(esperance))
	print("moyenne: "+str(moyenne))
	print("gains total: "+str(total))
	if(show):
		plt.plot(x, ya, label='esperance')
		plt.plot(x, yb, label='moyenne')
		plt.xlabel('Times')
		plt.ylabel('chances %')
		plt.title('Bandit-manchots wins probabilities')
		plt.legend()
		plt.show()


#print(jouer(l,2))
#print(uniformatisation(l))
#run(genere(4), choisirAlea, 50)
#run(genere(4), choisirGreedy, 50)
run(genere(20), choisirEGreedy, 100, 40)