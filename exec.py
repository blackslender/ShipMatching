import os
import code
import numpy as np
import pandas as pd


def printResult(res, data):
    result = list(res)
    result.sort()
    profitability = 0
    for p in result:
        if data[p[0]][p[1]] > 0:
            print("#" + str(p[0]+1) + " ship picks #" + str(p[1]+1) + " cargo")
            profitability += data[p[0]][p[1]]
    print("Profitability: " + str(profitability))
    return None


if __name__ == "__main__":
    import sys
    arg = sys.argv[1:]
    if len(arg) == 0:
        print("Running all testcases in \"testcases\" folder")
        for filename in os.listdir('./testcases'):
            print("Processing " + filename)
            path = './testcases/' + filename
            data = pd.read_csv(path).drop("Ship", 1).to_numpy()
            result = code.match(data)
            printResult(result, data)
            print("")
    else:
        for filename in arg:
            print("Processing " + filename)
            path = filename
            data = pd.read_csv(path).drop("Ship", 1).to_numpy()
            result = code.match(data)
            printResult(result, data)
            print("")
