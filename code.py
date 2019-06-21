
import pandas as pd
import numpy as np


def run(testpath):
    if testpath is not None:
        data = pd.read_csv(testpath).drop("Ship", 1)
        profit = data.to_numpy()
    else:
        profit = [[162769, 357472, 171622, 880829, 470885],
                  [354168, 387057, 329358, 386227, 49563],
                  [627831, 794682, 662168, 487391, 517803],
                  [642263, 177979, 843284, 863671, 725443],
                  [514798, 397148, 807740, 118587, 6402],
                  [940978, 268597, 826364, 521143, 734403]]
        profit = np.array(profit)

    nShips, nCargos = profit.shape[0], profit.shape[1]
    result = [(0, 0)]*min(nShips, nCargos)
    usedShip = [False]*nShips
    usedCargo = [False]*nCargos

    # Initial pairs
    for i in range(min([nShips, nCargos])):
        result[i] = (i, i)
        m, mi = -1, -1
        for cargo in range(nCargos):
            if not usedCargo[cargo]:
                if m < profit[i][cargo]:
                    m = profit[i][cargo]
                    mi = cargo

        result[i] = (i, mi)
        usedShip[i] = True
        usedCargo[mi] = True

    def currentVal(result, profit):
        s = 0
        for p in result:
            s += profit[p[0]][p[1]]
        return s

    # Start optimization
    optimizable = True
    step = 0

    while optimizable:
        optimizable = False
        # Check if there is any cargo that can be replaced to any current picked cargo
        # to make a better result
        bestCargoi = -1
        bestCargo = -1
        bestCargoVal = 0
        for cargo in range(nCargos):
            if usedCargo[cargo]:
                continue
            for i in range(len(result)):
                if (bestCargoVal < -profit[result[i][0]][result[i][1]] + profit[result[i][0]][cargo]):
                    optimizable = True
                    # result[i] = (result[i][0], cargo)
                    # usedCargo[result[i][1]] = False
                    # usedCargo[cargo] = True
                    bestCargoi = i
                    bestCargo = cargo
                    bestCargoVal = - \
                        profit[result[i][0]][result[i][1]] + \
                        profit[result[i][0]][cargo]
        # Check if there is any ship that can be replaced to current used ship
        # to make a better result
        bestShipi = -1
        bestShip = -1
        bestShipVal = 0
        for ship in range(nShips):
            if usedShip[ship]:
                continue
            for i in range(len(result)):
                if (bestShipVal < -profit[result[i][0]][result[i][1]] + profit[ship][result[i][1]]):
                    # result[i] = (ship, result[i][1])
                    # usedShip[result[i][0]] = False
                    # usedCargo[ship] = True
                    bestShipi = i
                    bestShip = ship
                    bestShipVal = - profit[result[i][0]
                                           ][result[i][1]] + profit[ship][result[i][1]]
        # Check if there is any pair that can be swapped
        # to make a better result
        swapi = -1
        swapj = -1
        swapVal = 0
        for i in range(len(result)):
            for j in range(i):
                if (swapVal < -(profit[result[i][0]][result[i][1]] + profit[result[j][0]][result[j][1]])
                        + (profit[result[i][0]][result[j][1]] + profit[result[j][0]][result[i][1]])):
                    # p1 = (result[i][0], result[j][1])
                    # p2 = (result[j][0], result[i][1])
                    # result[i] = p1
                    # result[j] = p2
                    swapi = i
                    swapj = j
                    swapVal = -(profit[result[i][0]][result[i][1]] + profit[result[j][0]][result[j][1]]) + (
                        profit[result[i][0]][result[j][1]] + profit[result[j][0]][result[i][1]])
        if (swapVal > bestShipVal and swapVal > bestCargoVal):
            # print('Doing swap')
            i, j = swapi, swapj
            p1 = (result[i][0], result[j][1])
            p2 = (result[j][0], result[i][1])
            result[i] = p1
            result[j] = p2
            optimizable = True
        elif (bestShipVal > bestCargoVal):
            # print('Doing change ship')
            i, ship = bestShipi, bestShip
            usedShip[result[i][0]] = False
            usedShip[ship] = True
            result[i] = (ship, result[i][1])
            optimizable = True
        elif (bestCargoVal > 0):
            # print('Doing change cargo')
            i, cargo = bestCargoi, bestCargo
            usedCargo[result[i][1]] = False
            usedCargo[cargo] = True
            result[i] = (result[i][0], cargo)
            optimizable = True
        else:
            optimizable = False
        step += 1
    result.sort()
    return (result, currentVal(result, profit))


if __name__ == "__main__":
    import sys
    arg = sys.argv[1:]
    print("Result for manual testcase:")
    pairs, profit = run(arg[0])
    print("Profitability: " + str(profit))
    for p in pairs:
        print("#" + str(p[0]+1) + " ship pick #" + str(p[1]+1) + " cargo")
    print("")
