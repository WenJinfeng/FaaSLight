import os
import json

def rewrite_template(unused_file_name, funname, local_list, returnnum):
    """clear"""
    
    return_string = ''
    if returnnum > 0:
        for i in range(returnnum):
            return_string = return_string + 'return{},'.format(i)
        return_string = return_string[:-1] + '='

    LOC = ''
    if 'on_demand_loading' not in globals().keys():
        import gzip
        with gzip.open('gzipinfo.txt', 'r') as fin:
            globals()['on_demand_loading'] = json.loads(fin.read().decode('utf-8'))
        
    
    LOC = globals()['on_demand_loading'][unused_file_name]
    
    LOC = '{}\n'.format(LOC) + return_string + '{}'.format(funname)
    exec(LOC, local_list, globals())
    
    
    if returnnum == 1:
            return globals()['return0']
    return tuple( [globals()['return{}'.format(i)] for i in range( returnnum ) ])
