import numpy as np
import math
import matplotlib.pyplot as plt



def visulaize_clusters(c1,c2,g1,g2):
    pts1x=list(list(zip(*c1))[0])
    pts1y=list(list(zip(*c1))[1])

    pts2x=list(list(zip(*c2))[0])
    pts2y=list(list(zip(*c2))[1])

    plt.scatter(pts1x,pts1y,color='red')
    plt.scatter(pts2x,pts2y,color='blue')
    plt.legend(['Cluster 1','Cluster 2'])
    plt.plot(g1[0],g1[1],'+',color='red', ms=20)
    plt.plot(g2[0],g2[1],'+',color='blue',ms=20)



    plt.show()

def predict(point):
    global final_centroids
    cents=final_centroids
    c1=cents[0]
    c2=cents[1]

    if(getdistance(point,c1)<getdistance(point,c2)):
        return 'cluster1'
    else:
        return 'cluster2'


def calcnewcentroid(c):
    cent=tuple()
    centx=0.0
    centy=0.0
    for point in c:
        centx=centx+point[0]
        centy=centy+point[1]
    centx=round(centx/len(c),2)
    centy=round(centy/len(c),2)

    cent=(centx,centy)

    return cent


def getdistance(point,p):
    #print(math.sqrt(pow((point[1]-p[1]),2)+pow((point[0]-p[0]),2)))
    return math.sqrt(pow((point[1]-p[1]),2)+pow((point[0]-p[0]),2))

def createclusters(pts,M1,M2):
    clusternum=[]
    cluster1=[]
    cluster2=[]
    for point in pts:
        d1=getdistance(point,M1)
        d2=getdistance(point,M2)
        if(d1<d2):
            cluster1.append(point)
        else:
            cluster2.append(point)
    newM1=calcnewcentroid(cluster1)
    newM2=calcnewcentroid(cluster2)
    print('Cluster 1 ',cluster1)
    print('Cluster 2',cluster2)
    print('Centroid 1 ',M1)
    print('Centroid 2 ',M2)

    visulaize_clusters(cluster1,cluster2,M1,M2)

    if(newM1==M1 and newM2==M2):

        global final_centroids
        final_centroids.append(newM1)
        final_centroids.append(newM2)

        print('Final clusters are \n',cluster1,'\n',cluster2)
        return
    else:
        createclusters(pts,newM1,newM2)



points=[(0.1,0.6),(0.15,0.71),(0.08,0.9),(0.16,0.85),(0.2,0.3),(0.25,0.5),(0.24,0.1),(0.3,0.2)]

m1=points[0]
m2=points[7]  #no visible change with these initial cetroids as given in assignment. Try better centroids

final_centroids=[]

createclusters(points,m1,m2)

print('Final Centroids ',final_centroids)

trailpoint=points[5]   #point 6 as per assignment
print('Predicted point lies in ',predict(trailpoint))
