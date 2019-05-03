import random
from ecdsa import SigningKey ,NIST256p
import matplotlib.pyplot as plt
from network_utils import *

def test_Sortition_one():
	sk_List = []
	pk_List = []
	init_AsymmtericKeys(sk_List,pk_List)

	tau_proposer = 64

	W = MAX_NODES * (MAX_ALGORAND / 2)

	w = []
	j = [0] * MAX_NODES

	for i in range(MAX_NODES):
		w.append(random.randint(1,50))

	for i in range(ROUNDS):
		for k in range(MAX_NODES):
			retval = (Sortition(sk_List[k],"THIS IS BEST BLOCK ALGORAND SIMULATOR" + str(k) + str(i),tau_proposer,"ROLE",w[k],W))
			j[k] += retval[2]
		print("Current Round = ",i+1)

	for i in range(MAX_NODES):
		j[i] = j[i] / ROUNDS

	final = {}
	idx = 0
	for wght in w:
		if wght in final:
			final[wght] += j[idx]
		else:
			final[wght] = j[idx]
		idx += 1

	plt.xlabel('stakes')
	plt.ylabel('avg. sub-user')
	plt.title('Variation of mean of sub-users across round w.r.t stake')
	plt.legend()

	plt.bar(final.keys(), final.values(), label="line 1",)
	plt.savefig("2.1.1-64.svg")
	plt.show()

def test_Sortition_two():
	sk_List = []
	pk_List = []
	init_AsymmtericKeys(sk_List,pk_List)

	tau_proposer = 32

	W = MAX_NODES * (MAX_ALGORAND / 2)

	w = []
	j = [0] * MAX_NODES

	for i in range(MAX_NODES):
		w.append(random.randint(1,50))

	fractions = []
	
	final = {}
	idx = 0
	for wght in w:
		if wght in final:
			final[wght] += j[idx]
		else:
			final[wght] = j[idx]
		idx += 1
		
	for r in range(ROUNDS):
		for s in range(5):  #STEPS = 5 
			
			totalWinner = 0
			for k in range(MAX_NODES):
				retval = (Sortition(sk_List[k],"THIS IS BEST BLOCK ALGORAND SIMULATOR" + str(k) + str(i),tau_proposer,"ROLE",w[k],W))
				j[k] += retval[2]
				
				totalWinner += retval[2]
			
			for i in range(MAX_NODES):
				j[i] = j[i] / ROUNDS
			
			final = {}
			idx = 0
			for wght in w:
				if wght in final:
					final[wght] += j[idx]
				else:
					final[wght] = j[idx]
				idx += 1
			x = []
			for wght,summ in final.items():
				x.append(summ/totalWinner)
			fractions.append(x)

			print("Current Step = ",s+1)			
		print("Current Round = ",r+1)

	final = []
	for lst in fractions:


	plt.xlabel('stakes')
	plt.ylabel('avg. sub-user')
	plt.title('Variation of mean of sub-users across round w.r.t stake')
	plt.legend()

	plt.bar(final.keys(), final.values(), label="line 1",)
	plt.savefig("2.1.1.svg")
	plt.show()


test_Sortition_one()