import random, time
random.seed(time.time())
from utils.cost import cost

# ---------- CROSSOVERS ----------
def crossover_simple(p1, p2):
    n = len(p1)
    start, end = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[start:end] = p1[start:end]
    fill = [x for x in p2 if x not in child]
    k = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[k]
            k += 1
    return child

#def crossover_double(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = p1[:a] + p2[a:b] + p1[b:]
    seen = []
    return [x for x in child if not (x in seen or seen.append(x))]
def crossover_double(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    # Copy middle segment from parent2
    child[a:b] = p2[a:b]
    # Fill remaining positions from parent1
    pos = b
    for gene in p1:
        if gene not in child:
            if pos >= n:
                pos = 0
            child[pos] = gene
            pos += 1
    return child


def crossover_uniform(p1, p2):
    n = len(p1)
    child = []
    for i in range(n):
        child.append(p1[i] if random.random() < 0.5 else p2[i])
    # fix duplicates
    seen, fixed = set(), []
    for x in child:
        if x in seen:
            fixed.append(None)
        else:
            seen.add(x)
            fixed.append(x)
    missing = [x for x in p1 if x not in seen]
    for i in range(n):
        if fixed[i] is None:
            fixed[i] = missing.pop(0)
    return fixed


# ---------- SELECTION METHODS ----------

# 🧬 1. Roulette Selection
def roulette_selection(pop, matrix):
    fitness = [1 / (cost(sol, matrix) + 1e-6) for sol in pop]  # inverse cost = fitness
    total = sum(fitness)
    pick = random.uniform(0, total)
    current = 0
    for sol, f in zip(pop, fitness):
        current += f
        if current >= pick:
            return sol
    return pop[-1]

# 🧬 2. Rank Selection (Rang)
def rank_selection(pop, matrix):
    sorted_pop = sorted(pop, key=lambda sol: cost(sol, matrix))
    ranks = list(range(1, len(sorted_pop) + 1))  # lowest cost = lowest rank
    total = sum(ranks)
    pick = random.uniform(0, total)
    current = 0
    for sol, rank in zip(sorted_pop, ranks):
        current += rank
        if current >= pick:
            return sol
    return sorted_pop[-1]


# ---------- MAIN GENETIC ALGORITHM ----------
def genetique(matrix, selection="roulette", type_croisement="simple", pop_size=20, generations=100):
    n = len(matrix)
    pop = [random.sample(range(n), n) for _ in range(pop_size)]

    for _ in range(generations):
        # 🧠 Choose selection method
        if selection == "roulette":
            p1 = roulette_selection(pop, matrix)
            p2 = roulette_selection(pop, matrix)
        else:  # rang selection
            p1 = rank_selection(pop, matrix)
            p2 = rank_selection(pop, matrix)

        # 🧬 Apply crossover
        if type_croisement == "simple":
            child = crossover_simple(p1, p2)
        elif type_croisement == "double":
            child = crossover_double(p1, p2)
        else:
            child = crossover_uniform(p1, p2)

        # 🧬 Mutation
        if random.random() < 0.2:
            i, j = random.sample(range(n), 2)
            child[i], child[j] = child[j], child[i]

        # 🔁 Replace the worst individual
        worst = max(pop, key=lambda sol: cost(sol, matrix))
        if cost(child, matrix) < cost(worst, matrix):
            pop.remove(worst)
            pop.append(child)

    best = min(pop, key=lambda sol: cost(sol, matrix))
    return best, cost(best, matrix)
