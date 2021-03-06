import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math

proba_fixe=[]
for i in range(1000):
	proba_fixe.append(random.random())

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
		machine.append(proba_fixe[i])
		#machine.append(random.random())
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
		return 0.9
	return moyenne+math.sqrt((2*math.log(t))/coups)

def choixGagnantUCB(moyenne, coups, T):
	m = calculUCB(moyenne[0], coups[0], T)
	indice = 0
	for i in range(len(moyenne)):
		if(calculUCB(moyenne[i], coups[i], T) > m):
			indice = i
			m = calculUCB(moyenne[i], coups[i], T)
	return indice

def choisirUCB(data, explo=20):
	choix, moyenne, esperance, coups, gagnant, t = data
	return choixGagnantUCB(moyenne, coups, t)

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
	if(random.random() < explo):
		return choisirAlea(data)
		
	else:
		return choixGagnant(moyenne)


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
	yc = []
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
		meilleur_levier = moyenne.index(max(moyenne))
		maximal += gain[meilleur_levier]
		regret = maximal - total
		ya.append(total)
		yb.append(maximal)
		x.append(i)
		yc.append(regret)
		if(i == explo):
			gagnant = choixGagnant(moyenne)
		
	print("\n\n\n-------TERMINAISON-------")
	# print("esperance: "+str(esperance))
	# print("moyenne: "+str(moyenne))
	# print("gains total: "+str(total))
	print("regret: "+str(regret))
	#if(show):
		# plt.plot(x, ya, label='gain du joueur')
		# plt.plot(x, yb, label='gain maximal espéré')
		# plt.xlabel('Times(moves)')
		# plt.ylabel('gains(€)')
		# plt.title('Bandit-manchots ('+str(algorithme)+')')
		# plt.legend()
		# plt.show()

		# plt.plot(x, yc, label='regret du joueur')
		# plt.plot(x, yb, label='gain maximal espéré')
		# plt.xlabel('Times(moves)')
		# plt.ylabel('regret')
		# plt.title('Bandit-manchots ('+str(algorithme)+')')
		# plt.legend()
		# plt.show()


	#yc correspond au regret, yb au max et ya au total
	return yc,yb,ya

taille = 100
nbM = 200

alea_yc, alea_yb, alea_ya = run(genere(nbM), choisirAlea, taille)
greedy_yc, greedy_yb, greedy_ya = run(genere(nbM), choisirGreedy, taille, taille*0.4)
egreedy_yc, egreedy_yb, egreedy_ya = run(genere(nbM), choisirEGreedy, taille, 0.2)
ucb_yc, ucb_yb, ucb_ya = run(genere(nbM), choisirUCB, taille, 0)


#boucle pour récupérer le x du run
x=[]
for i in range(taille):
	x.append(i)



#affichage du regret
plt.plot(x, alea_yc, label='regret alea')
plt.plot(x, greedy_yc, label='regret greedy')
plt.plot(x, egreedy_yc, label='regret egreedy')
plt.plot(x, ucb_yc, label='regret ucb')

plt.xlabel('Times(moves)')
plt.ylabel('regret')
plt.title('Evolution du regret en fonction du nombre de tirage')
plt.legend()
plt.show()
