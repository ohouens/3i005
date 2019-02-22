from source import *
import random
import math
import copy
"test commit"
class AgentAlea(Agent):
	def __init__(self, prenom="zero"):
		self.prenom = prenom
		#print("un joueur initialisé: "+self.prenom)

	def get_action(self,state):
		case = random.randint(0, len(state.get_actions())-1)
		return state.get_actions()[case]


class AgentMontecarlo(Agent):
	def __init__(self, prenom="zero", state=MorpionState()):
			self.prenom = prenom
			self.state = state
			#print("un joueur initialisé: "+self.prenom)

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

		for i in range(n):
			#print('partie '+str(i)+' aleatoire')
			choix = random.randint(0,len(actions)-1)
			coups[choix] += 1
			#print("actions: "+str(len(actions)))
			#print('choix: '+str(choix))
			newState = copy.deepcopy(state)
			v1, v2 = jeux(newState, j1, j2, 60, False)
			moyennes[choix] += v1

		for i in range(len(coups)):
			if[coups[i]==0]:
				esperance[i] = 0
			else:
				esperance[i] = moyennes[i]/coups[i]

		return (actions[esperance.index(max(esperance))])

def jeux(state, j1, j2, T=500, show=True):
	somme1 = 0
	somme2 = 0

	x = []
	partiesJ1 = []
	partiesJ2 = []

	for i in range(T):
		jeu = Jeu(state, j1, j2)
		win, log = jeu.run()
		if(win == 1):
			somme1 += 1
		else:
			somme2 += 1
		x.append(i)
		partiesJ1.append(somme1)
		partiesJ2.append(somme2)

	if(show):
		print('Pourcentage:\n'+j1.prenom+': '+str(somme1*100/T)+'\n'+j2.prenom+': '+str(somme2*100/T))
		plt.plot(x, partiesJ1, label='j1')
		plt.plot(x, partiesJ2, label='j2')
		plt.xlabel('Times(moves)')
		plt.ylabel('parties gagnees')
		plt.title('Morpions')
		plt.legend()
		plt.show()
	return (somme1*100/T, somme2*100/T)

jeux(MorpionState(), AgentAlea("Pierre"), AgentMontecarlo("Ryan"), 40)