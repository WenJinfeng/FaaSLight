from genericpath import exists
import json
import os
import ast
from typing import DefaultDict


def read_context(fileinput):
    with open(fileinput,'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def file_exsit(rel_dir, one_package_str, i):
    """
    Determine file type
    
    """
    temp_file = "{}.{}".format(rel_dir, one_package_str[i])

    if os.path.exists(temp_file.replace('.','/')):
        if (len(one_package_str)-1) > i:
            f, t, l = file_exsit(temp_file, one_package_str, i+1)
            return f, t, l
        else:
            if os.path.exists("{}/__init__.py".format(temp_file.replace('.','/'))):
                flag = 3
                return flag, '{}.__init__'.format(temp_file), i
            else:
                flag = 0
                return flag, temp_file, i

    else:
        if os.path.exists("{}.py".format(temp_file.replace('.','/'))):
            return 1, temp_file, i
        else:
            h = temp_file.replace('.','/').split('/')[:-1]

            if os.path.exists('{}/__init__.py'.format('/'.join(h))):
                return 2, '{}/__init__'.format('/'.join(h)).replace('/','.'), i-1
            else:
                flag = 0
                return flag, temp_file, i
    

def get_ast(input_file):

    with open(input_file,'r',encoding='utf-8') as f:
        content = f.read()
    tree_node = ast.parse(content)
    return tree_node




def handler12_process(find_file, flag, fun_component, dir_name, py_all):
    """
    Variables in functions and classes

    """
    
    tree_node = get_ast(find_file)
    fun_components = fun_component.split('.')

    as_tmp = []
    add_str = [] 
    func_attr = {}
    level_tmp = []
    class_tmp = []
    module_tmp = []
    function_tmp = []
    fromimport_tmp = []
    class_func_tmp = []
    function_variable = []
    function_internal_tmp = []
    class_func_internel_tmp = []
    module_tmp, level_tmp, fromimport_tmp, as_tmp = get_importfrom(tree_node)

    function_tmp, function_internal_tmp, function_internal_internal_tmp = get_function_3subfunction(tree_node)
    class_tmp, class_func_tmp, class_func_internel_tmp = get_class(tree_node)

    new_function_tmp = []
    for i in function_tmp:
        new_function_tmp.append(i)

    new_function_internal_tmp = []
    for i in function_internal_tmp:
        new_function_internal_tmp.append(i)

    new_function_internal_internal_tmp = []
    for i in function_internal_internal_tmp:
        new_function_internal_internal_tmp.append(i)


    for idx, val in enumerate(class_func_tmp):
        for val_internal in class_func_internel_tmp[idx]:
            for ex_func_i, ex_func_val in enumerate(function_tmp):
                if (ex_func_val == val) or (ex_func_val in val_internal):
                    new_function_tmp[ex_func_i] = ""
                    new_function_internal_tmp[ex_func_i] = ["null"]
                    new_function_internal_internal_tmp[ex_func_i] = ["null"]
    
    function_tmp = []
    for i in new_function_tmp:
        if len(str(i))!=0:
            function_tmp.append(i)

    function_internal_tmp = []
    for i in new_function_internal_tmp:
        if i != ["null"]:
            function_internal_tmp.append(i)

    function_internal_internal_tmp = []
    for i in new_function_internal_internal_tmp:
        if i != ["null"]:
            function_internal_internal_tmp.append(i)

    if len(fun_components) == 1:
        if fun_component in function_tmp:
            function_variable, func_attr1 = get_certainfunction(tree_node, fun_component)
            func_attr=merge_dict(func_attr,func_attr1)
        elif fun_component in class_tmp:
            function_variable, func_attr1 = get_certainclass(tree_node, fun_component)
            func_attr=merge_dict(func_attr,func_attr1)
        else:
            for key_i in py_all.keys():
                if fun_component in py_all[key_i]:
                    add_str.append("{}.{}".format(key_i, fun_component))
            tmp = variable_find_import(fun_component, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            add_str.extend(tmp)

    else:
        if fun_components[0] in class_tmp:
            if len(fun_components) > 2:
                function_variable, func_attr1 = get_certainclass_func_internal(tree_node, fun_components[0], fun_components[1], fun_components[2])
                func_attr=merge_dict(func_attr,func_attr1)
            else:
                function_variable, func_attr1 = get_certainclass_func(tree_node, fun_components[0], fun_components[1])
                func_attr=merge_dict(func_attr,func_attr1)
        if fun_components[0] in function_tmp:
            function_variable, func_attr1 = get_nestedfunction(tree_node, fun_components[0], fun_components[1])
            func_attr=merge_dict(func_attr,func_attr1)
    if len(function_variable) > 0:
        for variable_i in function_variable:
            tmp = variable_find_class(variable_i, class_tmp, class_func_tmp, class_func_internel_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

            tmp = variable_find_function(variable_i, function_tmp, function_internal_tmp, function_internal_internal_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

            tmp = variable_find_import(variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    if len(func_attr) > 0:
        for attr_i in func_attr.keys():
            attr_i_values = func_attr[attr_i]
            tmp = attr_find_import(attr_i, attr_i_values, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    T = []
    for i in add_str:
        if not i in T:
            T.append(i)
    add_str = T
    return add_str   
                                           
def handler13_process(find_file, flag, dir_name):
    """
    Variables not in functions and classes

    """
    tree_node = get_ast(find_file)
    
    as_tmp = []
    add_str = [] 
    func_attr = {}
    level_tmp = []
    class_tmp = []
    module_tmp = []
    function_tmp = []
    all_variable = []
    fromimport_tmp = []
    class_func_tmp = []
    function_variable = []
    function_internal_tmp = []
    class_func_internel_tmp = []

    function_variable, func_attr, all_variable = get_File_Name(tree_node)
    module_tmp, level_tmp, fromimport_tmp, as_tmp = get_importfrom(tree_node)
    function_tmp, function_internal_tmp, function_internal_internal_tmp = get_function_3subfunction(tree_node)
    class_tmp, class_func_tmp, class_func_internel_tmp = get_class(tree_node)

    new_function_tmp = []
    for i in function_tmp:
        new_function_tmp.append(i)

    new_function_internal_tmp = []
    for i in function_internal_tmp:
        new_function_internal_tmp.append(i)

    new_function_internal_internal_tmp = []
    for i in function_internal_internal_tmp:
        new_function_internal_internal_tmp.append(i)

    for idx, val in enumerate(class_func_tmp):
        for val_internal in class_func_internel_tmp[idx]:
            for ex_func_i, ex_func_val in enumerate(function_tmp):
                if (ex_func_val == val) or (ex_func_val in val_internal):
                    new_function_tmp[ex_func_i] = ""
                    new_function_internal_tmp[ex_func_i] = ["null"]
                    new_function_internal_internal_tmp[ex_func_i] = ["null"]
    
    function_tmp = []
    for i in new_function_tmp:
        if len(str(i))!=0:
            function_tmp.append(i)

    function_internal_tmp = []
    for i in new_function_internal_tmp:
        if i != ["null"]:
            function_internal_tmp.append(i)

    function_internal_internal_tmp = []
    for i in new_function_internal_internal_tmp:
        if i != ["null"]:
            function_internal_internal_tmp.append(i)

    if len(function_variable) > 0:

        for variable_i in function_variable:
            tmp = variable_find_class(variable_i, class_tmp, class_func_tmp, class_func_internel_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

            tmp = variable_find_function(variable_i, function_tmp, function_internal_tmp, function_internal_internal_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)
    
            tmp = variable_find_import(variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    if len(func_attr) > 0:
        for attr_i in func_attr.keys():
            attr_i_values = func_attr[attr_i]
            tmp = attr_find_import(attr_i, attr_i_values, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    if len(all_variable) > 0:
        for all_variable_i in all_variable:
            tmp = variable_find_import(all_variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    T = []
    for i in add_str:
        if not i in T:
            T.append(i)  
    add_str = T       

    return add_str 


def attr_find_import(attr_i, attr_i_values, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name):
    add_str = [] 

    for idx_module, val in enumerate(as_tmp):
        for idx_from, val_as in enumerate(val):
            if val_as == None:
                if fromimport_tmp[idx_module][idx_from] == attr_i:
                    if level_tmp[idx_module] == 0:
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}".format(fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(module_tmp[idx_module], fromimport_tmp[idx_module][idx_from], value))
                            

                    if level_tmp[idx_module] == 1:
                        path_str = os.path.dirname(find_file)
                        path_str = path_str.replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from], value))
                            
                            
                    if level_tmp[idx_module] == 2:
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from],value))                        
                elif fromimport_tmp[idx_module][idx_from] == "*":
                    if module_tmp[idx_module] == attr_i:
                        if level_tmp[idx_module] == 0:
                            for value in attr_i_values:
                                add_str.append("{}.{}".format(module_tmp[idx_module], value))
                        
                        if level_tmp[idx_module] == 1:
                            path_str = os.path.dirname(find_file)
                            path_str = path_str.replace(dir_name,"").replace('/','.')
                            
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module],value))
                        
                        if level_tmp[idx_module] == 2:
                            path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module],value))
    
            else:
                if as_tmp[idx_module][idx_from] == attr_i:
                    if level_tmp[idx_module] == 0:
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}".format(fromimport_tmp[idx_module][idx_from], value))
                        else:        
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(module_tmp[idx_module], fromimport_tmp[idx_module][idx_from], value))

                    if level_tmp[idx_module] == 1:
                        path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from], value))
                                        
                    if level_tmp[idx_module] == 2:
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from],value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from],value))
    return add_str


def variable_find_class(variable_i, class_tmp, class_func_tmp, class_func_internel_tmp, flag, find_file, dir_name):
    """
    Find variables corresponding to class

    """
    add_str = [] 
    for idx_class, idx_class_val in enumerate(class_tmp):
        if variable_i == idx_class_val:
            if (flag == 3) or (flag == 2):
                path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
            if flag ==1:
                path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                    
            add_str.append("{}.{}".format(path_str, idx_class_val))

        for idx, val in enumerate(class_func_tmp[idx_class]):
            if variable_i in val:
                if (flag == 3) or (flag == 2):
                    path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
                if flag ==1:
                    path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                            
                add_str.append("{}.{}.{}".format(path_str, idx_class_val, val))
                        
            for idx_internal, val_internal in enumerate(class_func_internel_tmp[idx_class][idx]):
                if variable_i == val_internal:
                    if (flag == 3) or (flag == 2):
                        path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
                    if flag ==1:
                        path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                            
                    add_str.append("{}.{}.{}.{}".format(path_str, idx_class_val, val, val_internal))
    return add_str    


def variable_find_function(variable_i, function_tmp, function_internal_tmp, function_internal_internal_tmp, flag, find_file, dir_name):
    """
    Find variables corresponding to function

    """
    add_str = []
    if variable_i in function_tmp:
        path_str = ''
        if (flag == 3) or (flag == 2):
            path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
        if flag ==1:
            path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
        add_str.append("{}.{}".format(path_str, variable_i))

    for idx, val in enumerate(function_internal_tmp):
        if variable_i in val:
            if (flag == 3) or (flag == 2):
                path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
            if flag ==1:
                path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                    
            add_str.append("{}.{}.{}".format(path_str,function_tmp[idx], variable_i))  
        
        
        if variable_i in function_internal_internal_tmp[idx]:
            if (flag == 3) or (flag == 2):
                path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
            if flag ==1:
                path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                    
            add_str.append("{}.{}.{}.{}".format(path_str,function_tmp[idx], function_internal_tmp[idx][0], variable_i))  
        

    
    return add_str


def variable_find_import(variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name):
    add_str = [] 
    for idx_module, val in enumerate(as_tmp):
        for idx_from, val_as in enumerate(val):
            if val_as == None:
                if fromimport_tmp[idx_module][idx_from] == variable_i:
                    if level_tmp[idx_module] == 0:
                        if module_tmp[idx_module] == None:
                            add_str.append("{}".format(fromimport_tmp[idx_module][idx_from]))
                        else:
                           add_str.append("{}.{}".format(module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))

                    if level_tmp[idx_module] == 1:
                        path_str = os.path.dirname(find_file)
                        path_str = path_str.replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
                            
                            
                    if level_tmp[idx_module] == 2:
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
                
                elif fromimport_tmp[idx_module][idx_from] == "*":
                    if module_tmp[idx_module] == variable_i:
                        if level_tmp[idx_module] == 0:
                            add_str.append("{}".format(module_tmp[idx_module]))


                        if level_tmp[idx_module] == 1:
                            path_str = os.path.dirname(find_file)
                            path_str = path_str.replace(dir_name,"").replace('/','.')
                        
                            add_str.append("{}.{}".format(path_str, module_tmp[idx_module]))
                            
                            
                        if level_tmp[idx_module] == 2:
                            path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        
                            add_str.append("{}.{}".format(path_str, module_tmp[idx_module]))
            
            else:
                if as_tmp[idx_module][idx_from] == variable_i:
                    if level_tmp[idx_module] == 0:
                        if module_tmp[idx_module] == None:
                            add_str.append("{}".format(fromimport_tmp[idx_module][idx_from]))
                        else:
                           add_str.append("{}.{}".format(module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
                             

                    if level_tmp[idx_module] == 1:
                        path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
                                        
                    if level_tmp[idx_module] == 2:
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
    
    return add_str




def get_importfrom(tree_node):
    module_tmp = []
    level_tmp = []
    importfrom_tmp = []
    as_tmp = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Import):
            module_tmp.append(None)
            level_tmp.append(0)
            from_content = []
            as_content = []
            for i in node.names:
                from_content.append(i.name+"")
                as_content.append(i.asname)
            importfrom_tmp.append(from_content)
            as_tmp.append(as_content)

        if isinstance(node, ast.ImportFrom):          
            module_tmp.append(node.module)
            level_tmp.append(node.level)
            from_content = []
            as_content = []
            for i in node.names:
                from_content.append(i.name+"")
                as_content.append(i.asname)
            importfrom_tmp.append(from_content)
            as_tmp.append(as_content)
    return module_tmp, level_tmp, importfrom_tmp, as_tmp

def get_class(tree_node):
    """
    Find all class names and class functions

    """
    class_tmp = []
    class_func_tmp = []
    class_func_internel_tmp = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            class_tmp.append(node.name+"")
            function_tmp, function_internal_tmp, function_internal_tmp_node = get_function_subfunction(node)
            class_func_tmp.append(function_tmp)
            class_func_internel_tmp.append(function_internal_tmp)
    return class_tmp, class_func_tmp, class_func_internel_tmp


def get_decoratorclass_func(tree_node):
    """
    Annotation content of the class

    """
    func_map = {}
    for node in tree_node.decorator_list:
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id in func_map.keys():
                        func_map[node.func.value.id].append(node.func.attr)
                    else:
                        tmp = []
                        tmp.append(node.func.attr)
                        func_map[node.func.value.id] = tmp
            
            for k in node.args:
                if isinstance(k, ast.Attribute):
                    if isinstance(k.value, ast.Name):
                        if k.value.id in func_map.keys():
                            func_map[k.value.id].append(k.attr)
                        else:
                            tmp = []
                            tmp.append(k.attr)
                            func_map[k.value.id] = tmp
    return func_map


def get_certainclass(tree_node, check_class):
    """
    Find variables in class

    """
    decorator_package_function = {}
    other_v = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            if node.name == check_class:
                decorator_package_function = get_decoratorclass_func(node)
                for n in node.decorator_list:
                    other_v.extend(get_Name(n))
                    
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Namelist(k))
                        decorator_package_function = merge_dict(decorator_package_function, get_Attribute_func(k))

    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    new_func_map = {}
    for i in decorator_package_function.keys():
        T1 = []
        for j in decorator_package_function[i]:
            if len(str(j))> 0:
                if not j in T1:
                    T1.append(j)
        if len(T1)>0:
            new_func_map[i]=T1

    return T, new_func_map


def get_certainclass_func(tree_node, check_class, check_func):
    """
    Find variables in class function

    """
    decorator_package_function = {}
    other_v = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            if node.name == check_class:
                decorator_package_function = get_decoratorclass_func(node)
                for n in node.decorator_list:
                    other_v.extend(get_Name(n))
                    
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Namelist(k))
                        decorator_package_function = merge_dict(decorator_package_function, get_Attribute_func(k))

            
                for node_class in ast.walk(node):
                    if isinstance(node_class, ast.FunctionDef):
                        a,b = get_certainfunction(node_class, check_func)
                        other_v.extend(a)
                        decorator_package_function = merge_dict(decorator_package_function, b)

    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    new_func_map = {}
    for i in decorator_package_function.keys():
        T1 = []
        for j in decorator_package_function[i]:
            if len(str(j))> 0:
                if not j in T1:
                    T1.append(j)
        if len(T1)>0:
            new_func_map[i]=T1

    return T, new_func_map

def get_certainclass_func_internal(tree_node, check_class, check_func, check_func_internal):
    decorator_package_function = {}
    other_v = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            if node.name == check_class:
                decorator_package_function = get_decoratorclass_func(node)
                for n in node.decorator_list:
                    other_v.extend(get_Name(n))
                    
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Namelist(k))
                        decorator_package_function= merge_dict(decorator_package_function, get_Attribute_func(k))
                a, b = get_nestedfunction(tree_node, check_func, check_func_internal)
                other_v.extend(a)
                decorator_package_function = merge_dict(decorator_package_function, b)
                
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    new_func_map = {}
    for i in decorator_package_function.keys():
        T1 = []
        for j in decorator_package_function[i]:
            if len(str(j))> 0:
                if not j in T1:
                    T1.append(j)
        if len(T1)>0:
            new_func_map[i]=T1

    return T, new_func_map


def get_function_subfunction(tree_node):
    function_tmp = []
    function_internal_tmp = []
    function_internal_tmp_node = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            function_tmp.append(node.name+"")
            tmp,tmp_node = get_function(node)
            tmp.remove(node.name)
            tmp_node.remove(node)
            function_internal_tmp.append(tmp)
            function_internal_tmp_node.append(tmp_node)

    return function_tmp, function_internal_tmp, function_internal_tmp_node


def get_function_3subfunction(tree_node):
    function_tmp = []
    function_internal_tmp = []
    function_internal_internal_tmp = []

    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            function_tmp.append(node.name+"")
            tmp1, tmp2, tmp2_node = get_function_subfunction(node)
            tmp1.remove(node.name)
            second_func = []
            third_func = []

            for id1, i in enumerate(tmp2_node):
                for id2, j in enumerate(i):
                    child_name=[]
                    for child in ast.walk(j):
                        if isinstance(child, ast.FunctionDef):
                            child_name.append(child.name)
                    child_name.remove(j.name)
                    if len(child_name)>0:
                        third_func.extend(child_name)
            third_func=list(set(third_func))

            for each_i in tmp2:
                for each_each_i in each_i:
                    if (each_each_i not in third_func) and (each_each_i not in second_func):
                        second_func.append(each_each_i)


            second_func=list(set(second_func))
            function_internal_tmp.append(second_func)
            function_internal_internal_tmp.append(third_func)

    return function_tmp, function_internal_tmp, function_internal_internal_tmp


def get_function(tree_node):
    """
    Get all function names under node

    """
    function_tmp = []
    function_tmp_node = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            function_tmp.append(node.name+"")
            function_tmp_node.append(node)
    return function_tmp, function_tmp_node


def get_certainfunction(tree_node, check_func):
    other_v = []
    func_map = {}
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            if node.name == check_func:
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Name(k))
                        func_map = merge_dict(func_map, get_Attribute_func(k))
                        
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    new_func_map = {}
    for i in func_map.keys():
        T1 = []
        for j in func_map[i]:
            if len(str(j))> 0:
                if not j in T1:
                    T1.append(j)
        if len(T1)>0:
            new_func_map[i]=T1
    return T, new_func_map


def get_nestedfunction(tree_node, check_func, check_nestfunc):
    """
    Variables for nested functions

    """
    other_v = []
    func_map = {}
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            if node.name == check_func:
                a, b = get_certainfunction(node, check_func)
                other_v.extend(a)
                func_map = merge_dict(func_map, b)
                c, d = get_certainfunction(node, check_nestfunc)
                other_v.extend(c)
                func_map = merge_dict(func_map, d)

    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    new_func_map = {}
    for i in func_map.keys():
        T1 = []
        for j in func_map[i]:
            if len(str(j))> 0:
                if not j in T1:
                    T1.append(j)
        if len(T1)>0:
            new_func_map[i]=T1

    return T, new_func_map


def get_Name(tree_node):
    """
    Unique

    """
    Name_tmp = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Name):
            Name_tmp.append(node.id)

    T = []
    for i in Name_tmp:
        if not i in T:
            T.append(i)
    return T

def get_Namelist(tree_node):
    Name_tmp = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Name):
            Name_tmp.append(node.id)
    return Name_tmp

def get_Attribute_func(tree_node):
    func_map = {}
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                if node.value.id in func_map.keys():
                    func_map[node.value.id].append(node.attr)
                else:
                    tmp = []
                    tmp.append(node.attr)
                    func_map[node.value.id] = tmp

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id in func_map.keys():
                        func_map[node.func.value.id].append(node.func.attr)
                    else:
                        tmp = []
                        tmp.append(node.func.attr)
                        func_map[node.func.value.id] = tmp
            
            for k in node.args:
                if isinstance(k, ast.Attribute):
                    if isinstance(k.value, ast.Name):
                        if k.value.id in func_map.keys():
                            func_map[k.value.id].append(k.attr)
                        else:
                            tmp = []
                            tmp.append(k.attr)
                            func_map[k.value.id] = tmp

    return func_map

def merge_dict(dict1, dict2):
    combined_keys = dict1.keys() | dict2.keys()
    d_comb = {key: dict1.get(key, []) + dict2.get(key, []) for key in combined_keys}
    return d_comb

def get_assign(tree_node):
    all_variable = []
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ["__all__", "__ALL__"]:
                if isinstance(node.value, ast.List):
                    for i in node.value.elts:
                        all_variable.append(i.s)
        if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            if node.target.id in ["__all__", "__ALL__"]:
                if isinstance(node.value, ast.List):
                    for i in node.value.elts:
                        all_variable.append(i.s)
    return all_variable

def get_File_Name(tree_node):
    Name_tmp = get_Namelist(tree_node)
    func_map = get_Attribute_func(tree_node)
    all_variable = get_assign(tree_node)

    functionclass_variable_tmp = []
    functionclass_func_tmp = {}
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            functionclass_variable_tmp.extend(get_Namelist(node))
            functionclass_func_tmp = merge_dict(functionclass_func_tmp, get_Attribute_func(node))
        if isinstance(node, ast.ClassDef):
            functionclass_func_tmp = merge_dict(functionclass_func_tmp, get_decoratorclass_func(node))
            for n in node.decorator_list:
                functionclass_variable_tmp.extend(get_Name(n))
            for k in ast.iter_child_nodes(node):
                if not isinstance(k, ast.FunctionDef):
                    functionclass_variable_tmp.extend(get_Namelist(k))
                    functionclass_func_tmp = merge_dict(functionclass_func_tmp, get_Attribute_func(k))

    if len(functionclass_variable_tmp)>0:
        for i in functionclass_variable_tmp:
            for idx, j in enumerate(Name_tmp):
                if i == j:
                    Name_tmp[idx] = ''
                    break
    T = []
    for i in Name_tmp:
        if len(str(i))> 0:
            if not i in T:
                T.append(i)

    for i in functionclass_func_tmp.keys():
        if i in func_map.keys():
            for j in functionclass_func_tmp[i]:
                for idx, k in enumerate(func_map[i]):
                    if j == k:
                        func_map[i][idx]= ''
                        break

    new_func_map = {}
    for i in func_map.keys():
        T1 = []
        for j in func_map[i]:
            if len(str(j))> 0:
                if not j in T1:
                    T1.append(j)
        if len(T1)>0:
            new_func_map[i]=T1
        
    return T, new_func_map, all_variable


 
def update_key(load_dict):
    keylist = load_dict.keys()
    add_key = []
    for value in load_dict.values():
        for i in value:
            if not i in keylist:
                add_key.append(i)
    add_key = list(set(add_key))
    return add_key

def update_output(load_dict, rel_dir, dir_name, py_all):

    for key_i in load_dict.keys():
        
        temp_key = key_i.split('.')
        flag, target_file, loc = file_exsit(rel_dir, temp_key, 0)

        find_file = ''
        fun_component = ''

        if flag ==1 and loc < len(temp_key)-1:
            full_key_i = "{}.{}".format(rel_dir, key_i)
            fun_rep = full_key_i.replace("{}.".format(target_file),"")
            find_file = "{}.py".format(target_file.replace('.','/'))
            fun_component = fun_rep
             
        if flag == 1 and loc == len(temp_key)-1:
            find_file = "{}.py".format(target_file.replace('.','/'))
                
        if flag == 2:
            find_file = "{}.py".format(target_file.replace('.','/'))
            fun_component = '.'.join(temp_key[loc+1:len(temp_key)])

        if flag == 3:
            find_file = "{}.py".format(target_file.replace('.','/'))
        
        add_str = []

        if flag ==2 or (flag ==1 and loc < len(temp_key)-1):
            add_str = handler12_process(find_file, flag, fun_component, dir_name, py_all)
        
        if flag == 3 or (flag == 1 and loc == len(temp_key)-1):
            add_str = handler13_process(find_file, flag, dir_name)

        if key_i in load_dict.keys():
            add_str.extend(load_dict[key_i])
        T = []
        for i in add_str:
            if not i in T:
                T.append(i)


        load_dict[key_i] = T
    
    return load_dict



def add_info(path, jsoninput, handler_file, moshu_file, jsonoutput):
    
    py_all = get_all_value(path)

    dir_name = "{}/".format(path)

    load_dict = read_context(jsoninput)

    for handler_i in handler_file:
        load_dict = handler_file_handle(handler_i, load_dict, dir_name, py_all, moshu_file)
    
    with open(jsonoutput, "w", encoding='utf-8') as f:
        f.write(json.dumps(load_dict))
    
    f.close()


def handler_file_handle(handler_i, load_dict, dir_name, py_all, moshu_file):

    rel_path = os.path.realpath(handler_i)
    rel_dir = os.path.splitext(rel_path)[0].split('/')[:-1]
    rel_dir = ".".join([path for path in rel_dir])

    load_dict = update_output(load_dict, rel_dir, dir_name, py_all)
    add_key = update_key(load_dict)

    special_key = ['numpy.fromfunction']
    add_key.extend(special_key)
    
    for line in open(moshu_file):
        line = line.strip('\n')
        add_key.append(line)

    num = 1

    while len(add_key)>0:
        num = num +1
        add_keydict = {}
        for add_key_i in add_key:
            add_keydict[add_key_i] = []
        load_dict.update(update_output(add_keydict, rel_dir, dir_name, py_all))
        add_key = update_key(load_dict)
    
    return load_dict
    

def get_all_value(path):

    dir_name = "{}/".format(path)
    py_all={}
    handle_file= ""
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                tree_node = get_ast(handle_file)
                all_tmp = get_assign(tree_node)
                py_name = handle_file.replace(dir_name,'').split(".")[0].replace('/','.')
                py_all[py_name] = all_tmp


    return py_all
                
           
if __name__ == "__main__":
    pass

