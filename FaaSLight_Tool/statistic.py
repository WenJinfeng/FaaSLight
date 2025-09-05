import os
import json
import astroid
from astroid import parse
import argparse
import sys
sys.setrecursionlimit(5000000)

count = []

def pre_function_transform(node: astroid.FunctionDef):
    count.append("1")
    node.doc="""clear"""
    
    return node



if __name__ == "__main__": 

    
    astroid.MANAGER.register_transform(
        astroid.nodes.FunctionDef,
        pre_function_transform,
    )


    path = "/home/wenjinfeng/TestApp/Keras_tensorflow/origin copy"
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                print(handle_file)
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()
                f.close()
                tree = parse(content)
                w = open(handle_file, 'w',encoding='utf-8')
                w.write(tree.as_string())
                w.close()
   
    print("Number of functions is{}".format(len(count)))
    import metricCal
    metricCal.main(path)
