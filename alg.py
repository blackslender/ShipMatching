import pulp
import numpy as np

class CustomError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def parse(result,data):
    jsonResult = []
    profitability = 0
    for x,y in result:
        jsonResult.append({
            "vessel": x+1,
            "cargo": y+1,
            "value": data[x][y]
        })
        profitability += data[x][y]
    return jsonResult, profitability

def cal(data):
    problem = pulp.LpProblem("ShipMatching", pulp.LpMaximize)
    if data is None:
        raise CustomError("Data is None")
    if len(data)==0:
        raise CustomError("Data has len 0")

    if type(data)==type([]):
        nShips, nCargos = len(data),len(data[0])
        for row in data:
            if len(row)!=nCargos:
                raise CustomError("Data dimension error, some value is missing")
    elif type(data) == type(np.array([])):
        nShips, nCargos = data.shape
    else:
        raise CustomError("Data type error")

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