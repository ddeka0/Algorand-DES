import random
import ecdsa
import binomial
import PRG


M = 10
N = 2000

def Sortition(sk,seed,tau,role,w,W):
    randomNo = PRG.prg(seed+role)
    hash =  (sk.sign((str(randomNo)).encode('utf-8'))).hex()
    p = tau/W
    j = 0
    hashint = int(hash,16)
    value = hashint/2**(512)

    while(j<=w):
        k=0
        leftlimit = 0
        rightlimit = 0
        for k in range(j):
            leftlimit = leftlimit+binomial.B(k,w, p)

        for k in range(j+1):
            rightlimit = rightlimit + binomial.B( k,w, p)

        print("value ", value)
        print("left right :" ,leftlimit,rightlimit)

        if(leftlimit>value or value>=rightlimit):
            j = j+1
        else:
            break
    return j
    #return tuple((hash,randomNo,j))




# SECP256k1 is the Bitcoin elliptic curve
listsk = []
listvk = []

for i in range(N):
    listsk.append(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1))
    print("sk = ",i)

for i in range(N):
    listvk.append(listsk[i].get_verifying_key())
    print("vk = ", i)

seed = "HASHOFPREVIOUSBLOCK"
tau = 20
W  = 50000
listw = []

for i in range(N):
    listw.append(random.randint(1,50))

s = 0
for t in range(M):
    k = 0
    for i in range(N):
        k = k + Sortition(listsk[i],seed,tau,"sdsds",listw[i],W)
        print("k = ",k)

    s = s + k

s = s / M

print(s)
