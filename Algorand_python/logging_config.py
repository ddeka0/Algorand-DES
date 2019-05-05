# !/bin/python3

BLACK = lambda x: '\033[30m' + str(x)
RED = lambda x: '\033[31m' + str(x)
GREEN = lambda x: '\033[32m' + str(x)
YELLOW = lambda x: '\033[33m' + str(x)
BLUE = lambda x: '\033[34m' + str(x)
MAGENTA = lambda x: '\033[35m' + str(x)
CYAN = lambda x: '\033[36m' + str(x)
WHITE = lambda x: '\033[37m' + str(x)
UNDERLINE = lambda x: '\033[4m' + str(x)
RESET = lambda x: '\033[0m' + str(x)


BOLDBLACK = lambda x: '\033[1m\033[30m' + str(x)
BOLDRED = lambda x: '\033[1m\033[31m' + str(x)
BOLDGREEN = lambda x: '\033[1m\033[32m' + str(x)
BOLDYELLOW = lambda x: '\033[1m\033[33m' + str(x)
BOLDBLUE = lambda x: '\033[1m\033[34m' + str(x)
BOLDMAGENTA = lambda x: '\033[1m\033[35m' + str(x)
BOLDCYAN = lambda x: '\033[1m\033[36m' + str(x)
BOLDWHITE = lambda x: '\033[1m\033[37m' + str(x)
