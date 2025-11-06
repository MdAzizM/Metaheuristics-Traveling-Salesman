import random, time
random.seed(time.time())
from utils.cost import cost

def tabu_search(matrix, tenure=5, max_iter=200):
    n = len(matrix)
    current = list(range(n))
    random.shuffle(current)
    best = current[:]
    best_cost = cost(best, matrix)
    tabou_list = []

    for _ in range(max_iter):
        neighbors = []
        for i in range(n):
            for j in range(i + 1, n):
                neighbor = current[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)

        neighbors = sorted(neighbors, key=lambda sol: cost(sol, matrix))
        for sol in neighbors:
            move = (sol[0], sol[-1])
            if move not in tabou_list:
                current = sol
                c = cost(sol, matrix)
                if c < best_cost:
                    best = sol[:]
                    best_cost = c
                tabou_list.append(move)
                if len(tabou_list) > tenure:
                    tabou_list.pop(0)
                break

    return best, best_cost
