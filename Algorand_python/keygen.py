# !/bin/python3
import pickle
import ecdsa

listsk = []
listpk = []
MAX_NODES = 256

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
