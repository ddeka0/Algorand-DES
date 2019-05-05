# !/bin/python3
import pickle
import ecdsa
import numpy as np

def generate_keys(nkeys):
	listsk = []
	listpk = []
	for i in range(nkeys):
		listsk.append(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1))
		print("secret key generate for node = ", i)
	for i in range(nkeys):
		listpk.append(listsk[i].get_verifying_key())
		print("public key generated for node = ", i)
	total_list = []
	total_list.append(listsk)
	total_list.append(listpk)
	with open("keysFile-" + str(nkeys), 'wb') as f:
		pickle.dump(total_list, f)
	#pickle.close()
	print("keysFile-" + str(nkeys)," is stored")

def generate_delays(nnodes,md,vd,mD,vD,mind):
	delays = []
	blockDelays = []
	for i in range(nnodes):
		lz = [0] * nnodes
		delays.append(lz)
	for i in range(nnodes):
		for j in range(nnodes):
			if i == j:
				delays[i][j] = 0
			else:
				normal_delay = np.random.normal(md,\
					vd,1)
				normal_delay = list(normal_delay)[0]
				delays[i][j] = max(mind,normal_delay)/1000
	for i in range(nnodes):
		lz = [0] * nnodes
		blockDelays.append(lz)
	for i in range(nnodes):
		for j in range(nnodes):
			if i == j:
				blockDelays[i][j] = 0
			else:
				normal_delay = np.random.normal(mD,\
					vD,1)
				normal_delay = list(normal_delay)[0]
				blockDelays[i][j] = max(mind,normal_delay)/1000
	total_list = []
	total_list.append(delays)
	total_list.append(blockDelays)
	with open("delays-" + str(nnodes), 'wb') as f:
		pickle.dump(total_list, f)
	print("delays-" + str(nnodes)," is stored")
