def match(data):
    import pulp
    import numpy as np
    problem = pulp.LpProblem("ShipMatching", pulp.LpMaximize)

    nShips, nCargos = data.shape

    variables = [[pulp.LpVariable("x_" + str(i) + "_" + str(j), 0, 1, cat="Integer")
                  for j in range(nCargos)] for i in range(nShips)]

    # Contraints

    for ship in range(nShips):
        s = 0
        for cargo in range(nCargos):
            s += variables[ship][cargo]

        problem += (s <= 1)

    for cargo in range(nCargos):
        s = 0
        for ship in range(nShips):
            s += variables[ship][cargo]

        problem += (s <= 1)

    opt = 0
    for ship in range(nShips):
        for cargo in range(nCargos):
            opt += data[ship][cargo]*variables[ship][cargo]

    problem += opt

    # print(problem)
    problem.solve()

    result = set()
    for ship in range(nShips):
        for cargo in range(nCargos):
            if variables[ship][cargo].varValue > 0.5:
                result.add((ship, cargo))

    return result
