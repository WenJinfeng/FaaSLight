import os
import json
import astroid
from astroid import parse
import argparse


flag = {}
pickle_dict = {}
sta_file = ""
unused_dir = ""
handle_file = ""
T = 0

var_save = []           # all variables
import_save = []        # import variables
classdef_save = []      # class name
decorator_info = []     # decorator variables
func_para_save = []     # function parameter
returnnum_save = []     # return value
builtin_global = []     # builtin function set
assignname_save = []    # variable defined variable
functiondef_save = []   # nested function names


def code2node(code):
    """
    Convert the source code to ast format

    """
    try:
        return astroid.extract_node(code)
    except ValueError:
        """ here is a bug of astroid """
        tree = astroid.parse(code)
        return astroid.nodes.Const(tree.doc)


def pre_function_transform(node: astroid.FunctionDef):
    """
    Preprocessing
    Set the value of all function concatenation paths to 0

    """
    if (T==1): return node
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
    flag[".".join(parent_func)]=0
    
    return node

def pre_class_transform(node: astroid.ClassDef):
    """
    Preprocessing
    Set the value of all class concatenation paths to 0

    """
    if (T==1): return node
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
    flag[".".join(parent_func)]=0
    
    return node


def function_transform(node: astroid.FunctionDef):
    """
    Determine if this function is overridden

    """
    body = []
    newnode = node
    
    parent_flag = 0
    parent_func = [ node.name ]
    parent_type = ["only_function"]

    while newnode.parent:

        if newnode.parent.__class__ == astroid.FunctionDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
            parent_flag = parent_flag + 1
            parent_type.append("parent_function")

        elif newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
            parent_flag = parent_flag + 1
            parent_type.append("parent_class")

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
    

    """Determine if there is a decorator"""
    decorator_property_flag = 0
    if node.decorators:
        for k in node.decorators.nodes:
            if (k.__class__ == astroid.Name) and (k.name == "property"):
                decorator_property_flag = decorator_property_flag + 1

    if (".".join(parent_func) in flag.keys()) and (flag[".".join(parent_func)]==0) and (decorator_property_flag == 0) and (node.name != '__init__'):
        """Determine whether its parent node also needs to be rewritten"""
        if (len(parent_func)> 1 and parent_flag>0 and (flag[".".join(parent_func[:-1])]==1) and parent_type[1] == "parent_function") or (parent_flag == 0):
            """
            The parent node exists and is a useful function, the child node needs to be rewritten, 
            or if there is no parent node, rewrite it directly

            Determine if the number of lines of code is greater than 5
            
            """
            num = 0
            for i in node.body:
                num = num + len(i.as_string().split('\n'))
    
            if num > 2:
                """generate file"""
                unused_file_name = ".".join(parent_func)
                tempnode = node
                pickle_dict[unused_file_name] = tempnode.as_string()
                node_re = rewrite_node(node, unused_file_name)

                return node_re

    return node

def rewrite_node(node: astroid.FunctionDef, unused_file_name):
    """
    rewrite function

    """
    argskey_temp = []
    decorator_info.clear()

    if node.decorators:
        for i in node.decorators.nodes:
            node_tmp = parse(i.as_string())

    argskey_temp.extend(decorator_info)    
    decorator_info.clear()
        
    if node.args.__class__ == astroid.Arguments:
        if node.args.args:
            for i in node.args.args:
                argskey_temp.append(i.name)
        for j in node.args.kwonlyargs:
            argskey_temp.append(j.name)
        for k in node.args.defaults:
            if isinstance(k, astroid.Name):
                argskey_temp.append(k.name)
        if node.args.vararg:
            argskey_temp.append(node.args.vararg)
        if node.args.kwarg:
            argskey_temp.append(node.args.kwarg)
 
 
    """Process the content in the body"""
    var_save.clear()
    import_save.clear()
    classdef_save.clear()
    func_para_save.clear()
    returnnum_save.clear()
    assignname_save.clear()
    functiondef_save.clear()

    for i in node.body:
        node_tmp = parse(i.as_string())
    
    """find useful variables"""
    new_add = []
    for i in var_save:
        if i not in argskey_temp:
            if i not in import_save:
                if i not in functiondef_save:
                    if i not in builtin_global:
                        if i not in assignname_save:
                            if i not in func_para_save:
                                if i not in classdef_save:
                                    new_add.append(i)

    """find global variables"""
    varible_globals = []
    varible_globals.extend(new_add)
    new_add.extend(argskey_temp)

    """number of returns"""
    return_num = 0
    if len(returnnum_save)> 0:
        return_num = returnnum_save[0]

    var_save.clear()
    import_save.clear()
    argskey_temp.clear()
    classdef_save.clear()
    returnnum_save.clear()
    func_para_save.clear()
    assignname_save.clear()
    functiondef_save.clear()

    """Rewrite the content of node.body"""
    newbody = []
    doc_info = node.doc
    new_node = node
    new_node.body = []
    new_node.doc = ''
    newannotation = []

    if new_node.args.__class__ == astroid.Arguments:
        newannotation = new_node.args.annotations
        for i in newannotation:
            if i != None:
                for k in i.get_children():
                    if k.__class__ == astroid.Name:
                        new_add.append(k.name)
                    if k.get_children():
                        for kk in k.get_children():
                            if kk.__class__ == astroid.Name:
                                new_add.append(kk.name)
        temp_newannotation = newannotation.copy()     
        new_node.args.annotations = newannotation.clear()

    if new_node.returns!=None:
        if new_node.returns.get_children():
            for mm in new_node.returns.get_children():
                if mm.__class__ == astroid.Name:
                    new_add.append(mm.name)
                if mm.get_children():
                    for kk in mm.get_children():
                        if kk.__class__ == astroid.Name:
                            new_add.append(kk.name)


    
    temp_return = new_node.returns
    new_node.returns = None
    funccall_string = new_node.as_string().strip()
    funccalls = funccall_string.split('\n')
    if len(funccalls)>1:
        for i in funccalls:
            if "def " in i:
                funccall_string=i

    funccall_string = funccall_string[4:]
    funccall_string = funccall_string[:-1]
    """Handle parameters with * """
    funccall_string = funccall_string.replace(' *,', '')
    funccall_string = "\"\"\"{}\"\"\"".format(funccall_string)

    new_node.args.annotations = temp_newannotation
    new_node.returns = temp_return
    node.doc = doc_info

    newcontent= '''
    import custom_funtemplate
    '''
    newbody.append(code2node(newcontent))

    inputvar = '{' +'}'
    if len(new_add)>0:
        inputvar = '{'
        for i in new_add:
            inputvar = inputvar + "\'{}\': {},".format(i, i)
        inputvar = inputvar[:-1] +'}'
   
    if return_num > 0:
        newcontent= '''
        return custom_funtemplate.rewrite_template('{}', {}, {}, {})
        '''.format(unused_file_name, funccall_string, inputvar, return_num)
        newbody.append(code2node(newcontent))
    else:
        newcontent= '''
        custom_funtemplate.rewrite_template('{}', {}, {}, {})
        '''.format(unused_file_name, funccall_string, inputvar, return_num)
        newbody.append(code2node(newcontent))


    node.body = newbody
    return node

    

"""Identify ways to rewrite nodes"""
def find_Return(node:astroid.Return):
    if node.value.__class__ == astroid.Tuple:
        if len(node.value.elts) not in returnnum_save:
            returnnum_save.append(len(node.value.elts))
    else:
        if 1 not in returnnum_save:
            returnnum_save.append(1)


def find_AssignName(node: astroid.AssignName):
    if node.name not in assignname_save:
        assignname_save.append(node.name)


def find_ClaDef(node:astroid.ClassDef):
    """
    Find the classdef under the node
    """
    if node.name not in classdef_save:
        classdef_save.append(node.name)

def find_FuncDef(node: astroid.FunctionDef):
    """
    Find the functiondef under the node
    """
    if node.name not in functiondef_save:
        functiondef_save.append(node.name)
    if node.args.__class__ == astroid.Arguments:
        if node.args.args:
            for i in node.args.args:
                if i.name not in func_para_save:
                    func_para_save.append(i.name)
        for j in node.args.kwonlyargs:
            if j.name not in func_para_save:
                func_para_save.append(j.name)
        for k in node.args.defaults:
            if isinstance(k, astroid.Name):
                func_para_save.append(k.name)
        if node.args.vararg:
            if node.args.vararg not in func_para_save:
                func_para_save.append(node.args.vararg)
        if node.args.kwarg:
            if node.args.kwarg not in func_para_save:
                func_para_save.append(node.args.kwarg)
 

def find_Import(node: astroid.Import):
    """
    Find the import under the node
    """
    for i in node.names:
        if i[1] is None:
            if i[0] not in import_save:
                import_save.append(i[0])
        else:
            if i[1] not in import_save:
                import_save.append(i[1])

def find_ImportFrom(node: astroid.ImportFrom):
    """
    Find the importfrom under the node
    """
    for i in node.names:
        if i[1] is None:
            if i[0] not in import_save:
                import_save.append(i[0])
        else:
            if i[1] not in import_save:
                import_save.append(i[1])


def find_Name(node: astroid.Name):
    if node.name not in var_save:
        var_save.append(node.name)
    if node.name not in decorator_info:
        decorator_info.append(node.name)

def read_built(inputfile):
    built_list = []
    file = open(inputfile) 
    for line in file:
       built_list.append(line.strip('\n'))
    file.close()
    return built_list

if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dirname",
        default=""
    )
    parser.add_argument(
        "--path",
        default=""
    )
    parser.add_argument(
        "--usedfuntionlist",
        default=""
    )
    parser.add_argument(
        "--unused_gzip_dir",
        default=""
    )
    parser.add_argument(
        "--builtlist",
        default=""
    )
    args = parser.parse_args()
    sta_file = args.dirname
    path = args.path
    used_functionlist = args.usedfuntionlist
    unused_gzip_dir = args.unused_gzip_dir
    buits_list_file = args.builtlist

    builtin_global = read_built(buits_list_file)

 

    astroid.MANAGER.register_transform( astroid.nodes.FunctionDef, pre_function_transform,)
    astroid.MANAGER.register_transform( astroid.nodes.ClassDef, pre_class_transform,)

    
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = "" + os.path.join(root, name)
                with open(handle_file,'r',encoding = 'utf-8') as f:
                    content = f.read()
                f.close()
                tree = parse(content)
                w = open(handle_file, 'w',encoding = 'utf-8')
                w.write(tree.as_string())
                w.close()
  

    """Mark useful functions as 1"""
    with open(used_functionlist,"r",encoding="utf-8") as f:
        content=f.read()
    
    list_name=content.split("\n")
    if len(list_name)>0:
        for i in list_name :
            flag[i]=1
    T=1

    """start processing"""
    astroid.MANAGER.register_transform( astroid.nodes.FunctionDef, function_transform)
    astroid.MANAGER.register_transform( astroid.Name, find_Name)
    astroid.MANAGER.register_transform( astroid.ImportFrom, find_ImportFrom)
    astroid.MANAGER.register_transform( astroid.Import, find_Import)
    astroid.MANAGER.register_transform( astroid.FunctionDef, find_FuncDef)
    astroid.MANAGER.register_transform( astroid.ClassDef, find_ClaDef)
    astroid.MANAGER.register_transform( astroid.AssignName, find_AssignName)
    astroid.MANAGER.register_transform( astroid.Return, find_Return)
      


    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                """write back"""
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()
                f.close()
                tree = parse(content)
                w = open(handle_file, 'w',encoding='utf-8')
                w.write(tree.as_string())
                w.close()
    

    import gzip
    with gzip.open(unused_gzip_dir, 'w') as fout:
        fout.write(json.dumps(pickle_dict).encode('utf-8'))
    fout.close()

