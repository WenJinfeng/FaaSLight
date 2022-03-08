import os
import astroid
from astroid import parse
import argparse

handle_file = ""

def code2node(code):
    """
    Convert the source code to ast format

    """
    try:
        return astroid.extract_node(code)
    except ValueError:
        """ here is a bug of astroid """
        tree = astroid.parse(code, apply_transforms=True)
        return astroid.nodes.Const(tree.doc)

        
def function_transform(node: astroid.FunctionDef):
    body = []
    newnode = node
    parent_func = []

    while newnode.parent:
        if newnode.parent.__class__ == astroid.FunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    parent_func= [i for i in parent_func if(len(str(i))!=0)]
    parent_func.reverse()

    if parent_func:
        body.append(code2node("print('{}={}={}={}')".format(handle_file, "=".join(parent_func), node.name, node.lineno)))
    else:
        body.append(code2node("print('{}={}={}')".format(handle_file, node.name, node.lineno)))
    
    tempbody  = node.body

    node.body = []
    node.body.extend(body)
    node.body.extend(tempbody)

    return node

def asyfunction_transform(node: astroid.AsyncFunctionDef):
    body = []
    newnode = node
    parent_func = []

    while newnode.parent:
        if newnode.parent.__class__ == astroid.AsyncFunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    parent_func= [i for i in parent_func if(len(str(i))!=0)]
    parent_func.reverse()

    if parent_func:
        body.append(code2node("print('{}={}={}={}')".format(handle_file, "=".join(parent_func), node.name, node.lineno)))
    else:
        body.append(code2node("print('{}={}={}')".format(handle_file, node.name, node.lineno)))
    
    

    tempbody  = node.body

    node.body = []
    node.body.extend(body)
    node.body.extend(tempbody)

    return node

            



if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default=""
    )

    args = parser.parse_args()
    path = args.path

    astroid.MANAGER.register_transform( astroid.nodes.FunctionDef, function_transform)
    astroid.MANAGER.register_transform( astroid.nodes.AsyncFunctionDef, asyfunction_transform)

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()
                tree = parse(content,apply_transforms=True)              
                w = open(handle_file, 'w')
                w.write(tree.as_string())
                w.close()


