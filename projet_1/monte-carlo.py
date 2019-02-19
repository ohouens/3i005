from source import *
import random
import math

class AgentAlea(Agent):
	def __init__(self, prenom="zero"):
		self.prenom = prenom
		print("un joueur initialisé: "+self.prenom)

	def get_action(self,state):
		case = random.randint(0, len(state.get_actions())-1)
		return state.get_actions()[case]


# state = MorpionState()
# print(state.get_actions())
# print(state.grid)
# state.grid[0][0] = -1
# print(state.grid)
# print(state.get_actions())


"""
jeu = Jeu(MorpionState(), AgentAlea(), AgentAlea())
win, log = jeu.run(True, 1)
print("joueur gagnant: "+str(win))
print(log)
"""

def jeuxAleatoire(T=1000):
	j1 = AgentAlea("Ryan")
	j2 = AgentAlea("Pierre")

	somme1 = 0
	somme2 = 0

	x = []
	partiesJ1 = []
	partiesJ2 = []

	for i in range(T):
		jeu = Jeu(MorpionState(), j1, j2)
		win, log = jeu.run()
		if(win == 1):
			somme1 += 1
		else:
			somme2 += 1
		x.append(i)
		partiesJ1.append(somme1)
		partiesJ2.append(somme2)

	print('Poucentage:\nJ1: '+str(somme1*100/T)+'\nJ2: '+str(somme2*100/T))
	plt.plot(x, partiesJ1, label='j1')
	plt.plot(x, partiesJ2, label='j2')
	plt.xlabel('Times(moves)')
	plt.ylabel('parties gagnees')
	plt.title('Morpions')
	plt.legend()
	plt.show()

# jeuxAleatoire()

class AgentMontecarlo(Agent):
	def __init__(self, prenom="zero"):
			self.prenom = prenom
			print("un joueur initialisé: "+self.prenom)

	def get_action(self,state,n=3):
		moyennes = []
		actions = state.get_actions()
		j1 = AgentAlea("j1")
		j2 = AgentAlea("j2")

		
		for j in range (len(actions)):
			moyennes.append(0)

		for i in range(n+1):
			choix = random.randint(0,len(actions))
			print(choix)
			a = state
			while(a.win()==0):
				jeu = Jeu(a, j1, j2)
				gagnant, log = jeu.run()
				"faire jouer les joueurs aléatoirement"
				if(gagnant == 1):
					moyennes[choix] += 1

			
		return (actions[index(max(moyennes))])
		"mettre à jour moyennes en fonction du resultat"
		"retourner max(moyennes)"

		


j1 = AgentMontecarlo("Pierre")
j2 = AgentAlea("Ryan")
jeu = Jeu(MorpionState(), j1, j2)
win, log = jeu.run()
print("joueur gagnant: "+str(win))
print(log)