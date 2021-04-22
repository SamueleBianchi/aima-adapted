from search import *

romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))

romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)

def bfs_albero(problem):
    frontiera = deque([Node(problem.initial)])# in python non c'è distinzione tra lifo e fifo, dipende da come estraggo
    while frontiera:
        nodo = frontiera.popleft() # FIFO
        
        if problem.goal_test(nodo.state):
            return nodo
        else:
            for nodo_figlio in nodo.expand(problem):
                frontiera.append(nodo_figlio)
            # istruzione alternativa frontiera.extend(nodo.expand(problema))

def bfs_grafo(problem):
        frontiera = deque([Node(problem.initial)])
        visitati = set();

        while frontiera:
            nodo = frontiera.popleft()
            visitati.add(nodo.state)

            if problem.goal_test(nodo.state):
                return nodo
            else:
                for nodo_figlio in nodo.expand(problem):
                    if nodo_figlio.state not in visitati and nodo_figlio not in frontiera:
                        frontiera.append(nodo_figlio)

def dfs_albero(problem):
    frontiera = deque([Node(problem.initial)])
    while frontiera:
        nodo = frontiera.pop() # LIFO
        
        if problem.goal_test(nodo.state):
            return nodo
        else:
            for nodo_figlio in nodo.expand(problem):
                frontiera.append(nodo_figlio)
            # istruzione alternativa frontiera.extend(nodo.expand(problema))

def dfs_grafo(problem):
        frontiera = deque([Node(problem.initial)])
        visitati = set();

        while frontiera:
            nodo = frontiera.pop()
            visitati.add(nodo.state)

            if problem.goal_test(nodo.state):
                return nodo
            else:
                for nodo_figlio in nodo.expand(problem):
                    if nodo_figlio.state not in visitati and nodo_figlio not in frontiera:
                        frontiera.append(nodo_figlio)

##print("BFS ALBERO", bfs_albero(romania_problem).solution())
#print("BFS GRAFO", bfs_grafo(romania_problem).solution())
# va in overflow perche percorre dei cicli in quanto non tiene traccia dei nodi visitati
#print("DFS ALBERO", dfs_albero(romania_problem).solution()) 
#print("DFS GRAFO", dfs_grafo(romania_problem).solution())


def best_first(problem, f):
    
    if problem.goal_test(problem.initial):
        return Node(problem.initial)

    f = memoize(f,'f')
    frontiera = PriorityQueue('min',f)
    frontiera.append(Node(problem.initial))
    visitati = set()

    while frontiera:
        nodo = frontiera.pop()
        if problem.goal_test(nodo.state):
            return nodo 
        visitati.add(nodo.state)

        for nodo_figlio in nodo.expand(problem):
            if nodo_figlio.state not in visitati and nodo_figlio not in frontiera:
                frontiera.append(nodo_figlio)
            elif nodo_figlio in frontiera:
                nodo_prossimo = frontiera.get_item(nodo_figlio)
                if f(nodo_figlio) < f(nodo_prossimo):
                    del frontiera[nodo_prossimo]
                    frontiera.append(nodo_figlio)
        

#print("UCS      ",best_first(romania_problem, lambda n: n.path_cost).solution())