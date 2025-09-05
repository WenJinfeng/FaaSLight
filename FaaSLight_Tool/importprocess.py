import os
import astroid
from astroid import parse
import argparse

handle_file = ""

# Convert source code to AST format
def code2node(code):
    try:
        return astroid.extract_node(code)
    except ValueError:
        # here is a bug of astroid
        tree = astroid.parse(code, apply_transforms=True)
        return astroid.nodes.Const(tree.doc)

        
def function_transform(node: astroid.FunctionDef):
    body = []

    newnode = node
    # if node.doc:
    #     node.doc = node.doc.replace("\"\"\"", "\"")
    #     # node.doc = r''+node.doc
    # # Contains \u character
    # if node.name == "to_latex":
    #     node.doc = """clear"""
    # node.doc = """clear"""
    parent_func = []
    # print(newnode.parent)
    while newnode.parent:
        if newnode.parent.__class__ == astroid.FunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    # print(parent_func)
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

    # node.body.extend(body)
    return node

def asyfunction_transform(node: astroid.AsyncFunctionDef):
    body = []

    newnode = node
    # node.doc = """clear\nclear\nclear\nclear"""
    # if node.doc:
    #     node.doc = node.doc.replace("\"\"\"", "\"")
    #     # node.doc = r''+node.doc
    # if node.name == "to_latex":
    #     node.doc = """clear"""
    parent_func = []
    # print(newnode.parent)
    while newnode.parent:
        if newnode.parent.__class__ == astroid.AsyncFunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    # print(parent_func)
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

    # node.body.extend(body)
    return node

            



if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default=""
    )

    args = parser.parse_args()
    path = args.path

    astroid.MANAGER.register_transform(
        astroid.nodes.FunctionDef,
        function_transform,
    )

    astroid.MANAGER.register_transform(
        astroid.nodes.AsyncFunctionDef,
        asyfunction_transform,
    )
   
    # path = "/home/wenjinfeng/test_application/test-requests/application-init-test"
    # path = "/home/wenjinfeng/test_application/test-numpy/test-init-numpy-origin"
    
    # overwrite_file(path)
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                print(os.path.join(root, name))
                handle_file = ""+os.path.join(root, name)
                # print(handler_file)
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()
                tree = parse(content,apply_transforms=True)              
                w = open(handle_file, 'w')
                w.write(tree.as_string())
                w.close


