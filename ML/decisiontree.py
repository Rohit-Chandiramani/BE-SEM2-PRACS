import numpy as np
import pandas as pd
import math
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import export_graphviz
import pydotplus

def entropyofoutput(X):
    unique=list(set(X))
    countperunique=[]
    count=0
    entropy=0
    for item in unique:
        count=0
        for i in range(0,14):
            if(X[i]==item):
                count=count+1
        countperunique.append(count)
    for value in countperunique:
        entropy=entropy+(-((value/14)*(math.log2(value/14))))
    #print(entropy)
    return entropy

def entropyforfeature(X,Y):
    uniquex=list(set(X))
    uniquey=list(set(Y))
    #print(uniquex)
    #print(uniquey)
    countperuniquey=[]
    countperuniquex=[]

    entropy=0
    for item in uniquex:
        countperuniquey=[]
        for value in uniquey:
            count2=0
            for i in range(0,len(Y)):
                if(X[i]==item and Y[i]==value):
                    count2=count2+1
            #print(count2)
            countperuniquey.append(count2)
        countperuniquex.append(countperuniquey)
    #print(countperuniquex)

    for l in countperuniquex:
        subval=0
        for item in l:
            if(item==0):
                subval=subval+0
            else:
                subval=subval+(-((item/sum(l))*(math.log2(item/sum(l)))))
                #print(subval)

        temp=(sum(l)/14)*subval
        #print(temp)
        entropy=entropy+((sum(l)/14)*subval)

    #print(entropy)
    return entropy


def getmaxgainfeature(entroot,entfeat):

    return entfeat[min(list(entfeat.keys()))],min(list(entfeat.keys()))



def buildtree(entr,entf,X,Y,tree):
    entf={}
    #print(len(X.columns))
    for i in range(0,len(X.columns)):
        entf[entropyforfeature(list(X.iloc[:,i]),list(Y))]=list(X.columns)[i]
    #print(entf)
    maxgainfeat,entr=getmaxgainfeature(entr,entf)
    #print(entf.keys())
    flag=0
    for val in list(entf.keys()):
        if(val!=0.0):
            flag=1
            break
    if(flag==0):
        tree.append(list(set(list(Y))))
        #print(tree)
        global fintree
        fintree=tree
        return
    entf={}
    #print(maxgainfeat)
    tree.append(maxgainfeat)
    unique=list(set(list(X[maxgainfeat])))
    for v in unique:
        newX=X.loc[X[maxgainfeat]==v]
        newY=Y.loc[X[maxgainfeat]==v]
        del newX[maxgainfeat]
        tree.append(str('if '+v))
        #print(tree)
        #print(newX)
        #print(newY)

        buildtree(entr,entf,newX,newY,tree)















data=pd.read_csv('decisiondata.csv')
x=data.iloc[:,1:5]
#print(type(x))
#print(data)
xnames=[]
xnames=list(data.columns.values)
xnames=xnames[:-1]
xnames=xnames[1:]
#print(xnames)
y=[]
y=data.iloc[:,-1]
fintree=[]
entout=entropyofoutput(y)



buildtree(entout,{},x,y,[])
print('The final binary tree is ')
print(fintree)

print(x.columns)

#using inbuilt classifer from sklearn
le1=LabelEncoder()
le2=LabelEncoder()
le3=LabelEncoder()
le4=LabelEncoder()

#creating DataFrame of featueres with encoded data
X=pd.DataFrame({'Age':le1.fit_transform(x.iloc[:,0]),
'Income':le2.fit_transform(x.iloc[:,1]),
'Gender':le3.fit_transform(x.iloc[:,2]),
'Marital Status':le4.fit_transform(x.iloc[:,3])})

model = DecisionTreeClassifier(criterion='entropy',random_state=0)

model.fit(X,y)
print('Prediction on data point [Age < 21, Income = Low,Gender = Female, Marital Status = Married] is ',
model.predict(pd.DataFrame({'Age':le1.transform(['<21']),
'Income':le2.transform(['Low']),
'Gender':le3.transform(['Female']),
'Marital Status':le4.transform(['Married'])}))[0])


#visualize tree
dot_data= export_graphviz(model,out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png('dt.png')
