import random
from ecdsa import SigningKey ,NIST256p
#import matplotlib.pyplot as plt



# returns nCr
def nCr(n, r):
	return fact(n) // (fact(r) * fact(n - r))

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
	hashValue = random.randint(0,(2**256-1))
	return hashValue


def VerifySort(pk, hashValue, pi, seed, tau, role, w, W):

	# if not pk.verify(hashValue, str((pi)).encode('utf-8')):
	# 	return 0
	# else:
	hashval = hashValue.hex()
	p = tau / W
	j = 0
	value = int(hashval,16) / (2 ** 512)
	while j <= w:
		leftlimit = 0
		rightlimit = 0
		for k in range(j):
			leftlimit = leftlimit + B(k, w, p)

		for k in range(j + 1):
			rightlimit = rightlimit + B(k, w, p)

		if leftlimit > value or value >= rightlimit:
			j = j + 1
		else:
			break
	return j

def Sortition(sk, seed, tauProposer, role, w, W):
	# Refer to Algorand paper
	pi = PRG(seed+role)
	VRFhash = (sk.sign((str(pi)).encode('utf-8')))

	p = tauProposer/W
	j = 0

	hashval = VRFhash.hex()
	hashIntValue = int(hashval,16)
	value = hashIntValue/(2**512)

	while j <= w:
		leftlimit = 0
		rightlimit = 0
		for k in range(j):
			leftlimit = leftlimit + B(k,w, p)

		for k in range(j+1):
			rightlimit = rightlimit + B( k,w, p)

		if leftlimit > value or value >= rightlimit:
			j = j + 1
		else:
			break
	return tuple((VRFhash,pi,j))




