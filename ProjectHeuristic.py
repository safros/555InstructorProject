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

def expectedSchedule(busSchedule,pj, dj):
    for i in range(0,10):
        busScheduleExpTime = {}
        #bus number the Cmax and then the Lmax
        busNumCmaxLmax = []
        j=0
        for bus in busSchedule:
            expTime = []
            Lmax=0
            index=busSchedule[bus][0]
            processingDist=pj[index]
            x = processingDist.split('-')
            samplePj1=np.random.uniform(int(x[0]),int(x[1]),1)
            expTime.append(2*int(samplePj1[0]))
            busNumCmaxLmax.append(bus)
            if 2*samplePj1[0]>dj[index]:
                Lmax+=2*samplePj1[0]-dj[index]
            tStart=2*samplePj1[0]
            for h in range(0,len(busSchedule[bus])-1):
                index = busSchedule[bus][h+1]
                processingDist = sij[h][h+1]
                x = processingDist.split('-')
                samplePj2 = np.random.uniform(int(x[0]), int(x[1]), 1)
                expTime.append(int(samplePj2[0]))
                processingDist = pj[h+1]
                x = processingDist.split('-')
                samplePj3 = np.random.uniform(int(x[0]), int(x[1]), 1)
                expTime.append(int(samplePj3[0]))
                if tStart+samplePj2[0]+samplePj3[0]>dj[index]:
                    Lmax+=tStart+samplePj2[0]+samplePj3[0]-dj[index]
                tStart+=samplePj2[0]+samplePj3[0]
            busScheduleExpTime[j]=expTime
            completionTime = sum(expTime)
            busNumCmaxLmax.append(completionTime)
            busNumCmaxLmax.append(int(Lmax))
            j+=1
        print(busScheduleExpTime)
        print(busNumCmaxLmax)

if __name__ == '__main__':
    sij = [["-", "12-22", "10-20"], ["9-16", "-", "18-35"], ["10-20", "18-35", "-"]]
    dj = [100, 130, 130]
    pj = ["5-9", "7-10", "4-6"]
    schoolID = [1, 2, 3]
    numBusses = 10  # set as required
    busSchedule = {}
    numbusRequiredPerSchool = [7, 9, 5]
    mapIndexOntoSchoolAndRegionID = {}
    for i in range(0, len(sij)):
        mapIndexOntoSchoolAndRegionID[i] = schoolID[i]

    busSchedule = construction(numBusses, sij, dj, numbusRequiredPerSchool)
    print(busSchedule)
    expectedSchedule(busSchedule, pj, dj)
