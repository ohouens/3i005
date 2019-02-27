import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math


nom = ["aleatoire"]
l=[0.1,0.2,0.3]
proba_fixe=[0.2, 0.5, 0.012, 0.4]
gain_fixe=[4, 1, 50, 5]
"""test"""
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
		#machine.append(proba_fixe[i])
		#gain.append(gain_fixe[i])
		machine.append(random.random())
		#gain.append(random.randint(1,500))
		gain.append(1)
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

def choixGagnant(moyenne):
	m = moyenne[0]
	indice = 0
	for i in range(len(moyenne)):
		if(moyenne[i] > m):
			indice = i
			m = moyenne[i]
	return indice

def calculUCB(moyenne, coups, t):
	if(coups == 0 or moyenne == 0):
		return 1
	return moyenne+math.sqrt((2*math.log(t))/coups)

def choixGagnantUCB(moyenne, coups, T):
	m = calculUCB(moyenne[0], coups[0], T)
	indice = 0
	for i in range(len(moyenne)):
		if(calculUCB(moyenne[i], coups[i], T) > m):
			indice = i
			m = calculUCB(moyenne[i], coups[i], T)
	return indice

def choisirAlea(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data 
	return random.randint(0, len(choix)-1)

def choisirGreedy(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data
	if(np.sum(np.array(coups)) > explo):
		return gagnant
	else:
		return choisirAlea(data)

def choisirEGreedy(data, explo=20, e=0.2):
	choix, moyenne, esperance, coups, gagnant, t = data
	if(np.sum(np.array(coups)) > explo):
		return choisirAlea(data)
	else:
		a = random.random()
		if(a < e):
			return choisirAlea(data)
		else:	
			return choixGagnant(moyenne)

def choisirUCB(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data
	return choixGagnantUCB(moyenne, coups, t)

def run(generation, algorithme, T, explo=20, show=True):
	print("-------Initialisation-------")
	machines, gain, esperance, moyenne, coups, recolte = generation
	print("machines: "+str(machines))
	print("gains par machines: "+str(gain))
	choix = uniformatisation(machines)
	total = 0
	maximal = 0
	gagnant = 0
	ya = []
	yb = []
	x = []
	print("\n\n\n-------TRAITEMENT-------")
	for i in range(T):
		#tableau de choix pour choisir uniformement les levier
		levier = algorithme((choix, moyenne, esperance, coups, gagnant, i), explo)
		print("\nlevier: "+str(levier))
		resultat = jouer(machines, levier)
		print("resultat: "+str(resultat))
		coups[levier] = coups[levier]+1
		recolte[levier] = recolte[levier] + gain[levier]*resultat
		moyenne[levier] = recolte[levier]/coups[levier]
		esperance[levier] = recolte[levier]*1.0/gain[levier]/coups[levier]
		total += resultat*gain[levier]
		maximal += gain[levier]
		ya.append(total)
		yb.append(maximal)
		x.append(i)
		if(i == explo):
			gagnant = choixGagnant(moyenne)
		regret = maximal - total
	print("\n\n\n-------TERMINAISON-------")
	print("esperance: "+str(esperance))
	print("moyenne: "+str(moyenne))
	print("gains total: "+str(total))
	print("regret: "+str(regret))
	if(show):
		plt.plot(x, ya, label='gain du joueur')
		plt.plot(x, yb, label='gain maximal espéré')
		plt.xlabel('Times(moves)')
		plt.ylabel('gains(€)')
		plt.title('Bandit-manchots ('+str(algorithme)+')')
		plt.legend()
		plt.show()
	return regret

#print(jouer(l,2))
#print(uniformatisation(l))
run(genere(200), choisirAlea, 1000)
run(genere(200), choisirGreedy, 1000, 500)
run(genere(200), choisirEGreedy, 1000, 500)
run(genere(200), choisirUCB, 1000, 500)

"""
def experience(T, quantite):
	regret_alea = []
	regret_greedy = []
	regret_eGreedy = []
	regret_UCB = []
	for i in range(25):
		regret_alea.append(run(genere(quantite), choisirAlea, T)
		regret_greedy.append(run(genere(quantite), choisirGreedy, T, eps)
		regret_eGreedy.append(run(genere(quantite), choisirEGreedy, T)
		regret_UCB.append(run(genere(quantite), choisirUCB, T)
"""	