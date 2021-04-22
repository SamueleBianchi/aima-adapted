import sys
from search import *
numero_nodi = 0
numero_nodi_max = 0

# Esempi
#romania_problem = GraphProblem('Arad', 'Bucharest', romania_map) #tutti e 3 hanno differenti path
#romania_problem = GraphProblem('Lugoj', 'Zerind', romania_map) # DFS molto lunga e BFS = UC
#romania_problem = GraphProblem('Lugoj', 'Craiova', romania_map) #  Tutti e 3 uguali
romania_problem = GraphProblem('Lugoj', 'Neamt', romania_map)  # cammino lungo DFS = UC != BFS, RBFS lenta

def show_solution(type_search_graph, node):
    if node is None or type(node) == str:
        print(type_search_graph, "no solution")
    else:
        print(type_search_graph, node.solution())


def depth_limited_search(problem, limit=20):
    """[Figure 3.17]"""

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)

#esempi con 1/2/10/20
#show_solution('DLS',depth_limited_search(romania_problem,10))


def iterative_deepening_search(problem):
    """[Figure 3.18]"""
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result

#show_solution('IDS',iterative_deepening_search(romania_problem))

# a lezione 
#from esercitazione_13_ottobre_live import best_first
#per noi, per mostrare quanti nodi sono in memoria allo stesso tempo 
def best_first(problem, f):
    global numero_nodi
    nodo_iniziale = Node(problem.initial)
    numero_nodi = 1

    if problem.goal_test(nodo_iniziale.state):
        return nodo_iniziale

    f = memoize(f,'f')
    frontiera = PriorityQueue('min',f)
    frontiera.append(nodo_iniziale)
    visitati = set()

    while frontiera:
        nodo = frontiera.pop()
        visitati.add(nodo.state)
        
        if problem.goal_test(nodo.state):
            return nodo 

        expand = nodo.expand(problem)
        numero_nodi += len(expand)
        for nodo_figlio in expand:
            if nodo_figlio.state not in visitati and nodo_figlio not in frontiera:
                frontiera.append(nodo_figlio)
            elif nodo_figlio in frontiera:
                nodo_prossimo = frontiera.get_item(nodo_figlio)
                if f(nodo_figlio) < f(nodo_prossimo):
                    del frontiera[nodo_prossimo]
                    frontiera.append(nodo_figlio)

#ricordare ucs ****(U=uniform)**** 
def ucs_search(problem):
    """f(n) = g(n)"""
    return best_first(problem, lambda n: n.path_cost)

risultato = ucs_search(romania_problem)
#show_solution("UCS {}".format(numero_nodi),risultato)

#presentare greedy 
#dire che per questo problema H=distanza euclidea trai nodi e mostrare codice in Class Problem
#e dire che possiamo usare H alternative
def greedy_search(problem, h=None):
    """f(n) = h(n)"""
    h = memoize(h or problem.h, 'h') #spiegare
    return best_first(problem, lambda n: h(n))

risultato = greedy_search(romania_problem)
#show_solution("GREEDY {}".format(numero_nodi),risultato)

# dire che greedy + ucs = a*
def astar_search(problem, h=None):
    """f(n) = g(n)+h(n)."""
    h = memoize(h or problem.h, 'h')
    return best_first(problem, lambda n: n.path_cost + h(n))

risultato = astar_search(romania_problem)
#show_solution("A STAR {}".format(numero_nodi),risultato)

sys.setrecursionlimit(10000)

def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""
    h = memoize(h or problem.h, 'h')
    g = memoize(lambda n: n.path_cost, 'g')
    f = memoize(lambda n: g(n) + h(n),'f')

    global numero_nodi_max
    global numero_nodi
    numero_nodi_max = 0
    numero_nodi = 1

    def RBFS(problem, node, flimit=np.inf):
        global numero_nodi
        global numero_nodi_max
        #test
        if problem.goal_test(node.state):
            return node, 0
        #list of child
        successors = [*node.expand(problem)]
        n_successors = len(successors)
        numero_nodi += n_successors
        numero_nodi_max = max(numero_nodi, numero_nodi_max)
        #print(node.state, n_successors)
        #no childs
        if len(successors) == 0:
            return None, np.inf
        #f of successors
        for succ_node in successors:
            succ_node.f = max(f(succ_node), node.f)

        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            #print([(s.state,'f',s.f,'g',s.g,'h',s.h) for s in successors])
            best = successors[0]
            #f
            if best.f > flimit:
                numero_nodi -= n_successors
                return None, best.f
            #elternative
            alternative = successors[1].f if len(successors) > 1 else np.inf
            #importante, sovrascrivere best.f
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            #return result
            if result is not None:
                numero_nodi -= n_successors
                return result, best.f

    node = Node(problem.initial) 
    f(node)
    return RBFS(problem, node)[0]

risultato = recursive_best_first_search(romania_problem)
#show_solution('RBFS {} (MAX)'.format(numero_nodi_max),risultato)