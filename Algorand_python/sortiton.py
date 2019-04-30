import random
from ecdsa import SigningKey ,NIST256p
import matplotlib.pyplot as plt



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




def test_Sortition():

	final = {}
	sk_List = []
	pk_List = []
	NODES = 256
	MAX_MONEY = 50
	ROUNDS = 64
	tau_proposer = 64
	W = NODES * (MAX_MONEY/2)

	w = []
	j = [0] * NODES

	for i in range(NODES):
		w.append(random.randint(1,50))


	for i in range(NODES):  # 200
		sk_List.append(SigningKey.generate(curve=NIST256p))


	for i in range(ROUNDS):
		for k in range(NODES):  # 200
			retval = (Sortition(sk_List[k],"THIS IS BEST BLOCK ALGORAND SIMULATOR",tau_proposer,"ROLE",w[k],W))
			j[k] += retval[2]
		print("Current Round = ",i+1)

	c = 0
	# for i in w:
	# 	if i in final:
	# 		final[i] += j[c]
	# 	else:
	# 		final[i] = j[c]
	# 	c += 1
	for i in range(len(j)):
		j[i] = j[i]/ROUNDS

	print(j)
	print(w)

	for i in w:
		if i in final:
			final[i] += j[c]
			#final[i].append(j[c])
		else:
			final[i] = j[c]
			#final[i] = []
			#final[i].append(j[c])
		c += 1

	temp={}
	for k,v in final.items():
		final[k] = v/ROUNDS
		#temp[k]= sum(final[k])/len(final[k])

	print(sum(temp.values()))

	plt.xlabel('stakes')
	# frequency label
	plt.ylabel('avg sub-user')
	# plot title
	plt.title('My bar plot!')
	# showing legend
	plt.legend()

	print(final)
	plt.bar(final.keys(), final.values(), label="line 1",)
	plt.show()



# test_Sortition()




