# !/bin/python3
import pickle
import ecdsa
import numpy as np
from network_utils import * 



listsk = []
listpk = []
MAX_NODES = 256

def tmep():
	for i in range(MAX_NODES):
		listsk.append(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1))
		print("sk = ", i)

	for i in range(MAX_NODES):
		listpk.append(listsk[i].get_verifying_key())
		print("pk = ", i)

	total_list = []
	total_list.append(listsk)
	total_list.append(listpk)



	with open('keysFile-256', 'wb') as f:
		pickle.dump(total_list, f)


	with open('keysFile-256', 'rb') as f:
		read_list = pickle.load(f)


def init_Delays():
	delays=[]
	blockDelays=[]
	MAX_NODES=256
	for i in range(MAX_NODES):
		lz = [0] * MAX_NODES
		delays.append(lz)

	for i in range(MAX_NODES):
		for j in range(MAX_NODES):
			if i == j:
				delays[i][j] = 0
			else:
				#normal_delay = np.random.normal(200,400,1)
				normal_delay = np.random.normal(40,64,1)
				normal_delay = list(normal_delay)[0]
				delays[i][j] = max(MIN_DELAY,normal_delay)/DIVIDE_BY  # TODO: change value here
	#print(delays)

	for i in range(MAX_NODES):
		lz = [0] * MAX_NODES
		blockDelays.append(lz)
	
	for i in range(MAX_NODES):
		for j in range(MAX_NODES):
			if i == j:
				blockDelays[i][j] = 0
			else:
				#normal_delay = np.random.normal(200,400,1)
				normal_delay = np.random.normal(40,64,1)
				normal_delay = list(normal_delay)[0]
				blockDelays[i][j] = max(MIN_DELAY,normal_delay)/DIVIDE_BY  # TODO: change value here
	#print(blockDelays)

	motal_list = []
	motal_list.append(delays)
	motal_list.append(blockDelays)
	

	with open('delays-256', 'wb') as f:
		pickle.dump(motal_list, f)

init_Delays()
