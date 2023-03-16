# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#importing the networkx library
import networkx as nx
import numpy as np
#importing the matplotlib library for plotting the graph
import matplotlib.pyplot as plt
import math


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    machineSet=[]
    jobMachineDict={}
    for i in range(1,30):
        numOperations = np.random.normal(5, 0.05, 1)
        numOps=math.floor(numOperations[0])
        for j in range(1,numOps):
            machineSet.append(math.floor(np.random.uniform(1,18,1)[0]))
            # machineSet.append(np.random.triangular(1,5,18,1))
        jobMachineDict[i]=machineSet
        machineSet = []

    G = nx.erdos_renyi_graph(3, 0.88)
    nx.draw(G, with_labels=True)
    plt.show()
    H = nx.barabasi_albert_graph(3, 2)
    nx.draw(H, with_labels=True)
    plt.show()
    print(jobMachineDict)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

