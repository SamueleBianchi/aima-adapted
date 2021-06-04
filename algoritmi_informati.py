from search import *
#from algoritmi_noninformati import best_first
numero_nodi = 0
numero_nodi_max = 0


def show_solution(type_search_graph, node):
    if node is None or type(node) == str:
        print(type_search_graph, "Nessuna soluzione trovata")
    else:
        print(type_search_graph, node.solution())


romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)

def depth_limited_search(problem, limit = 20):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit-1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None
    return recursive_dls(Node(problem.initial), problem, limit)

#show_solution("DLS", depth_limited_search(romania_problem, 10))

def iterative_deepening_search(problem):
    for depth in range(sys.maxsize): #maxsize è il limite massimo della macchina
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result
    return None

#show_solution("IDS", iterative_deepening_search(romania_problem))
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


def greedy_search(problem):
    h = memoize(problem.h, 'h')#euristica in linea d'aria, memoize permette di aggiungere l'attributo euristica h al nodo
    return best_first(problem, f=h)

#show_solution("GREEDY SEARCH", greedy_search(romania_problem))

def astar_search(problem):
    h = memoize(problem.h, 'h')
    g = memoize(lambda n: n.path_cost, 'g')
    return best_first(problem, f = lambda n: g(n) + h(n))

#show_solution("ASTAR", astar_search(romania_problem))

#usando questa versione si espandono meno nodi
#di contro, abbiamo che costa di piu a livello computazionale

def recursive_best_first_search(problem, h=None):
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
        if problem.goal_test(node.state):
            return node, 0
        successors = [*node.expand(problem)]
        n_successors = len(successors)
        numero_nodi += n_successors
        numero_nodi_max = max(numero_nodi, numero_nodi_max)

        if len(successors) == 0:
            return None, np.inf

        for succ_node in successors:
            succ_node.f = max(f(succ_node), node.f)

        while True:
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                numero_nodi -= n_successors
                return None, best.f
            alternative = successors[1].f if len(successors) > 1 else np.inf
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                numero_nodi -= n_successors
                return result, best.f

    node = Node(problem.initial) 
    f(node)
    return RBFS(problem, node)[0]

#show_solution("RBFS", recursive_best_first_search(romania_problem))