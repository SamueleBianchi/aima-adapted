import sys
from search import *
from utils import *
from esercitazione_13_ottobre import *

class SmartVacuum(Problem):
    """The Smart Vacuum problem """
    def __init__(self, initial, goal=((0,0,0,0),0)):
        super().__init__(initial, goal)

    def azioni_valide(self, state):
        room,position = state
        possible_actions = ['CLEAN','UP','DOWN','LEFT','RIGHT']
        if room[position] == 0:
            possible_actions.remove('CLEAN')
        if position == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('UP')
        elif position == n-1:
            possible_actions.remove('RIGHT')
            possible_actions.remove('UP')
        elif position == n*(n-1):
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        elif position == n*n-1:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
        elif position%n == 0:
            possible_actions.remove('LEFT')
        elif position%n == n-1:
            possible_actions.remove('RIGHT')
        elif position < n*n and position > n*(n-1):
            possible_actions.remove('DOWN')
        elif position > 0 and position < n-1:
            possible_actions.remove('UP')
        return possible_actions

    def result(self, state, action):
        room,pos = state
        new_room = [*room]
        new_pos = pos
        if action == 'LEFT':
            new_pos -= 1
        elif action == 'RIGHT':
            new_pos += 1
        elif action == 'UP':
            new_pos -= n
        elif action == 'DOWN':
            new_pos += n
        elif action == "CLEAN":
            new_room[new_pos] -= 1
        new_state = (tuple(new_room),new_pos)
        return new_state

    def goal_test(self, state):
        return state == self.goal

    def actions(self, state):
        possible_actions = self.azioni_valide(state)
        for azioni in self.azioni_valide(state):
            room,pos = self.result(state, azioni)
            #print(room[pos])
            if room[pos] == -1:
                possible_actions.remove(azioni)
        return possible_actions
    
    def getGoalState(self, state):
        state = list(state[0])
        print(state)
        for i in range(len(goal[0])):
            if state[i] == 1 or state[i] == 2:
                state[i]=0
            
        return tuple(state)

initial = ((-1,1,2,1,2,1,-1, 2,-1),1)
goal = ((-1,0,0,0,0,0,-1,0,-1),1)
n = int(len(goal[0])**(0.5))

smart_vacuum = SmartVacuum(initial, goal)

stato = smart_vacuum.getGoalState(initial)
print(stato)
#print(smart_vacuum.actions(initial))
print(bfs_grafo(smart_vacuum).solution())
