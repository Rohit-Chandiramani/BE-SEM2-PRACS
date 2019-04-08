import numpy as np







def getmixcolval(tup):
    if(tup[0]==0 or tup[1]==0): #
        return 0                #
    elif(tup[0]==1):            #=========>handling base boundary conditions
        return tup[1]           #          as the refernce mix columns table
    elif(tup[1]==1):            #           did not handle them
        return tup[0]           #
    else:
        return(mixcolmap[tup])


def mixcolumns(c):
    mat=[int(c[0:4],2), int(c[4:8],2), int(c[8:12],2), int(c[12:16],2)] #column major
    pre=[1,4,4,1]
    val=[]
    val.append(getmixcolval((pre[0],mat[0]))^getmixcolval((pre[1],mat[1])))
    val.append(getmixcolval((pre[2],mat[0]))^getmixcolval((pre[3],mat[1])))

    val.append(getmixcolval((pre[0],mat[2]))^getmixcolval((pre[1],mat[3])))
    val.append(getmixcolval((pre[2],mat[2]))^getmixcolval((pre[3],mat[3])))

    fin=''
    for v in val:
        fin=fin+padbits(bin(v)[2:],4)
    return fin




def createmixcolumn():
    mixcol=[2,4,6,8,10,12,14,3,1,7,5,11,9,15,13,4,8,12,3,7,11,15,6,2,14,10,5,1,13,9,9,1,8,2,11,3,10,4,13,5,12,6,15,7,14]  #static valyes from internet
    global mixcolmap

    v=2
    r=0
    for cnt in range(0,3):
        for j in range(1,16):
            mixcolmap[(v,j)]=mixcol[r]
            mixcolmap[(j,v)]=mixcol[r]
            r=r+1
        if v==2:
            v=4
        elif v==4:
            v=9

    for i in range (0,len(list(mixcolmap.keys()))):
        print(str(list(mixcolmap.keys())[i])+'    '+str(list(mixcolmap.values())[i]))




def shiftrows(c):
    return c[0:4]+c[12:]+c[8:12]+c[4:8]

def encrypt(pt,keys):
    #plaintext ^ roundkey1

    ct=padbits(bin(int(pt,2)^int(keys[0],2))[2:],16)
    ct=subnib(ct[0:8])+subnib(ct[8:])
    ct=shiftrows(ct)
    ct=mixcolumns(ct)
    ct=padbits(bin(int(ct,2)^int(keys[1],2))[2:],16)
    ct=subnib(ct[0:8])+subnib(ct[8:])
    ct=shiftrows(ct)
    ct=padbits(bin(int(ct,2)^int(keys[2],2))[2:],16)
    return ct

def padbits(s,n):
    #s is binary string, n is n. of maximum bits in output string

    fin='0'*n
    if(len(s)<len(fin)):
        return(fin[0:(len(fin)-len(s))]+s)
    else:
        return(s)


def subnib(w):
    sbox=[[9,4,10,11],[13,1,8,5],[6,2,0,3],[12,14,15,7]]

    first=w[0:4]
    second=w[4:]

    first=padbits(bin(sbox[int(first[0:2],2)][int(first[2:],2)])[2:],4)   #padding as output nibble in binary might not contain leading zeros
    second=padbits(bin(sbox[int(second[0:2],2)][int(second[2:],2)])[2:],4)

    return (first+second)



def rotnib(w):
    return(str(w[4:]+w[0:4]))


def generatekeys(k):
    rcon1='10000000'   #rcon1 and 2 re round constants
    rcon2='00110000'
    w0=k[0:8]
    w1=k[8:]
    Keys=[]

    print(w0)
    print(w1)
    w2=padbits(bin(int(w0,2)^int(rcon1,2)^int(subnib(rotnib(w1)),2))[2:],8)        #padding as output nibble in binary might not contain leading zeros
    print(w2)

    w3=padbits(bin(int(w2,2)^int(w1,2))[2:],8)
    print(w3)

    w4=padbits(bin(int(w2,2)^int(rcon2,2)^int(subnib(rotnib(w3)),2))[2:],8)
    print(w4)

    w5=padbits(bin(int(w4,2)^int(w3,2))[2:],8)
    print(w5)


    Keys.append(w0+w1)
    Keys.append(w2+w3)
    Keys.append(w4+w5)

    return Keys

#plain=str(input("Input the 16 bit plain text "))
#key=str(input("Input the 16 bit key "))

plain='1110011100101000'  #e728
key='0100101011110101'   #random
mixcolmap={}
roundkeys=[]
roundkeys=generatekeys(key)

print(roundkeys)
createmixcolumn()

ciphertext=encrypt(plain,roundkeys)
print('Cipher text is ',ciphertext)

#print(hex(int(ciphertext[0:4],2))[2:]+hex(int(ciphertext[4:8],2))[2:]+hex(int(ciphertext[8:12],2))[2:]+hex(int(ciphertext[12:],2))[2:])  presenting binary 16 bit as 4 digit hex
