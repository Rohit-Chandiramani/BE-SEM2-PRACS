def gcd(p,q):
    if(p==0):
        return q
    return(gcd(q%p,p))






plain=int(input('Enter the plain text '),2)
print(plain)

a=int(input('First prime number '))
b=int(input('Second prime number '))


n=a*b
fiofn=(a-1)*(b-1)

print('Finding e such that e and fi(n)=',fiofn,' are relatively prime')

e=2
while(1):
    if(gcd(e,fiofn)==1):
        break
    e=e+1

print('Encryption key is ',e)

cypher=(pow(plain,e))%n
print('Encrypted message is ',cypher)

print('Finding decryption key...........')

i=1

while(1):
    if(((fiofn*i+1)/e).is_integer()):
        print('Decryption key is ',((fiofn*i+1)/e))
        break
    i=i+1

    

    



