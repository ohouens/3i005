from source import *
import random
import math
import copy

class AgentAlea(Agent):
	def __init__(self, prenom="zero"):
		self.prenom = prenom
		print("un joueur initialisé: "+self.prenom)

	def get_action(self,state):
		case = random.randint(0, len(state.get_actions())-1)
		return state.get_actions()[case]


class AgentMontecarlo(Agent):
	def __init__(self, prenom="zero", n=50):
			self.prenom = prenom
			self.n = n
			print("un joueur initialisé: "+self.prenom)

	def get_action(self,state,n=50):
		moyennes = []
		coups = []
		esperance = []
		actions = state.get_actions()
		j1 = AgentAlea("j1")
		j2 = AgentAlea("j2")

		for j in range (len(actions)):
			moyennes.append(0)
			esperance.append(0)
			coups.append(0)

		for i in range(self.n):
			print('partie '+str(i)+' aleatoire')
			newState = copy.deepcopy(state)
			courant = newState.courant
			choix = random.randint(0,len(actions)-1)
			coups[choix] += 1
			print("actions: "+str(len(actions)))
			print('choix: '+str(choix))
			case = newState.get_actions()[choix]
			newState = newState.next(case)
			v1, v2 = jeux(newState, j1, j2, 1, False)
			if(courant == 1):
				moyennes[choix] += v1
			else:
				moyennes[choix] += v2

		for i in range(len(coups)):
			if[coups[i]==0]:
				esperance[i] = 0
			else:
				esperance[i] = moyennes[i]/coups[i]

		return (actions[esperance.index(max(esperance))])

def graphique(x, y1, y2):
	plt.plot(x, y1, label='j1')
	plt.plot(x, y2, label='j2')
	plt.xlabel('Times(moves)')
	plt.ylabel('parties gagnees')
	plt.title('Morpions')
	plt.legend()
	plt.show()

def jeux(state, j1, j2, T=500, show=True, pause=4):
	if(pause > 5):
		pause = 1
	somme1 = 0
	somme2 = 0

	x = []
	partiesJ1 = []
	partiesJ2 = []

	for i in range(T):
		print("-------------JEU "+str(i)+"-------------")
		jeu = Jeu(state, j1, j2)
		win, log = jeu.run()
		if(win == 1):
			somme1 += 1
		else:
			somme2 += 1
		x.append(i)
		partiesJ1.append(somme1)
		partiesJ2.append(somme2)
		if(show and (i+1)%(T//pause) == 0):
			graphique(x, partiesJ1, partiesJ2)
	p1 = somme1*100/T
	p2 = somme2*100/T
	print('Pourcentage:\n'+j1.prenom+': '+str(p1)+'\n'+j2.prenom+': '+str(p2))
	return (p1, p2)

jeux(MorpionState(), AgentMontecarlo("Pierre", 10), AgentMontecarlo("Ryan", 30), 10, True, 1)