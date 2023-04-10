import random
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def shortestUnitFirst(demand, pij, pij2, seq1, seq2):
    schedule = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    JobsNotScheduled = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 4, 15: 4,
                        16: 4}
    JobsScheduled = {}
    demandCopy = demand.copy()
    for m in range(1, 11):
        # for each machine find the jobs that need ot be placed on it
        jobNumPijDemand = {}
        listJobs = returnListOfJobsM(seq1, m, pij)
        listJobs2 = returnListOfJobs(seq2, m, pij2)
        randomlist = []
        indxer = 0
        for li in listJobs[0]:
            jobNumPijDemand[li] = listJobs[1][indxer] * demandCopy[li - 1]
            indxer += 1
        indxer = 0
        for li in listJobs2[0]:
            jobNumPijDemand[li] = listJobs2[1][indxer] * demandCopy[li - 1]
            indxer += 1
        sortedList = sorted(jobNumPijDemand.items(), key=lambda x: x[1])
        for idx in sortedList:
            schedule[m].append(idx[0])
    # with schedule assign random batch sizes
    for li in range(0, 16):
        randomlist.append(random.randint(1, demand[li] // 100))
    dictJobNumBatchInfo = {}
    for num in range(0, len(randomlist)):
        dictJobNumBatchInfo[num + 1] = returnBatches(demand[num], randomlist[num])
    return schedule, dictJobNumBatchInfo


def returnBatches(demandNum, numBatches):
    b1 = demandNum / numBatches
    b2 = math.floor(b1)
    b3 = b2 * numBatches
    b4 = demandNum - b3
    batches = []
    for num in range(0, numBatches - 1):
        batches.append(b2)
    batches.append(b2 + b4)
    return batches


def returnListOfJobsM(seq1, m, pij):
    li = []
    pijli = []
    for i in range(0, len(seq1)):
        for k in range(0, len(seq1[0])):
            if seq1[i][k] == m:
                li.append(1 + i)
                pijli.append(pij[i][k])
    return li, pijli


def returnListOfJobs(seq2, m, pij2):
    li = []
    pijli = []
    for i in range(0, len(seq1)):
        for k in range(0, len(seq2[0])):
            if seq2[i][k] == m:
                li.append(9 + i)
                pijli.append(pij2[i][k])
    return li, pijli

def SQNO(demand, pij, pij2, seq1, seq2):
    randomlist = []
    for li in range(0, 16):
        randomlist.append(random.randint(1, demand[li] // 100))
    dictJobNumBatchInfo = {}
    for num in range(0, len(randomlist)):
        dictJobNumBatchInfo[num + 1] = returnBatches(demand[num], randomlist[num])
    batchperJob1=dictJobNumBatchInfo.copy()
    timeDict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [],
                15: [], 16: []}
    machineQeue = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    graphDict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    timeIndex = []
    machineFree = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    jobInprocessing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    batchSizeThatwasOnMachine = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # schedule for t=0 the queue for the machines
    for j in range(1, 9):
        for b in range(0, len(batchperJob1[j])):
            machineQeue[seq1[j - 1][0]].append(j)
            machineQeue[seq1[j - 1][0]].append(batchperJob1[j][b])
    for j in range(9, 17):
        for b in range(0, len(batchperJob1[j])):
            machineQeue[seq2[j - 9][0]].append(j)
            machineQeue[seq2[j - 9][0]].append(batchperJob1[j][b])
    t = 0
    while allDone(machineQeue):
        for mach in range (1, 11):
            if len(machineQeue[mach]) != 0 and machineFree[mach - 1] <= t:
                if len(machineQeue[mach]) == 2:
                    jobToSchedule=machineQeue[mach][0]
                    batchsize=machineQeue[mach][1]
                    if jobToSchedule < 9:
                        processingTime = pij[jobToSchedule - 1][seq1[jobToSchedule - 1].index(mach)]
                    else:
                        processingTime = pij2[jobToSchedule - 9][seq2[jobToSchedule - 9].index(mach)]
                    idx = machineQeue[mach].index(jobToSchedule)
                    machineFree[mach - 1] = t + processingTime * batchsize
                    jobInprocessing[mach - 1] = jobToSchedule
                    batchSizeThatwasOnMachine[mach - 1] = batchsize
                    timeDict[jobToSchedule].append(t + processingTime * batchsize)
                    # remove job from queue
                    machineQeue[mach] = machineQeue[mach][:idx] + machineQeue[mach][idx + 2:]
                else:
                    jobToSchedule=findJobWithNextShortestQueue(machineQeue,seq1, seq2,mach)
                    idx = machineQeue[mach].index(jobToSchedule)
                    batchsize = machineQeue[mach][idx+1]
                    if jobToSchedule < 9:
                        processingTime = pij[jobToSchedule - 1][seq1[jobToSchedule - 1].index(mach)]
                    else:
                        processingTime = pij2[jobToSchedule - 9][seq2[jobToSchedule - 9].index(mach)]
                    machineFree[mach - 1] = t + processingTime * batchsize
                    jobInprocessing[mach - 1] = jobToSchedule
                    batchSizeThatwasOnMachine[mach - 1] = batchsize
                    timeDict[jobToSchedule].append(t + processingTime * batchsize)
                    # remove job from queue
                    machineQeue[mach] = machineQeue[mach][:idx] + machineQeue[mach][idx + 2:]
        t += 1
        # when a job completes processing put it in the next queue and free up the machine it was on
        for machineNum in range(1, 11):
            if machineFree[machineNum - 1] == t:
                jobToQueue = jobInprocessing[machineNum - 1]
                if jobToQueue < 9:
                    IndexmachineToGoOn = seq1[jobToQueue - 1].index(machineNum) + 1
                    # check if there is no more machines to go on
                    if len(seq1[jobToQueue - 1]) > IndexmachineToGoOn:
                        machineQeue[seq1[jobToQueue - 1][IndexmachineToGoOn]].append(jobToQueue)
                        machineQeue[seq1[jobToQueue - 1][IndexmachineToGoOn]].append(batchSizeThatwasOnMachine[machineNum - 1])
                else:
                    IndexmachineToGoOn = seq2[jobToQueue - 9].index(machineNum) + 1
                    # check if there is no more machines to go on
                    if len(seq2[jobToQueue - 9]) > IndexmachineToGoOn:
                        machineQeue[seq2[jobToQueue - 9][IndexmachineToGoOn]].append(jobToQueue)
                        machineQeue[seq2[jobToQueue - 9][IndexmachineToGoOn]].append(batchSizeThatwasOnMachine[machineNum - 1])

    for itrator in range(1, 17):
        print("SQNO: Job {} time job completed: {}".format(itrator, max(timeDict[itrator])))

def findJobWithNextShortestQueue(machineQeue,seq1, seq2,machineNum):
    minimumQueue=10000000
    for jobInqueue in range (0,len(machineQeue[machineNum]),2):
        jobNum = machineQeue[machineNum][jobInqueue]
        if jobNum<9:
            nextMachineIdx =seq1[jobNum-1].index(machineNum)+1
            # check if there is no more machines to go on
            if len(seq1[jobNum -1]) < nextMachineIdx:
                return jobNum
            nextMachine=seq1[jobNum-1][nextMachineIdx-1]
        else:
            nextMachineIdx = seq2[jobNum-9].index(machineNum) + 1
            if len(seq2[jobNum -9]) < nextMachineIdx:
                return jobNum
            nextMachine = seq2[jobNum - 9][nextMachineIdx-1]
        queueLengthNextMachine =len(machineQeue[nextMachine])
        if queueLengthNextMachine==0: return jobNum
        if queueLengthNextMachine<minimumQueue:
            jobToReturn=jobNum
    return jobToReturn

def Lmax(schedule,batchperJob,seq1,seq2,pij, pij2):
    schedule1=schedule.copy()
    batchperJob1=batchperJob.copy()
    timeDict={1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],11:[],12:[],13:[],14:[],15:[],16:[]}
    machineQeue={1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    graphDict={1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    timeIndex=[]
    machineFree=[0, 0,0,0,0,0,0,0,0,0]
    jobInprocessing=[0, 0,0,0,0,0,0,0,0,0]
    batchSizeThatwasOnMachine=[0, 0,0,0,0,0,0,0,0,0]
    indexer=[]
    maxIndex=[]
    counter=0
    for d in range(1,11):
        maxIndex.append(len(schedule[d]))
        indexer.append(0)

    #schedule for t=0 the queue for the machines
    for j in range (1,9):
        for b in range(0,len(batchperJob1[j])):
            machineQeue[seq1[j-1][0]].append(j)
            machineQeue[seq1[j-1][0]].append(batchperJob1[j][b])
    for j in range (9,17):
        for b in range(0,len(batchperJob1[j])):
            machineQeue[seq2[j-9][0]].append(j)
            machineQeue[seq2[j-9][0]].append(batchperJob1[j][b])
    t=0
    while allDone(machineQeue):
        for z in range (1,11):
            if len(machineQeue[z])!=0 and machineFree[z-1]<=t:
                graphDict[z].append(len(machineQeue[z]))
                timeIndex.append(t)
                jobToSchedule=schedule1[z][indexer[z-1]]
                if indexer[z - 1]+1<maxIndex[z-1]:
                    indexer[z - 1] += 1
                else:
                    indexer[z - 1]=0
                # check if the job is the queue of the machine if it is not then you cannot pick that job to schedule
                while machineQeue[z].count(jobToSchedule) == 0:
                    jobToSchedule = schedule1[z][indexer[z - 1]]
                    if indexer[z - 1] + 1 < maxIndex[z - 1]:
                        indexer[z - 1] += 1
                    else:
                        indexer[z - 1] = 0

                if jobToSchedule<9:
                    processingTime=pij[jobToSchedule-1][seq1[jobToSchedule-1].index(z)]
                else:
                    processingTime = pij2[jobToSchedule - 9][seq2[jobToSchedule - 9].index(z)]
                idx=machineQeue[z].index(jobToSchedule)
                machineFree[z-1]=t+ processingTime*machineQeue[z][idx+1]
                jobInprocessing[z-1]=jobToSchedule
                batchSizeThatwasOnMachine[z-1]=machineQeue[z][idx+1]
                timeDict[jobToSchedule].append(t + processingTime * machineQeue[z][idx + 1])
                #remove job from queue
                machineQeue[z]=machineQeue[z][:idx] + machineQeue[z][idx+2 :]
        t+=1
        #when a job completes processing put it in the next queue and free up the machine it was on
        for machineNum in range (1,11):
            if machineFree[machineNum-1]==t:
                jobToQueue=jobInprocessing[machineNum-1]
                if jobToQueue<9:
                    IndexmachineToGoOn = seq1[jobToQueue - 1].index(machineNum) + 1
                    # check if there is no more machines to go on
                    if len(seq1[jobToQueue - 1]) > IndexmachineToGoOn:
                        machineQeue[seq1[jobToQueue-1][IndexmachineToGoOn]].append(jobToQueue)
                        machineQeue[seq1[jobToQueue-1][IndexmachineToGoOn]].append(batchSizeThatwasOnMachine[machineNum-1])
                else:
                    IndexmachineToGoOn = seq2[jobToQueue - 9].index(machineNum) + 1
                    #check if there is no more machines to go on
                    if len(seq2[jobToQueue - 9])>IndexmachineToGoOn:
                        machineQeue[seq2[jobToQueue - 9][IndexmachineToGoOn]].append(jobToQueue)
                        machineQeue[seq2[jobToQueue - 9][IndexmachineToGoOn]].append(batchSizeThatwasOnMachine[machineNum - 1])
    #print("The completion time of each batch: {}".format(timeDict))
    for itrator in range(1,17):
        print("Job {} time job completed: {}".format(itrator,max(timeDict[itrator])))
    print(graphDict)

def allDone(machineQeue):
    for i in range (1,11):
        if len(machineQeue[i])!=0:
            return True
    return False

if __name__ == '__main__':
    random.seed(7)
    demand = [1018, 605, 577, 195, 1093, 1088, 241, 413, 478, 1150, 478, 163, 216, 867, 149, 543]
    demand2 = [1018, 1605, 577, 195, 1093, 1088, 241, 413, 478, 1150, 478, 163, 1216, 867, 149, 543]
    pij = [[1, 1, 1, 3, 1], [1, 2, 2, 1, 1], [2, 3, 3, 1, 1], [1, 3, 1, 1, 1], [3, 2, 3, 3, 1], [1, 3, 3, 3, 3],
           [1, 2, 3, 3, 2], [1, 3, 2, 1, 3]]
    pij2 = [[1, 2, 3, 1], [1, 1, 3, 2], [2, 3, 2, 3], [1, 2, 1, 2], [3, 1, 1, 1], [1, 3, 3, 3], [1, 2, 3, 3],
            [2, 3, 2, 2]]
    seq1 = [[5, 1, 8, 4, 6], [5, 1, 10, 7, 6], [5, 9, 3, 6, 7], [5, 1, 4, 6, 7], [5, 2, 3, 1, 7], [5, 2, 9, 6, 7],
            [5, 9, 4, 1, 7], [5, 2, 4, 6, 7]]
    seq2 = [[5, 1, 3, 6], [5, 1, 9, 6], [5, 1, 7, 6], [5, 10, 3, 6], [5, 2, 4, 6], [5, 1, 10, 7], [5, 9, 4, 7],
            [5, 2, 8, 6]]
    results=shortestUnitFirst(demand, pij, pij2, seq1, seq2)
    print("Schedule for the machine {} \nBatches for each job {}".format(results[0],results[1]))
    Lmax(results[0], results[1], seq1, seq2,pij, pij2)

    results = shortestUnitFirst(demand2, pij, pij2, seq1, seq2)
    print("Schedule for the machine {} \nBatches for each job {}".format(results[0], results[1]))
    Lmax(results[0], results[1], seq1, seq2, pij, pij2)

    SQNO(demand, pij, pij2, seq1, seq2)
    print("\n")
    SQNO(demand2, pij, pij2, seq1, seq2)
