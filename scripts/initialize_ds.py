from lib import constants
import os


bit_len_dict = {}
for filename in os.listdir(constants.DATA_PATH % ''): 
    if not filename.endswith('.code_length'): 
#             if not filename.endswith('.tries'):
        continue
    with open(constants.DATA_PATH % ('/%s' % filename), 'r') as rfptr:
        bit_len_dict[filename.split('.')[0]] = rfptr.read().split(',')
