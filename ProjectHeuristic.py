import numpy as np
import pandas as pd
import os
import openpyxl
import matplotlib.pyplot as plt

def indicies(list,searchVal):
    arryIndicies=[]
    for itr in range(len(list)):
        # check the condition
        if (list[itr] == searchVal):
            arryIndicies.append(itr)
    return arryIndicies

def construction(numBusses, sij, dj, numbusRequiredPerSchool):
    busSchedule = {}
    # intialize the busses
    for i in range(1, numBusses+1):
        busSchedule[i] = []
    currBusToSchedule = 1
    jobSetNotScheduled = dj.copy()
    jobSetScheduled=[]

    while len(jobSetNotScheduled) != 0:
        min_value = min(jobSetNotScheduled)
        min_index = dj.index(min_value)
        throw_index = jobSetNotScheduled.index(min_value)
        del jobSetNotScheduled[throw_index]
        ii = indicies(dj,min_value)
        once=True
        if len(ii)>1:
            #then there was a tie check for the one not scheduled
            for j in range(0,len(ii)):
                if jobSetScheduled.count(ii[j])==0 and once==True:
                    min_index=ii[j]
                    once = False

        jobSetScheduled.append(min_index)

        for busNum in range(1, numbusRequiredPerSchool[min_index]+1):
            if currBusToSchedule > numBusses:
                currBusToSchedule = 1
            busSchedule[currBusToSchedule].append(min_index)
            currBusToSchedule += 1
    return busSchedule

def EDDandShortestProcessingTime(numBusses, sij, dj, numbusRequiredPerSchool):
    busSchedule = {}
    # intialize the busses
    for i in range(1, numBusses + 1):
        busSchedule[i] = []
    currBusToSchedule = 1
    jobSetNotScheduled = dj.copy()
    jobSetScheduled = []
    jobNotMap={}
    for r in range(0,len(dj)):
        jobNotMap[r]=numbusRequiredPerSchool[r]

    while len(jobSetNotScheduled) != 0:
        #find the ealiest due date
        min_value = min(jobSetNotScheduled)
        min_index = dj.index(min_value)
        throw_index = jobSetNotScheduled.index(min_value)
        #del jobSetNotScheduled[throw_index]
        ii = indicies(dj, min_value)
        once = True
        tied_index=[]
        dictbusNumTimeRegion= {}
        if len(ii) > 1:
            # then there was a tie check for the one(s) not scheduled then find the one with the shortest setup+processing time to schedule it
            for j in range(0,len(ii)):
                if jobSetScheduled.count(ii[j])==0 and once==True:
                    tied_index.append(ii[j])
            for ind in range(0,len(tied_index)): jobSetNotScheduled.remove(min_value)
            while len(tied_index)>0:
                for busNum in range(1, numBusses+1):
                    for ind in range(0,len(tied_index)):
                    #get setup time
                        if busSchedule[busNum]==[]:
                            totalTimestr=pj[tied_index[ind]]
                            x = totalTimestr.split('-')
                            addTotal = 2* int(np.random.uniform(int(x[0]), int(x[1]), 1))
                        else:
                            lastIndexBus=busSchedule[busNum][-1]
                            setUpTimestr=sij[lastIndexBus][tied_index[ind]]
                            if setUpTimestr=='-':
                                setUpTimestr=pj[tied_index[ind]]
                                x = setUpTimestr.split('-')
                                addTotal = 2 * int(np.random.uniform(int(x[0]), int(x[1]), 1))
                            else:
                                x = setUpTimestr.split('-')
                                setUpTime = int(np.random.uniform(int(x[0]), int(x[1]), 1))
                                processingTimeBusstr=pj[tied_index[ind]]
                                x = processingTimeBusstr.split('-')
                                processingTimeBus=int(np.random.uniform(int(x[0]), int(x[1]), 1))
                                addTotal= setUpTime+processingTimeBus
                        if tied_index[ind] in dictbusNumTimeRegion:
                            dictbusNumTimeRegion[tied_index[ind]].append(busNum)
                            dictbusNumTimeRegion[tied_index[ind]].append(addTotal)
                        else :
                            dictbusNumTimeRegion[tied_index[ind]]=[busNum,addTotal]
                    #if min then set that as the region
                minTime=100000
                for region in dictbusNumTimeRegion:
                    for r in range(1,len(dictbusNumTimeRegion[region]),2):
                        if dictbusNumTimeRegion[region][r]< minTime:
                            minTime=dictbusNumTimeRegion[region][r]
                            busassigned=dictbusNumTimeRegion[region][r-1]
                    busSchedule[busassigned].append(region)
                    jobNotMap[region]=jobNotMap[region]-1
                    minTime=100000
                    if jobNotMap[region]==0:
                        tied_index.remove(region)
                dictbusNumTimeRegion = {}
        else:
            del jobSetNotScheduled[throw_index]
            jobSetScheduled.append(min_index)
            for busNum in range(1, numbusRequiredPerSchool[min_index] + 1):
                if currBusToSchedule > numBusses:
                    currBusToSchedule = 1
                busSchedule[currBusToSchedule].append(min_index)
                currBusToSchedule += 1
    return busSchedule

def expectedSchedule(busSchedule,pj, dj,sij):
    dictbusNumCmaxLmax={}
    for i in range(0,1000):
        busScheduleExpTime = {}
        #bus number the Cmax and then the Lmax
        busNumCmaxLmax = []
        j=1
        for bus in busSchedule:
            expTime = []
            Lmax=0
            index=busSchedule[bus][0]
            processingDist=pj[index]
            x = processingDist.split('-')
            toRegion=int(np.random.uniform(int(x[0]),int(x[1]),1))
            expTime.append(2*toRegion)
            busNumCmaxLmax.append(bus)
            if 2*toRegion>dj[index]:
                Lmax+=2*toRegion-dj[index]
            tStart=2*toRegion
            for h in range(0,len(busSchedule[bus])-1):
                indexTo = busSchedule[bus][h+1]
                indexFrom= busSchedule[bus][h]
                if indexTo==indexFrom:
                    processingDist = pj[indexTo]
                    x = processingDist.split('-')
                    samplePj2 = 2*int(np.random.uniform(int(x[0]), int(x[1]), 1))
                    expTime.append(samplePj2*2)
                    samplePj3=0
                else:
                    processingDist = sij[indexFrom][indexTo]
                    x = processingDist.split('-')
                    samplePj2 = int(np.random.uniform(int(x[0]), int(x[1]), 1))
                    processingDist = pj[indexTo]
                    x = processingDist.split('-')
                    samplePj3 = int(np.random.uniform(int(x[0]), int(x[1]), 1))
                    expTime.append(samplePj3)
                    expTime.append(samplePj2)
                #get the sample by splitting the string from pj
                #uniform sample
                if tStart+samplePj2+samplePj3>dj[indexTo]:
                    Lmax+=tStart+samplePj2+samplePj3-dj[indexTo]
                tStart+=samplePj2+samplePj3
            busScheduleExpTime[j]=expTime
            completionTime = sum(expTime)
            busNumCmaxLmax.append(completionTime)
            busNumCmaxLmax.append(Lmax)
            j+=1
        #print(busScheduleExpTime)
        #print(busNumCmaxLmax)
        dictbusNumCmaxLmax[i]=busNumCmaxLmax
    return dictbusNumCmaxLmax

def map(expSchedule):
    #get all the Cmax
    #get all the Lmax
    completionTime=[]
    latenessTimes=[]
    Cmax=[]
    Lmax=[]
    for i in range(0,100):
        arr=expSchedule[i]
        for j in range (1,len(arr),3):
            completionTime.append(arr[j])
        for j in range(2,len(arr),3):
            latenessTimes.append(arr[j])
        Cmax.append(max(completionTime))
        Lmax.append(max(latenessTimes))
    dfCmax = pd.DataFrame(Cmax, columns=['Cmax Values'])
    plt.hist(dfCmax)
    plt.title('Cmax')
    plt.xlabel('Counts')
    plt.ylabel('Time')
    plt.show()
    dfLmax=pd.DataFrame(Lmax,columns=['Lmax Values'])
    plt.hist(dfLmax)
    plt.title('Lmax')
    plt.xlabel('Counts')
    plt.ylabel('Time')
    plt.show()

if __name__ == '__main__':
    xls = pd.ExcelFile(r'C:\Users\sheil\Documents\University4B\MSCI555\Instructor project\data\dataFile.xlsx')
    sijDF = pd.read_excel(xls, 'S_ij')
    djDF = pd.read_excel(xls, 'dj')
    pjDF = pd.read_excel(xls, 'pj')
    numBusDF = pd.read_excel(xls, 'school')
    arrsij = sijDF.to_numpy()
    sij=arrsij[:,1:]
    #sij = [["-", "12-22", "10-20"], ["9-16", "-", "18-35"], ["10-20", "18-35", "-"]]
    dj2D=djDF.to_numpy()
    dj=[]
    pj=[]
    for ele in range(0,len(dj2D)):
        dj.append(dj2D[ele][0])
    #dj = [100, 130, 130]
    pj2D=pjDF.to_numpy()
    for ele in range(0,len(pj2D)):
        pj.append(pj2D[ele][0])
    #pj = ["5-9", "7-10", "4-6"]
    arrschoolID = numBusDF.to_numpy()
    schoolID = arrschoolID[:, 0]
    numbusRequiredPerSchool=arrschoolID[:,1]
    #schoolID = [1, 2, 3]
    numBusses = 50  # set as required
    busSchedule = {}
    #numbusRequiredPerSchool = [7, 9, 5]
    mapIndexOntoSchoolAndRegionID = {}
    for i in range(0, len(sij)):
        mapIndexOntoSchoolAndRegionID[i] = schoolID[i]
    busScheduleEDDSPT = EDDandShortestProcessingTime(numBusses, sij, dj, numbusRequiredPerSchool)
    print(busScheduleEDDSPT)
    busScheduleEDD = construction(numBusses, sij, dj, numbusRequiredPerSchool)
    print(busScheduleEDD)
    expScheduleEDDSPT=expectedSchedule(busScheduleEDDSPT,pj, dj,sij)
    expScheduleEDD=expectedSchedule(busScheduleEDD, pj, dj, sij)
    print(expScheduleEDDSPT)
    print(expScheduleEDD)
    map(expScheduleEDD)
    map(expScheduleEDDSPT)

