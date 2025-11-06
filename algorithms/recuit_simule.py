import random, math, time
random.seed(time.time())
from utils.cost import cost

def recuit_simule(matrix, T=1000, T_min=1, alpha=0.95):
    n = len(matrix)
    current = list(range(n))
    random.shuffle(current)
    best = current[:]
    best_cost = cost(best, matrix)

    while T > T_min:
        i, j = random.sample(range(n), 2)
        new_sol = current[:]
        new_sol[i], new_sol[j] = new_sol[j], new_sol[i]
        delta = cost(new_sol, matrix) - cost(current, matrix)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new_sol[:]
            if cost(current, matrix) < best_cost:
                best = current[:]
                best_cost = cost(current, matrix)
        T *= alpha

    return best, best_cost
