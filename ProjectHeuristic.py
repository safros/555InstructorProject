import numpy as np

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


if __name__ == '__main__':
    sij = [[9, 22, 20], [16, 10, 35], [20, 35, 6]]
    dj = [100, 130, 130]
    schoolID = [1, 2, 3]
    numBusses = 10  # set as required
    busSchedule = {}
    numbusRequiredPerSchool = [7, 9, 5]
    mapIndexOntoSchoolAndRegionID = {}
    for i in range(0, len(sij)):
        mapIndexOntoSchoolAndRegionID[i] = schoolID[i]

    busSchedule = construction(numBusses, sij, dj, numbusRequiredPerSchool)
    print(busSchedule)
