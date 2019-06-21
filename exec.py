import os
import code
for filename in os.listdir('./testcases'):
    path = './testcases/' + filename
    pairs, profit = code.run(path)
    print("Result for testcase " + filename)
    print("Profitability: " + str(profit))
    i = 0
    for p in pairs:
        while i < p[0]:
            i += 1
            print("#" + str(i) + " is free")
        print("#" + str(p[0]+1) + " ship picks #" + str(p[1]+1) + " cargo")
        i += 1
    print("")
