import os
import json
import astroid
from astroid import parse
import argparse

flag = {}
jug_module = {}
sta_file = ""
unused_dir = ""
handle_file = ""


import_flag = []
soimport_name = []
builtin_global = []
import_rewrite = []
import_rewrite_loc = []
T=0

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


def import_transform(node: astroid.Import):
    """
    Determine if this import is overridden

    """
    parent_imp = []
    import_list = []
    import_rewrite_self = []

    newnode = node
    road = handle_file.split("/")
    str_name=road.pop().split(".")

    """get the path of the file"""
    while len(road)>0:
        x=road.pop()
        if x==sta_file:
            break
        parent_imp.append(x)

    parent_imp= [i for i in parent_imp if(len(str(i))!=0)]
    parent_imp.reverse()
    file_rd=".".join(parent_imp)

    """Determine whether to rewrite"""
    for i in node.names:
        if i[0]!="lazy_import" and i[0]!="custom_funtemplate":
            if i[0] != '*':
                if file_rd !="":
                    if (flag.get(file_rd+"."+i[0], 'no') == 0) and (isContainedStr(file_rd+"."+i[0], flag) == "0") :
                        if jug_module.get(file_rd+"."+i[0], 'no') == 1:
                            if i[1] == None:
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[1], i[0]))
                        else:
                            if i[1] == None:
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[1], i[0]))
                    else:    
                        import_list.append(i)
                else:
                    if (flag.get(i[0], 'no') == 0 or flag.get(i[0], 'no') == "no") and (isContainedStr(i[0], flag) == "0") :
                        if jug_module.get(i[0], 'no') == 1:
                            if i[1] == None:
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[1], i[0]))
                        else:
                            if i[1] == None:
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[1], i[0]))
                    else:    
                        import_list.append(i)

        else:
            return node


    if isinstance(node.parent, astroid.Module):
        import_rewrite.append(import_rewrite_self)
        loc = 0
        for idx, i in enumerate(node.parent.body):
            if i == node:
                loc= idx
                break
        import_rewrite_loc.append(loc)

    else:

        if len(node.names)==1 and len(import_rewrite_self)>0:
            template_import=import_rewrite_self[0]
            import_flag.append("1")
            return code2node(template_import)
        
        elif len(node.names)>1 and len(import_rewrite_self)>0:
            import_rewrite.append(import_rewrite_self)
            loc = 0
            tempnode = node
            while tempnode.parent:
                if isinstance(tempnode.parent, astroid.Module):
                    for idx, i in enumerate(tempnode.parent.body):
                        if i == tempnode:
                            loc=idx
                            tempnode = tempnode.parent
                            break
                else:
                    tempnode = tempnode.parent
            import_rewrite_loc.append(loc)

    if (len(import_list)==0):
        return code2node("()")

    node.names=import_list
    return node


def importfrom_transform(node: astroid.ImportFrom):
    parent_imp = []
    import_list = []
    import_rewrite_self = []
    node_temp = node
    module_name = node.modname
    
    road=handle_file.split("/")
    str_name=road.pop().split(".")

    """get the path of the file"""
    while len(road)>0:
        x=road.pop()
        if x==sta_file:
            break
        parent_imp.append(x)

    parent_imp= [i for i in parent_imp if(len(str(i))!=0)]
    parent_imp.reverse()

    """dynamic link library"""
    if module_name in soimport_name:
        return node

    if node.level==None:
        parent_imp = module_name.split(".")
    else:
        if len(parent_imp)>0:
            for i in range(1, node.level):
                parent_imp.pop()
            parent_imp.append(module_name)
            parent_imp= [i for i in parent_imp if(len(str(i))!=0)]
    file_rd=".".join(parent_imp)

    for i in node.names:
        if i[0] == '*':
            import_list.append(i)
        if i[0] != '*':
            if (flag.get(file_rd+"."+i[0], 'no') == 0) and (isContainedStr(file_rd+"."+i[0], flag) == "0") :
                valuetemp =file_rd+"."+i[0]
                valuetemp = valuetemp.split(".")
                if i[1] == None:
                    """module is included"""
                    if (flag.get(file_rd, 'no') != 1):
                        if (jug_module.get('.'.join(valuetemp), 'no') == 1):
                            import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(valuetemp[-1], ".".join(valuetemp)))
                        else:
                            import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(valuetemp[-1], ".".join(valuetemp)))
                    else:
                        import_list.append(i)

                else:
                    if (flag.get(file_rd, 'no') != 1):
                        if jug_module.get('.'.join(valuetemp),'no')==1:
                            import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[1], ".".join(valuetemp)))
                        else:
                            import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[1], ".".join(valuetemp)))
                    else:
                        import_list.append(i)
            else:    
                import_list.append(i)


    if isinstance(node.parent, astroid.Module):
        import_rewrite.append(import_rewrite_self)
        loc = 0
        for idx, i in enumerate(node.parent.body):
            if i == node:
                loc= idx
                break
        import_rewrite_loc.append(loc)

    else:
        """There is also node in the outer layer of import"""
        if len(node.names)==1 and len(import_rewrite_self)>0:
            template_import=import_rewrite_self[0]
            import_flag.append("1")
            return code2node(template_import)

        elif len(node.names)>1 and len(import_rewrite_self)>0:
            import_rewrite.append(import_rewrite_self)
            loc = 0
            tempnode = node
            while tempnode.parent:
                if isinstance(tempnode.parent, astroid.Module):
                    for idx, i in enumerate(tempnode.parent.body):
                        if i == tempnode:
                            loc=idx
                            tempnode = tempnode.parent
                            break
                else:
                    tempnode = tempnode.parent
            import_rewrite_loc.append(loc)
            

    



    if (len(import_list)==0):
        return code2node("()")

    node.names=import_list
    return node

# ------------

def isContainedStr(importstr, flag):
    for key_i in flag.keys():
        if (importstr in key_i) and (flag[key_i]==1):
            """judge whether it is useful"""
            return "1"
    return "0"




"""Identify ways to rewrite nodes"""
def read_built(inputfile):
    built_list = []
    file = open(inputfile) 
    for line in file:
       built_list.append(line.strip('\n'))
    file.close()
    return built_list

def get_sofile(path):
    so_name = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.so'):
                so_name.append(name.split(".")[0])
    return so_name



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
        "--builtlist",
        default=""
    )
    parser.add_argument(
        "--module_name",
        default=""
    )
    args = parser.parse_args()
    path = args.path
    sta_file = args.dirname
    module_name = args.module_name
    buits_list_file = args.builtlist
    used_functionlist = args.usedfuntionlist

    builtin_global = read_built(buits_list_file)
    soimport_name = get_sofile(path)

 

    astroid.MANAGER.register_transform( astroid.nodes.FunctionDef, pre_function_transform )
    astroid.MANAGER.register_transform( astroid.nodes.ClassDef, pre_class_transform )

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()
                tree = parse(content)
                w = open(handle_file, 'w',encoding='utf-8')
                w.write(tree.as_string())
                w.close()
   
  

    """Mark useful functions as 1"""
    with open(used_functionlist,"r",encoding="utf-8") as f:
        content=f.read()
    
    list_name=content.split("\n")
    if len(list_name)>0:
        for i in list_name :
            flag[i]=1

    with open(module_name,"r",encoding="utf-8") as f:
        content=f.read()

    list_name=content.split("\n")
    if len(list_name)>0:
        for i in list_name :
            jug_module[i]=1
    T=1




    """start processing"""
    astroid.MANAGER.register_transform( astroid.nodes.ImportFrom, importfrom_transform )
    astroid.MANAGER.register_transform( astroid.nodes.Import,  import_transform )

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                import_rewrite = []
                import_rewrite_loc = []
                import_flag = []
                with open(handle_file,'r',encoding='utf-8') as f:
                    content = f.read()
                tree = parse(content)

                if len(import_rewrite)>0:
                    for idx, import_rewrite_i in enumerate(import_rewrite):
                        import_rewrite_i_temp = list(set(import_rewrite_i))
                        if len(import_rewrite_i_temp)>0:
                            loc= import_rewrite_loc[idx]
                            num = len(import_rewrite_i_temp)
                            new_tree = []
                            for k in range(0, len(tree.body)+num):
                                new_tree.append("temp")

                            for i in range(0, len(tree.body)):
                                if i<=loc:
                                    new_tree[i] = tree.body[i]
                                elif i>loc:
                                    new_tree[i+num] = tree.body[i]
                
                            for id_re, re in enumerate(import_rewrite_i_temp):
                                template_import='''
                                {}
                                '''.format(re)
                                new_tree[loc+id_re+1] = code2node(template_import)

                            import_rewrite_loc = [ h+num for h in import_rewrite_loc]
                            tree.body = new_tree
                            import_flag.append("1")
                                

                if "1" in import_flag:
                    if isinstance(tree.body[0], astroid.ImportFrom):
                        count =0
                        C = 0
                        while (isinstance(tree.body[count], astroid.ImportFrom)) and (tree.body[count].modname == "__future__"):
                            C = C+1
                            count = count +1
                        if C > 0:
                            treetmp = []
                            for k in range(0, len(tree.body)+1):
                                treetmp.append("temp")
                            for i in range(0, len(tree.body)):
                                if i<=(C-1):
                                    treetmp[i] = tree.body[i]
                                elif i>(C-1):
                                    treetmp[i+1] = tree.body[i]
                            treetmp[C] = code2node("import lazy_import")
                            tree.body = treetmp
                        else:
                            tree.body.insert(0, code2node("import lazy_import"))
                    
                    else:
                        tree.body.insert(0, code2node("import lazy_import"))

                import_rewrite = []
                import_rewrite_loc = []
                import_flag = []

                w = open(handle_file, 'w',encoding='utf-8')
                w.write(tree.as_string())
                w.close()
                
    


