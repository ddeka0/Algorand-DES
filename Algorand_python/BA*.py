import hashlib

FINAL = 1
TENTATIVE = 2
REDUCTION_ONE = 3
REDUCTION_TWO = 4
T_final = 5
tau_final = 5
lambda_step  =5
tau_step = 5

def H(block):
    retval = hashlib.sha256(block.encode())
    return retval.hexdigest()


def Reduction(ctx, round, hblock):
    CommmitteeVote(ctx,round,REDUCTION_ONE,tau_step,hblock)
    return 5

def committeeVote(ctx,round,step,tau,value):



def BinaryBA_Star(ctx, round, hblock):
    return 5


def CountVotes(ctx,round,step,T,tau,Lambda):
    return 5

def BlockofHash(hblock):
    return 5


def BA_Star(ctx,round,block):
    hblock = Reduction(ctx,round,H(block))
    hblock_Star = BinaryBA_Star(ctx,round,hblock)
    r = CountVotes(ctx,round,FINAL,T_final,tau_final,lambda_step)
    if hblock_Star == r :
        return tuple((FINAL,BlockofHash(hblock_Star)))
    else:
        return tuple((TENTATIVE, BlockofHash(hblock_Star)))

ctx = "ctx"
round = "round"
block = "block"

print(BA_Star(ctx,round,block))



