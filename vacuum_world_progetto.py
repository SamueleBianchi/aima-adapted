import sys
from time import sleep 
from search import *
from utils import *
from esercitazione_13_ottobre import *

initial = (('X','D','V','D','V','D','X','V','X'),5)
#goal = (('X','C','C','C','C','C','X','C','X'),1)
n = int(len(initial[0])**(0.5))

def getGoalState(state):
        state = list(state[0])
        print(state)
        for i in range(len(initial[0])):
            if state[i] == 'D' or state[i] == 'V':
                state[i]='C'
            
        return tuple(state)

goal_state = (getGoalState(initial),1)

class SmartVacuum(Problem):
    """The Smart Vacuum problem """
    def __init__(self, initial, goal=((0,0,0,0),0)):
        super().__init__(initial, goal)

    def azioni_valide(self, state):
        room,position = state
        possible_actions = ['CLEAN','UP','DOWN','LEFT','RIGHT']
        if room[position] == 'C':
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
            if new_room[new_pos] == 'D':
                new_room[new_pos] = 'C'
            elif new_room[new_pos] == 'V':
                new_room[new_pos] = 'D'
        new_state = (tuple(new_room),new_pos)
        return new_state

    def goal_test(self, state):
        return state == self.goal

    def actions(self, state):
        possible_actions = self.azioni_valide(state)
        for azioni in self.azioni_valide(state):
            room,pos = self.result(state, azioni)
            #print(room[pos])
            if room[pos] == 'X':
                possible_actions.remove(azioni)
        return possible_actions

    def print_matrix(self, state, action):
        print(action)
        room,pos = state
        for i in range(len(initial[0])):
            if i%n != n-1:
                if i==pos:
                    print('S', end=" ")
                else:
                    print(room[i], end=" ")
            else:
                if i==pos:
                    print('S')
                else:
                    print(room[i])
        print()

    def anim_vacuum(self, state, sequence_of_actions):
        res = state
        self.print_matrix(state,sequence_of_actions[0])
        for a in sequence_of_actions:
            res = self.result(res, a)
            sleep(1.5)
            self.print_matrix(res, a)

    

smart_vacuum = SmartVacuum(initial, goal_state)

#smart_vacuum.print_matrix(initial)
#smart_vacuum.print_matrix(goal_state)


#print(goal_state)
#print(smart_vacuum.actions(initial))
#print(bfs_grafo(smart_vacuum).solution())
smart_vacuum.anim_vacuum(initial, bfs_grafo(smart_vacuum).solution())