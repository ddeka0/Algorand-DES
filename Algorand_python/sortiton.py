import random
# returns nCr
def nCr(n, r):
    return (fact(n) // (fact(r) * fact(n - r)))

# Returns factorial of n
def fact(n):
    res = 1

    for i in range(2, n + 1):
        res = res * i

    return res


# Returns binomial distribution
def B(k,w,p):
    return nCr(w,k)*(p**k)*((1-p)**(w-k))


#Returns PRG seed
def PRG(seed):
    # PRG seed
    random.seed(seed)
    # Get random 256 bit number
    hash = random.randint(0,(2**256-1))
    return hash


def Sortition(sk,seed,tau,role,w,W):
    pi = PRG(seed+role)
    hash =  (sk.sign((str(pi)).encode('utf-8'))).hex()
    p = tau/W
    j = 0
    hashint = int(hash,16)
    value = hashint/2**(512)

    while(j<=w):
        k=0
        leftlimit = 0
        rightlimit = 0
        for k in range(j):
            leftlimit = leftlimit+B(k,w, p)

        for k in range(j+1):
            rightlimit = rightlimit +B( k,w, p)

        # print("value ", value)
        # print("left right :" ,leftlimit,rightlimit)

        if(leftlimit>value or value>=rightlimit):
            j = j+1
        else:
            break
    return tuple((hash,pi,j))
