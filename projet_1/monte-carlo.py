from source import *
import random
import math

class AgentAlea(Agent):
	def __init__(self):
		print("un joueur initialisé")

	def get_action(self,state):
		case = random.randint(0, len(state.get_actions())-1)
		return state.get_actions()[case]


"""state = MorpionState()
print(state.get_actions())
print(state.grid)
state.grid[0][0] = -1
print(state.grid)
print(state.get_actions())
"""

jeu = Jeu(MorpionState(), AgentAlea(), AgentAlea())
win, log = jeu.run(True, 1)
print("joueur gagnant: "+str(win))
print(log)