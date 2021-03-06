from source import *
import random
import math
import copy



class AgentAlea(Agent):
	def __init__(self, prenom="zero"):
		self.prenom = prenom
		#print("un joueur initialisé: "+self.prenom)

	def get_action(self,state):
		case = random.randint(0, len(state.get_actions())-1)
		return state.get_actions()[case]


class AgentMontecarlo(Agent):
	def __init__(self, prenom="zero", n=50):
			self.prenom = prenom
			self.n = n
			print("un joueur initialisé: "+self.prenom)

	def get_action(self,state):
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

		for i in range(len(actions)):
			courant = state.courant
			print('partie '+str(i)+' aleatoire')
			print('courant: '+str(courant))
			coups[i] += 1
			case = state.get_actions()[i]
			newState = state.next(case)
			v1, v2 = jeux(newState, j1, j2, 1, False)
			if(courant == 1):
				moyennes[i] += v1
			else:
				moyennes[i] += v2

		for i in range(self.n):
			courant = state.courant
			print('partie '+str(i)+' aleatoire')
			print('courant: '+str(courant))
			choix = random.randint(0,len(actions)-1)
			coups[choix] += 1
			case = state.get_actions()[choix]
			newState = state.next(case)
			v1, v2 = jeux(newState, j1, j2, 1, False)
			if(courant == 1):
				moyennes[choix] += v1
			else:
				moyennes[choix] += v2

		for i in range(len(actions)):
			if(coups[i]==0):
				print("probleme")
				print(coups)
				print(i)
				print(coups[i])
				exit(0)
			else:
				esperance[i] = moyennes[i]/coups[i]
		#print(esperance)
		#exit(0)
		return actions[esperance.index(max(esperance))]


class AgentUCT(Agent):
	def __init__(self, prenom="zero", n=5, parent=-1):
		self.prenom = prenom
		self.n = n
		self.parent = parent
		self.enfant = []
		self.coups = 0
		self.victoire = 0
		self.courant = 1
		if(self.parent != -1):
			self.courant = self.parent.state.courant
		#print("un joueur initialisé: "+self.prenom)

	def get_action(self,state):
		self.state = state
		self.naissance()
		for i in range(self.n):
			current = self.expansion(self.selection())
		case = self.selection(False)
		#print(self.victoire, self.coups)
		#print(case.victoire, case.coups)
		#print("SELECTION: "+str(case.prenom)+", son parent: "+str(case.parent.prenom))
		#print(state.get_actions())
		for i in range(len(self.enfant)):
			#print("enfant"+self.enfant[i].prenom+": ("+str(self.enfant[i].victoire)+")victoires/("+str(self.enfant[i].coups)+")coups")
			if(case is self.enfant[i]):
				self.victoire = 0
				self.coups = 0
				self.enfant.clear()
				return state.get_actions()[i]
		print("ERRRRRRRRRROOOOR: no child found")
		exit(0)

	def expansion(self, agent):
		if(len(agent.enfant) == 0):
			agent.naissance()
		else:
			agent.selection().simule()
		return agent.selection()

	def retroPropage(self, victoire):
		agent = self
		while(agent.parent != -1):
			agent.parent.victoire += victoire
			agent.parent.coups += 1
			agent = agent.parent
		return (agent.victoire, agent.coups)

	def naissance(self):
		actions = self.state.get_actions()
		for j in range (len(actions)):
			case = self.state.get_actions()[j]
			newState = self.state.next(case)
			self.enfant.append(AgentUCT(self.prenom+"_"+str(j), 0, self))
			self.enfant[j].courant = newState.courant*-1
			self.enfant[j].state = newState
			self.enfant[j].simule()
			#print("enfant"+self.prenom+": "+str(self.enfant[j].victoire)+"/"+str(self.enfant[j].coups)+"\n")

	def simule(self):
		j1 = AgentAlea("j1")
		j2 = AgentAlea("j2")
		v1, v2 = jeux(self.state, j1, j2, 1, False)
		self.coups += 1
		if(self.courant == 1 and v1>v2):
			self.victoire += 1
			return self.retroPropage(1)
		elif(self.courant == -1 and v1<v2):
			self.victoire += 1
			return self.retroPropage(1)
		else:
			return self.retroPropage(0)

	def selection(self, recursive=True):
		agent = self
		while(len(agent.enfant) != 0 and agent.coups != 0):
			victoire = []
			coups = []
			for e in agent.enfant:
				victoire.append(e.victoire)
				coups.append(e.coups)
			nAgent = self.selectionUCB(victoire, coups, np.sum(coups))
			enfant = agent.enfant[nAgent]
			if(recursive):
				agent = enfant
			else:
				return enfant
		return agent

	def calculUCB(self, victoire, coups, t):
		return (victoire/coups)+math.sqrt((2*math.log(t))/coups)

	def selectionUCB(self, victoire, coups, T):
		m = self.calculUCB(victoire[0], coups[0], T)
		indice = 0
		for i in range(len(victoire)):
			if(self.calculUCB(victoire[i], coups[i], T) > m):
				indice = i
				m = self.calculUCB(victoire[i], coups[i], T)
		return indice



def graphique(x, y1, y2, y3):
	plt.plot(x, y1, label='j1')
	plt.plot(x, y2, label='j2')
	plt.plot(x, y3, Label='Match nul')
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
	somme3 = 0
	x = []
	partiesJ1 = []
	partiesJ2 = []
	partiesJ3 = []
	for i in range(T):
		if(show):
			print("-------------JEU "+str(i)+"-------------")
		jeu = Jeu(state, j1, j2)
		win, log = jeu.run()
		if(win == 1):
			somme1 += 1
		elif(win == -1):
			somme2 += 1
		else:
			somme3 += 1
			
		x.append(i)
		partiesJ1.append(somme1)
		partiesJ2.append(somme2)
		partiesJ3.append(somme3)
		if(show and (i+1)%(T//pause) == 0):
			graphique(x, partiesJ1, partiesJ2, partiesJ3)
	p1 = somme1*100/T
	p2 = somme2*100/T
	if(show):
		print('Pourcentage:\n'+j1.prenom+': '+str(p1)+'\n'+j2.prenom+': '+str(p2))
	return (p1, p2)



jeux(MorpionState(), AgentMontecarlo("Pierre", 20), AgentUCT("Ryan", 20), 30, True, 1)