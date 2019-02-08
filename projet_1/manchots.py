import numpy as np
import copy
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
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

def choisirAlea(tab):
	temoin = random.randint(0,100)
	place = 0
	for i in tab:
		if(temoin < i):
			return place
		place += 1
	return place

def run(generation, algorithme, T):
	print("-------Initialisation-------")
	machines, gain, esperance, moyenne, coups, recolte = generation
	print(machines)
	print(gain)
	print(esperance)
	print(coups)
	print(recolte)
	choix = uniformatisation(machines)
	total = 0
	for i in range(T):
		#tableau de choix pour choisir uniformement les levier
		place = algorithme(choix)
		resultat = jouer(machines, place)
		#print("place: "+str(place))
		#print("resultat: "+str(resultat))
		coups[place] = coups[place]+1
		recolte[place] = recolte[place] + gain[place]*resultat
		total += resultat*gain[place]
	print("esperance: "+str(esperance))
	print("moyenne: "+str(moyenne))
	print("total: "+str(total))


#print(jouer(l,2))
#print(uniformatisation(l))
run(genere(4), choisirAlea, 15)
