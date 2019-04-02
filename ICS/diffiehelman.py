from random import *

print('Input two mutually accepted large prime numbers by both the entities')
p=int(input('Enter first prime number'))
q=int(input('Enter second large prime number'))

print('Choosing first party random number')
a=randint(1,50)
print('Random number is ',a)

r=pow(q,a)%p

print('Sending message ',r,' to second party')

b=randint(1,100)
print('Random number is ',b)

s=pow(q,b)%p

print('Sending message ',s,' to first party')

keyone=pow(s,a)%p

print('First party secret key is ',keyone)

keytwo=pow(r,b)%p

print('Second party secret key is ',keytwo)




'''
p, q mutually decided prime number

First decides a ranodm number

r=q^amodp
sends r

Second decides b random number

s=q^bmodp

Secret key of first= S^amodp
Secret key of seond= R^bmod p







'''
