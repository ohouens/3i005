import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math


nom = ["aleatoire"]
l=[0.1,0.2,0.3]
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
		machine.append(random.random()/8)#pour avoir au maximum une proba max = 0,125
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

def choixGagnant(moyenne):
	m = moyenne[0]
	indice = 0
	for i in range(len(moyenne)):
		if(moyenne[i] > m):
			indice = i
			m = moyenne[i]
	return indice

def calculUCB(moyenne, coups, t):
	if t<=0 or 2*math.log(t) > 0 or coups == 0:
		return moyenne
	else : 
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
	temoin = random.randint(0,100)
	levier = 0
	for i in choix:
		if(temoin < i):
			return levier
		levier += 1
	return levier

def choisirGreedy(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data
	if(np.sum(np.array(coups)) > explo):
		return gagnant
	else:
		return choisirAlea(data)

def choisirEGreedy(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data
	if(np.sum(np.array(coups)) > explo):
		return choixGagnant(moyenne)
	else:
		return choisirAlea(data)

def choisirUCB(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data
	if(np.sum(np.array(coups)) > explo):
		return choixGagnantUCB(moyenne, coups, t)
	else:
		return choisirAlea(data)

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
		#print("\nlevier: "+str(levier))
		resultat = jouer(machines, levier)
		#print("resultat: "+str(resultat))
		coups[levier] = coups[levier]+1
		recolte[levier] = recolte[levier] + gain[levier]*resultat
		moyenne[levier] = recolte[levier]/coups[levier]
		esperance[levier] = recolte[levier]*1.0/gain[levier]/coups[levier]
		total += resultat*gain[levier]
		maximal += gain[levier]*machines[levier]
		ya.append(total)
		yb.append(maximal)
		x.append(i)
		if(i == explo):
			gagnant = choixGagnant(moyenne)
	print("\n\n\n-------TERMINAISON-------")
	print("esperance: "+str(esperance))
	print("moyenne: "+str(moyenne))
	print("gains total: "+str(total))
	if(show):
		plt.plot(x, ya, label='gain du joueur')
		plt.plot(x, yb, label='gain maximal espéré')
		plt.xlabel('Times(moves)')
		plt.ylabel('gains(€)')
		plt.title('Bandit-manchots ('+str(algorithme)+')')
		plt.legend()
		plt.show()


#print(jouer(l,2))
#print(uniformatisation(l))
machines=genere(10)#avoir les memes valeurs pour comparer les algo
run(machines, choisirAlea, 100)
run(machines, choisirGreedy, 100, 20)
run(machines, choisirEGreedy, 100, 20)
run(machines, choisirUCB, 100, 20)