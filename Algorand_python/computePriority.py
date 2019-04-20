import hashlib


class resp:
    def __init__(self,hash,j):
        self.hash = hash
        self.j = j


def computePriority(resp):
    hashList = []
    for i in range(resp.j):
        input = str(resp.hash)+str(i)
        sha = hashlib.sha256(input.encode())
        hashList.append(sha.hexdigest())
    return hashList.index(min(hashList))+1




hash = hashlib.sha256("helo".encode())

r = resp(hash.hexdigest(),5)

computePriority(r)