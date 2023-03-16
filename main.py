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
    machineSetTriangular = []
    jobMachineDictTriangular = {}
    machineSetPref = []
    jobMachineDictPref = {}
    numJobs=30
    for i in range(1,numJobs):
        numOperations = np.random.normal(5, 0.1, 1)
        numOps=math.floor(numOperations[0])
        if numOps <=2:
            numOps=3
        for j in range(1,numOps):
            uniNum=math.floor(np.random.uniform(1,18,1)[0])
            triNum=math.floor(np.random.triangular(1,5,18,1))
            while (uniNum in machineSet):
                uniNum = math.floor(np.random.uniform(1, 18, 1)[0])
            machineSet.append(uniNum)
            while (triNum in machineSetTriangular):
                triNum = math.floor(np.random.uniform(1, 18, 1)[0])
            machineSetTriangular.append(triNum)
            prefNum=np.random.choice(np.arange(1, 19), p=[0.1, 0.1,0.05, 0.05, 0.05, 0.05,0.05, 0.05,0.05, 0.05,0.05, 0.05,0.05, 0.05,0.05, 0.05,0.05, 0.05])
            while (prefNum in machineSetPref):
                prefNum = np.random.choice(np.arange(1, 19),
                                           p=[0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                                              0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
            machineSetPref.append(prefNum)

        jobMachineDict[i]=machineSet
        jobMachineDictTriangular[i]=machineSetTriangular
        jobMachineDictPref[i]=machineSetPref
        machineSet = []
        machineSetTriangular = []
        machineSetPref = []

    G = nx.erdos_renyi_graph(3, 0.88)
    nx.draw(G, with_labels=True)
    plt.show()
    H = nx.barabasi_albert_graph(3, 2)
    nx.draw(H, with_labels=True)
    plt.show()
    print(jobMachineDict)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

