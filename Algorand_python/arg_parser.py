import argparse
from network_utils import *
import config
from logging_config import * 

parser = argparse.ArgumentParser()
parser.add_argument('-n', action='store', dest='max_nodes',
					default=config.MAX_NODES,
					help='set MAX_NODES',type=int)

parser.add_argument('-fan', action='store', dest='fan_out',
					default=config.GOSSIP_FAN_OUT,
					help='set GOSSIP_FAN_OUT',type=int)

# parser.add_argument('-r', action='store', dest='round',
# 					default=1000,
# 					help='set ROUND, currently not used')

parser.add_argument('-md', action='store', dest='non_block_delay_mean',
					default=config.NON_BLOCK_MSG_DELAY_MEAN,
					help='set NON_BLOCK_MSG_DELAY_MEAN',type=float)

parser.add_argument('-vd', action='store', dest='non_block_delay_sigma',
					default=config.NON_BLOCK_MSG_DELAY_SIGMA,
					help='set NON_BLOCK_MSG_DELAY_SIGMA',type=float)

parser.add_argument('-mD', action='store', dest='block_delay_mean',
					default=config.BLOCK_MSG_DELAY_MEAN,
					help='set BLOCK_MSG_DELAY_MEAN',type=float)

parser.add_argument('-vD', action='store', dest='block_delay_sigma',
					default=config.BLOCK_MSG_DELAY_SIGMA,
					help='set BLOCK_MSG_DELAY_SIGMA',type=float)


parser.add_argument('-tstep', action='store', dest='tou_step',
					default=config.tou_step,
					help='set tou_step',type=float)

parser.add_argument('-tprop', action='store', dest='tou_prop',
					default=config.tou_prop,
					help='set tou_prop',type=float)

parser.add_argument('-tfinal', action='store', dest='tou_final',
					default=config.tou_final,
					help='set tou_final',type=float)

parser.add_argument('-st', action='store', dest='max_algorand',
					default=config.MAX_ALGORAND,
					help='set MAX_ALGORAND',type=float)

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

def getUserArguments():
	result =  parser.parse_args()
	if result.max_nodes < result.fan_out:
		print(BOLDRED("Input Error"),RESET(""),"max nodes must be greater than the fan out")
		print("Try : python main.py -h")
		sys.exit()
	return result





					
# parser.add_argument('-c', action='store_const', dest='constant_value',
#                     const='value-to-store',
#                     help='Store a constant value')

# parser.add_argument('-t', action='store_true', default=False,
#                     dest='boolean_switch',
#                     help='Set a switch to true')
# parser.add_argument('-f', action='store_false', default=False,
#                     dest='boolean_switch',
#                     help='Set a switch to false')

# parser.add_argument('-a', action='append', dest='collection',
#                     default=[],
#                     help='Add repeated values to a list',
#                     )

# parser.add_argument('-A', action='append_const', dest='const_collection',
#                     const='value-1-to-append',
#                     default=[],
#                     help='Add different values to list')
# parser.add_argument('-B', action='append_const', dest='const_collection',
#                     const='value-2-to-append',
#                     help='Add different values to list')