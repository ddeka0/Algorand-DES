# !/bin/python3
import pickle
import ecdsa
import numpy as np
from network_utils import * 



listsk = []
listpk = []
MAX_NODES = 256

def generate_pk_sk():
	for i in range(MAX_NODES):
		listsk.append(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1))
		print("sk = ", i)

	for i in range(MAX_NODES):
		listpk.append(listsk[i].get_verifying_key())
		print("pk = ", i)

	total_list = []
	total_list.append(listsk)
	total_list.append(listpk)



	with open('keysFile-'+str(MAX_NODES), 'wb') as f:
		pickle.dump(total_list, f)


	with open('keysFile-'+str(MAX_NODES), 'rb') as f:
		read_list = pickle.load(f)


def generate_delayMatrices():
	delays=[]
	blockDelays=[]
	#MAX_NODES=256
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
	

	with open('delays-'+str(MAX_NODES), 'wb') as f:
		pickle.dump(motal_list, f)

def generate_peer_list():
	peer_list={}
	for i in range(MAX_NODES):
		peers_len = np.random.randint(2, 4)
		peer_list[i] = np.random.randint(0, MAX_NODES-1,(peers_len))
		while i in peer_list[i]:
			peer_list[i] = np.random.randint(0, MAX_NODES-1,(peers_len))
			print("some conflict")
	#print(peer_list)
	with open('peer-list-'+str(MAX_NODES), 'wb') as f:
		pickle.dump(peer_list, f)


generate_peer_list()
with open('peer-list-'+  str(MAX_NODES), 'rb') as f:
		apl = pickle.load(f)
		print(apl)

