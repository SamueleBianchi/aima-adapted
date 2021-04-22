from os import system
from time import sleep 
from search import *
from esercitazione_13_ottobre_live import *
from esercitazione_16_ottobre_live import *
#from esercitazione_16_ottobre_live import get_numero_nodi

class Vacumm(Problem):

    def __init__(self, initial, goal=((0,0,0,0),0)):
        super().__init__(initial, goal)

    def actions(self, state):
        room,pos = state
        possible_actions = ['CLEAN','LEFT', 'RIGHT']
        if room[pos] == 0:
            possible_actions.remove('CLEAN')
        if pos == 0:
            possible_actions.remove('LEFT')
        if pos == len(self.goal[0])-1:
            possible_actions.remove('RIGHT')

        return possible_actions

    def result(self, state, action):
        room,pos = state
        new_room = [*room]
        new_pos = pos
        if action == 'LEFT':
            new_pos -= 1
        elif action == 'RIGHT':
            new_pos += 1
        elif action == "CLEAN":
            new_room[new_pos] = 0
        new_state = (tuple(new_room),new_pos)
        return new_state

    def goal_test(self, state):
        #test dirty rooms and vacumm pos
        return state == self.goal
        #only dirty rooms 
        #return state[0] == self.goal[0]

    def h(self, node):
        return 0

def print_vacumm(state):
    room, pos = state
    print("   "*(pos)+" v")
    print("".join([" x " if x else "   " for x in room]))

def path_to_node(node):
    h = []
    p = node
    while p is not None:
        h.append(p)
        p = p.parent
    h.reverse()
    return h

def anim_vacumm(node):
    his = path_to_node(node)
    line = "---"*len(node.state[0])
    for k,node in enumerate(his):
        system('clear') 
        print(line)
        print("{} / {}".format(k,len(his)-1))
        print(line)
        print_vacumm(node.state)
        #print(node.state)
        print(line)
        sleep(0.5)
    print(node.solution())
    #print(get_numero_nodi())

def n_dirty(node):
    room, pos = node.state
    return sum(room)

def get_pos_dirty(arr):
    try:
        return arr.index(1)
    except:
        return 0

def min_dist_from_dirty(node):
    room, pos = node.state
    rl = [*room[:pos]]
    rl.reverse()
    dl = get_pos_dirty(rl)
    rr = room[pos+1:]
    dr = get_pos_dirty(rr)
    return min(dl,dr)

def max_dist_from_dirty(node):
    room, pos = node.state
    rl = [*room[:pos]]
    dl = get_pos_dirty(rl)
    rr = [*room[pos+1:]]
    rr.reverse()
    dr = get_pos_dirty(rr)
    return max(dl,dr)

def dir_dirty(node):
    room, pos = node.state
    dl = sum(room[:pos])
    dr = sum(room[pos+1:])
    return max(dl,dr)

#initial = ((1,0,0,1,1),2)
#goal = ((0,0,0,0,0),2)

#initial = ((1,0,0,0,1,1),3)
#goal = ((0,0,0,0,0,0),2)

initial = ((1,1,1,0),0)
goal = ((0,0,0,0),0)
#h = n_dirty
#h = max_dist_from_dirty
#h = min_dist_from_dirty
#h = dir_dirty
result = astar_search(Vacumm(initial,goal), h = max_dist_from_dirty)
anim_vacumm(result)