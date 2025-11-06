def cost(solution, matrix):
    total = 0
    for i in range(len(solution) - 1):
        total += matrix[solution[i]][solution[i + 1]]
    # Return to start
    total += matrix[solution[-1]][solution[0]]
    return total
