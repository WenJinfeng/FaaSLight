import os
import astroid
from astroid import parse
import argparse

"""
The file function:
Traverse all the content under the application, keep 
the content of the specific function name
"""

sta_file=""
moshu_save = []
slsfunction =[]

def function_transform(node: astroid.FunctionDef):
    body = []
    newnode = node
    parent_func = [ node.name ]

    while newnode.parent:
        if newnode.parent.__class__ == astroid.FunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    road=handle_file.split("/")
    str_name=road.pop().split(".")
    parent_func.append(str_name[0])

    """get the path of the file"""
    while len(road)>0:
        x=road.pop()
        if x==sta_file:
            break
        parent_func.append(x)

    parent_func= [i for i in parent_func if(len(str(i))!=0)]
    parent_func.reverse()
    moshu_func = ["__getitem__", "__setitem__", "__delitem__","__len__", "__iter__"]

    if node.name in moshu_func:
        if not ".".join(parent_func) in moshu_save:
            moshu_save.append(".".join(parent_func))

    if (node.args.args) and (len(node.args.args) == 2):
        if (node.args.args[0].__class__ == astroid.AssignName) and (node.args.args[1].__class__ == astroid.AssignName):
            if (node.args.args[0].name == 'event') and (node.args.args[1].name == 'context'):
                slsfunction.append(".".join(parent_func))
    
    return node

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument( "--dirname", default="" )
    parser.add_argument( "--path", default="" )
    parser.add_argument( "--moshuoutput", default="" )
    
    args = parser.parse_args()
    path = args.path
    sta_file = args.dirname
    moshu_file = args.moshuoutput

      
    astroid.MANAGER.register_transform( astroid.nodes.FunctionDef, function_transform )

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()   
                tree = parse(content)

    moshu_output = open(moshu_file, 'w', encoding='utf-8')

    for i in moshu_save:
        moshu_output.write(i)
        moshu_output.write("\n")
    moshu_output.close()
    
   
    slsfunction_output = open("entry_point.txt", 'w', encoding='utf-8')
    for i in slsfunction:
        slsfunction_output.write(i)
        slsfunction_output.write("\n")
    slsfunction_output.close()
