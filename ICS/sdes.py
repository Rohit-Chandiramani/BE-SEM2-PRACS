#pt=str(input('Input the 8 bit plain text '))
#key=str(input('Input the 10 bit key '))

def p10(k):
    #P10 Permutation to the original key
    #order:- 3 5 2 7 4 10 1 9 8 6

    orderofbits=[3,5,2,7,4,10,1,9,8,6]
    new=''
    for index in orderofbits:
        new+=k[index-1]  #index-1 as inbuilt index from 0
    return new


def p8(k):
    #p3=8 select and permutate
    #order:- 6 3 7 4 8 5 10 9
    new=''
    orderofbits=[6,3,7,4,8,5,10,9]

    for index in orderofbits:
        new+=k[index-1]
    return new


def p4(k):
    #P4 Permutation
    #order:- 2 4 3 1

    orderofbits=[2,4,3,1]
    new=''
    for index in orderofbits:
        new+=k[index-1]  #index-1 as inbuilt index from 0
    return new


def leftshift(k,num):
    return(k[num:]+k[0:num])


def generate_round_keys(k):
    
    global k1
    k1=p8(leftshift(p10(k)[0:5],1)+leftshift(p10(k)[5:],1))
    #print(k1)

    global k2
    k2=p8(leftshift(leftshift(p10(key)[0:5],1),2)+leftshift(leftshift(p10(key)[5:],1),2))
    #print(k2)

    print('The round keys generated are ',k1,'\t',k2)

    global keys
    keys.append(k1)
    keys.append(k2)


def initial_permutation(p):
    #IP:- initial permutation
    #order:- 2 6 3 1 4 8 5 7
    new=''
    orderofbits=[2,6,3,1,4,8,5,7]

    for index in orderofbits:
        new+=p[index-1]
    return new

def inverse_initial_permutation(p):
    #IP-1:- initial permutation
    #order:- 4 1 3 5 7 2 8 6
    new=''
    orderofbits=[4,1,3,5,7,2,8,6]

    for index in orderofbits:
        new+=p[index-1]
    return new


def expand_and_permutate(p):
    #EP:- expand permutation
    #order:- 4 1 2 3 2 3 4 1

    new=''
    orderofbits=[4,1,2,3,2,3,4,1]

    for index in orderofbits:
        new+=p[index-1]
    #print(new)
    return new


def S0_substitution(s):
    row=int(s[0]+s[3],2)
    column=int(s[1]+s[2],2)

    S0=[['01','00','11','10'],['11','10','01','00'],['00','10','01','11'],['11','01','11','10']]

    return S0[row][column]

def S1_substitution(s):
    row=int(s[0]+s[3],2)
    column=int(s[1]+s[2],2)

    S1=[['00','01','10','11'],['10','00','01','11'],['11','00','01','00'],['10','01','00','11']]

    return S1[row][column]

def round_func(p,roundno,ch):


    
    left4bits=p[0:4]
    right4bits=p[4:]
    afterexor=int(expand_and_permutate(right4bits),2)^int(keys[roundno],2)
    afterexor=str(bin(afterexor)[2:])
    zeros='00000000'
    if len(afterexor)<8:
        afterexor=zeros[0:(8-len(afterexor))]+afterexor

    aftersbox=S0_substitution(afterexor[0:4])+S1_substitution(afterexor[4:])
    afterexorwithleft4bits=str(bin(int(p4(aftersbox),2)^int(left4bits,2))[2:])
    
    if len(afterexorwithleft4bits)<4:
        afterexorwithleft4bits=zeros[0:(4-len(afterexorwithleft4bits))]+afterexorwithleft4bits
    #print(afterexorwithleft4bits)

    if (roundno==0 and ch=='e') or (roundno==1 and ch=='d'):
        afterswap=right4bits+afterexorwithleft4bits
        return afterswap
    else:
        return(afterexorwithleft4bits+right4bits)
    

'''
pt='01110010'
key='1010000010'
'''

pt=str(input('Input 8 bit plain text '))
key=str(input('Input 10 bit key '))
k1=''
k2=''
keys=[]
generate_round_keys(key)
cipher=inverse_initial_permutation(round_func(round_func(initial_permutation(pt),0,'e'),1,'e'))
print('The encrypted cipher text is ',cipher)

plain=inverse_initial_permutation(round_func(round_func(initial_permutation(cipher),1,'d'),0,'d'))
print('The decrypted plain text is ',plain)
