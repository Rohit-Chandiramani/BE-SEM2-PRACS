import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def gethofx(W1,W2,X):
    return(W1+W2*X)

def getcost(wz,wo):
    cost=0
    for i in range(0,8):
        sq=0
        sq=risk[i]-gethofx(wz,wo,nohours[i])
        sq=sq*sq
        cost=cost+sq
    cost=cost/(2*8)
    return cost

def getdelJ(wz,wo,dimension):
    delJ=0
    for i in range(0,8):
        val=0
        if dimension==0:
            val+=risk[i]-gethofx(wz,wo,nohours[i])
        else:
            val+=(risk[i]-gethofx(wz,wo,nohours[i]))*nohours[i]
        delJ=delJ-val
    delJ=delJ/8
    #print(abs(delJ))
    return delJ




nohours=[10,9,2,15,10,16,11,16]
risk=[95,80,10,50,45,98,38,93]


#by linear regression with gradient descent
w0=1
w1=0.1
alpha=0.001
costold=getcost(w0,w1)
costnew=getcost(w0,w1)
cnt=0
while True:
    w0=w0-alpha*getdelJ(w0,w1,0)
    w1=w1-alpha*getdelJ(w0,w1,1)
    #print(w0)
    #print(w1)
    print('cost============>',costold)
    costnew=getcost(w0,w1)
    if(abs(costnew-costold)<np.finfo(float).eps):
        break
    else:
        costold=costnew

ynew=[]
for i in range(0,8):
    ynew.append(gethofx(w0,w1,nohours[i]))
plt.scatter(nohours,risk)
plt.plot(nohours,ynew)
plt.ylabel('Risk score (y)')
plt.xlabel('Number of hours driving (x)')
plt.show()

#print(w0)
#print(w1)
print('By linear regression with Gradient Descent, the equation of best fit is \ny=',w0,'+',w1,'x')




#formula based Linear regression
meannohours=sum(nohours)/8
meanrisk=sum(risk)/8
ans=0
den=0
sst=0
for i in range(0,8):
    ans=ans+((nohours[i]-meannohours)*(risk[i]-meanrisk))
    sst=sst+pow((risk[i]-meanrisk),2)
    den=den+pow((nohours[i]-meannohours),2)
w1=ans/den
w0=meanrisk-w1*meannohours


#print(w0)
#print(w1)
print('By linear regression with formula, the equation of best fit is \ny=',w0,'+',w1,'x')



#calculating R2 statistic for testing goodness of fit
sse=0
for i in range(0,8):
    sse=sse+pow((risk[i]-gethofx(w0,w1,nohours[i])),2)

rsquared=(1-(sse/sst))
print('R squared statistic value is ',rsquared)



#uisng inbuilt classifier from sklearn
nohours=np.array(nohours).reshape(np.array(nohours).shape[0],1)
model=LinearRegression()
model.fit(nohours,risk)
print('The R squared statistic value using inbuilt classifier is ',model.score(nohours,risk))
