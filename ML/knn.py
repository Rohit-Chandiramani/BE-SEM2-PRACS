import numpy as np
import math


def getdistance(point,p):
    #print(math.sqrt(pow((point[1]-p[1]),2)+pow((point[0]-p[0]),2)))
    return math.sqrt(pow((point[1]-p[1]),2)+pow((point[0]-p[0]),2))


def knn(pts,p,K):
    distance={}
    for point in list(pts.keys()):
        if (getdistance(point,p) in list(distance.keys())) and  distance[getdistance(point,p)]!=[]:    #checking if one value leads to two points thn store them as a list
            distance[getdistance(point,p)].append(point)
        else:
            distance[getdistance(point,p)]=[point]

    print(distance)


    minpoints=[]

    for i in range(0,K):
        minpoints.append(distance[min(list(distance.keys()))][0])
        if len(distance[min(list(distance.keys()))])==1:   #if this was the last point with same distance then remove distance completely
            del distance[min(list(distance.keys()))]
        else:
            distance[min(list(distance.keys()))].remove(distance[min(list(distance.keys()))][0])  #else remove only current point and keep other point
        #print(minpoints)
        #print(distance)

    print(minpoints)

    classes=[]

    for point in minpoints:
        classes.append(pts[point])

    print('output classes ',classes)

    counts={}

    for c in list(set(classes)):
        counts[classes.count(c)]=c
    print(counts)
    print('Output class ',counts[max(list(counts.keys()))])


    #weighted knn classifaction

    distanceofminpoints=[]
    for point in minpoints:
        distanceofminpoints.append(getdistance(point,p))
    #print(distanceofminpoints)

    weightedclassmetric={}
    for u in list(set(classes)):
        weightedclassmetric[u]=0


        for i in range(0,len(classes)):
            if(u==classes[i]):
                weightedclassmetric[u]=weightedclassmetric[u]+(1/distanceofminpoints[i])   #weighting the outputs by 1/distance as distance increases weight decreases
    print('Weighted metric per class ',weightedclassmetric)

    maxweightedmetric=max(list(weightedclassmetric.values()))   #getting maximum weight

    for i in range(0,len(weightedclassmetric)):   #finding class with maximum weight
        if list(weightedclassmetric.values())[i]==maxweightedmetric:
            print('Output class by weighted KNN is ',list(weightedclassmetric.keys())[0])
            break



#main

datapoints={(2,4):1,(4,6):1,(4,2):1,(6,4):1,(4,4):2,(6,2):2}
newpoint=(6,6)

knn(datapoints,newpoint,3)
