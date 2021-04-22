from search import *
from esercitazione_13_ottobre import best_first

# def show_solution(nome_algoritmo, nodo):
#    try:
#        print(nome_algoritmo, nodo.solution())
#    except:
#        print(nome_algoritmo, nodo.solution())
#        if type(Node) == str:
#            print(nome_algoritmo, nodo)
#        else:
#            print(nome_algoritmo, "Nessuna soluzione trovata")

def show_solution(type_search_graph, node):
    if node is None or type(node) == str:
        print(type_search_graph, "no solution")
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

show_solution("DLS", depth_limited_search(romania_problem, 10))

def iterative_deepening_search(problem):
    for depth in range(sys.maxsize): #maxsize è il limite massimo della macchina
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result
    return None

show_solution("IDS", iterative_deepening_search(romania_problem))

def greedy_search(problem):
    h = memoize(problem.h, 'h')#euristica in linea d'aria, memoize permette di aggiungere l'attributo euristica h al nodo
    return best_first(problem, f=h)

show_solution("GREEDY SEARCH", greedy_search(romania_problem))

def astar_search(problem):
    h = memoize(problem.h, 'h')
    g = memoize(lambda n: n.path_cost, 'g')
    return best_first(problem, f = lambda n: g(n) + h(n))

show_solution("ASTAR", astar_search(romania_problem))

#usando questa versione si espandono meno nodi
#di contro, abbiamo che costa di piu a livello computazionale

def recursive_best_first_search(problem):
    h = memoize(problem.h, 'h')
    g = memoize(lambda n: n.path_cost, 'g')
    f = memoize(lambda n: g(n) + h(n), 'f')

    def RBFS(problem, node, f_limit = np.inf):
        if problem.goal_test(node.state):
            return node, 0    #0 è il costo 

        successors = node.expand(problem)

        if len(successors) == 0:
            return None, np.inf # siamo in un nodo foglia, e ha un costo infinito
        
        for s_node in successors:
            s_node.f = max(f(s_node), node.f) #aggiorno il costo dei successori

        while True:
            successors.sort(key = lambda n: n.f) #ordino i successori in base alla f
            best = successors[0] #prendo il successore con la f piu piccola
            if best.f > f_limit:
                return None, best.f

            sec_best_f = np.inf
            if len(successors) >= 2:
                sec_best_f = successors[1].f
            
            result, best.f = RBFS(problem, best, f_limit=min(best.f, sec_best_f))

            if result is not None:
                return result , best.f
    node =  Node(problem.initial)
    f(node)
    return RBFS(problem, node)[0]

show_solution("RBFS", recursive_best_first_search(romania_problem))