from genericpath import exists
import json
import os
import ast
from typing import DefaultDict

# Reads and loads JSON data from a file
def read_context(fileinput):
    with open(fileinput,'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict

# Checks if a file or module exists in the given directory path
# Returns a flag indicating the type of file found, the file path, and current position index
def file_exsit(rel_dir, one_package_str, i):
    # Construct file path with the current component
    temp_file = "{}.{}".format(rel_dir, one_package_str[i])
    
    # Check if directory exists for the module
    if os.path.exists(temp_file.replace('.','/')):
        # If there are more components in the package string, recursively check
        if (len(one_package_str)-1) > i:
            f, t, l = file_exsit(temp_file, one_package_str, i+1)
            return f, t, l
        else:
            # Check if this is a package (has __init__.py)
            if os.path.exists("{}/__init__.py".format(temp_file.replace('.','/'))):
                # Flag 3 indicates a package with __init__.py
                flag = 3
                return flag, '{}.__init__'.format(temp_file), i
            else:
                # Flag 0 indicates directory exists but not a Python module
                flag = 0
                return flag, temp_file, i
    else:
        # Check if a Python file exists for this module
        if os.path.exists("{}.py".format(temp_file.replace('.','/'))):
            # Flag 1 indicates a Python module file exists
            return 1, temp_file, i
        else:
            # Check if parent directory is a package
            h = temp_file.replace('.','/').split('/')[:-1]
            
            if os.path.exists('{}/__init__.py'.format('/'.join(h))):
                # Flag 2 indicates parent is a package
                return 2, '{}/__init__'.format('/'.join(h)).replace('/','.'), i-1
            else:
                # Flag 0 indicates no relevant Python module found
                flag = 0
                return flag, temp_file, i

# Parses a Python file into an abstract syntax tree (AST)
def get_ast(input_file):
    with open(input_file,'r',encoding='utf-8') as f:
        content = f.read()
    tree_node = ast.parse(content)
    return tree_node

# Process handler type 1 and 2 - handles specific components within a file
def handler12_process(find_file, flag, fun_component, dir_name, py_all):
    # Parse the file into AST
    tree_node = get_ast(find_file)
    fun_components = fun_component.split('.')
    
    # Initialize data structures to store analysis results
    function_tmp = [] 
    function_internal_tmp = [] 
    function_variable = [] 
    func_attr = {} 
    class_tmp = [] 
    class_func_tmp = [] 
    class_func_internel_tmp = [] 
    module_tmp = []
    level_tmp = []
    fromimport_tmp = []
    as_tmp = []
    
    # Extract import statements
    module_tmp, level_tmp, fromimport_tmp, as_tmp = get_importfrom(tree_node)
    
    add_str = [] 

    # Extract functions, nested functions, and their internals
    function_tmp, function_internal_tmp, function_internal_internal_tmp = get_function_3subfunction(tree_node)
    
    # Extract classes, their methods, and nested functions
    class_tmp, class_func_tmp, class_func_internel_tmp = get_class(tree_node)
    
    # Create a copy of function data to manipulate
    new_function_tmp = []
    for i in function_tmp:
        new_function_tmp.append(i)

    new_function_internal_tmp = []
    for i in function_internal_tmp:
        new_function_internal_tmp.append(i)

    new_function_internal_internal_tmp = []
    for i in function_internal_internal_tmp:
        new_function_internal_internal_tmp.append(i)

    # Remove functions that are methods of classes to avoid duplication
    for idx, val in enumerate(class_func_tmp):
        for val_internal in class_func_internel_tmp[idx]:
            for ex_func_i, ex_func_val in enumerate(function_tmp):
                if (ex_func_val == val) or (ex_func_val in val_internal):
                    new_function_tmp[ex_func_i] = ""
                    new_function_internal_tmp[ex_func_i] = ["null"]
                    new_function_internal_internal_tmp[ex_func_i] = ["null"]
    
    # Clean up the lists by removing empty entries
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

    # Process based on the component structure
    if len(fun_components) == 1:
        # Single component - could be a function, class, or imported name
        if fun_component in function_tmp:
            # It's a function in this file
            function_variable, func_attr1 = get_certainfunction(tree_node, fun_component)
            func_attr=merge_dict(func_attr,func_attr1)
        elif fun_component in class_tmp:
            # It's a class in this file
            function_variable, func_attr1 = get_certainclass(tree_node, fun_component)
            func_attr=merge_dict(func_attr,func_attr1)
        else:
            # Check if it's in any __all__ lists
            for key_i in py_all.keys():
                if fun_component in py_all[key_i]:
                    add_str.append("{}.{}".format(key_i, fun_component))
            
            # Check if it's imported
            tmp = variable_find_import(fun_component, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            add_str.extend(tmp)
    else:
        # Multi-part component - check for class methods or nested functions
        if fun_components[0] in class_tmp:
            if len(fun_components) > 2:
                # Class method with nested function
                function_variable, func_attr1 = get_certainclass_func_internal(tree_node, fun_components[0], fun_components[1], fun_components[2])
                func_attr=merge_dict(func_attr,func_attr1)
            else:
                # Class method
                function_variable, func_attr1 = get_certainclass_func(tree_node, fun_components[0], fun_components[1])
                func_attr=merge_dict(func_attr,func_attr1)
        if fun_components[0] in function_tmp:
            # Nested function
            function_variable, func_attr1 = get_nestedfunction(tree_node, fun_components[0], fun_components[1])
            func_attr=merge_dict(func_attr,func_attr1)
    
    # Process variables used in the function/class
    if len(function_variable) > 0:
        for variable_i in function_variable:
            # Check if variable is a class
            tmp = variable_find_class(variable_i, class_tmp, class_func_tmp, class_func_internel_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

            # Check if variable is a function
            tmp = variable_find_function(variable_i, function_tmp, function_internal_tmp, function_internal_internal_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

            # Check if variable is imported
            tmp = variable_find_import(variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    # Process attributes used in the function/class
    if len(func_attr) > 0:
        for attr_i in func_attr.keys():
            attr_i_values = func_attr[attr_i]
            tmp = attr_find_import(attr_i, attr_i_values, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    # Remove duplicates
    T = []
    for i in add_str:
        if not i in T:
            T.append(i)
    add_str = T
    
    return add_str   

# Process handler type 3 - handles entire file
def handler13_process(find_file, flag, dir_name):
    # Parse the file into AST
    tree_node = get_ast(find_file)
    
    # Initialize data structures
    function_variable = []
    func_attr = {}
    all_variable = []
    
    # Extract file-level names, attributes, and variables
    function_variable, func_attr, all_variable = get_File_Name(tree_node)
    
    # Extract import statements
    module_tmp = []
    level_tmp = []
    fromimport_tmp = []
    as_tmp = []
    module_tmp, level_tmp, fromimport_tmp, as_tmp = get_importfrom(tree_node)
    
    add_str = [] 

    # Extract functions and classes
    function_tmp = [] 
    function_internal_tmp = [] 
    class_tmp = [] 
    class_func_tmp = [] 
    class_func_internel_tmp = [] 
    
    function_tmp, function_internal_tmp, function_internal_internal_tmp = get_function_3subfunction(tree_node)
    class_tmp, class_func_tmp, class_func_internel_tmp = get_class(tree_node)
    
    # Create a copy of function data to manipulate
    new_function_tmp = []
    for i in function_tmp:
        new_function_tmp.append(i)

    new_function_internal_tmp = []
    for i in function_internal_tmp:
        new_function_internal_tmp.append(i)

    new_function_internal_internal_tmp = []
    for i in function_internal_internal_tmp:
        new_function_internal_internal_tmp.append(i)

    # Remove functions that are methods of classes to avoid duplication
    for idx, val in enumerate(class_func_tmp):
        for val_internal in class_func_internel_tmp[idx]:
            for ex_func_i, ex_func_val in enumerate(function_tmp):
                if (ex_func_val == val) or (ex_func_val in val_internal):
                    new_function_tmp[ex_func_i] = ""
                    new_function_internal_tmp[ex_func_i] = ["null"]
                    new_function_internal_internal_tmp[ex_func_i] = ["null"]
    
    # Clean up the lists by removing empty entries
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
    
    # Process variables used in the file
    if len(function_variable) > 0:
        for variable_i in function_variable:
            # Check if variable is a class
            tmp = variable_find_class(variable_i, class_tmp, class_func_tmp, class_func_internel_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

            # Check if variable is a function
            tmp = variable_find_function(variable_i, function_tmp, function_internal_tmp, function_internal_internal_tmp, flag, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)
            
            # Check if variable is imported
            tmp = variable_find_import(variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)
    
    # Process attributes used in the file
    if len(func_attr) > 0:
        for attr_i in func_attr.keys():
            attr_i_values = func_attr[attr_i]
            tmp = attr_find_import(attr_i, attr_i_values, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)
    
    # Process variables from __all__ list
    if len(all_variable) > 0:
        for all_variable_i in all_variable:
            tmp = variable_find_import(all_variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name)
            if len(tmp):
                add_str.extend(tmp)

    # Remove duplicates
    T = []
    for i in add_str:
        if not i in T:
            T.append(i)  
    add_str = T       
    
    return add_str 

# Find attribute usage in imports and track their source
def attr_find_import(attr_i, attr_i_values, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name):
    add_str = [] 
    
    # Iterate through all import statements
    for idx_module, val in enumerate(as_tmp):
        for idx_from, val_as in enumerate(val):
            if val_as == None:
                # Case when import doesn't use 'as' alias
                if fromimport_tmp[idx_module][idx_from] == attr_i:
                    # Regular import matching attribute name
                    if level_tmp[idx_module] == 0:
                        # Absolute import
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}".format(fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(module_tmp[idx_module], fromimport_tmp[idx_module][idx_from], value))

                    if level_tmp[idx_module] == 1:
                        # Relative import (from . import)
                        path_str = os.path.dirname(find_file)
                        path_str = path_str.replace(dir_name,"").replace('/','.')
                        
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from], value))
                    
                    if level_tmp[idx_module] == 2:
                        # Relative import (from .. import)
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from], value))
                        else:
                            for value in attr_i_values:
                                add_str.append("{}.{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from],value))                        
                elif fromimport_tmp[idx_module][idx_from] == "*":
                    # Wildcard import
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
                # Case when import uses 'as' alias
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

# Find variable references in classes
def variable_find_class(variable_i, class_tmp, class_func_tmp, class_func_internel_tmp, flag, find_file, dir_name):
    add_str = [] 
    
    # Check if the variable is a class or within class methods
    for idx_class, idx_class_val in enumerate(class_tmp):
        if variable_i == idx_class_val:
            # Variable is a class
            if (flag == 3) or (flag == 2):
                # Package (__init__.py) or parent package
                path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
            if flag == 1:
                # Regular Python file
                path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                    
            add_str.append("{}.{}".format(path_str, idx_class_val))

        # Check class methods
        for idx, val in enumerate(class_func_tmp[idx_class]):
            if variable_i in val:
                if (flag == 3) or (flag == 2):
                    path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
                if flag == 1:
                    path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                            
                add_str.append("{}.{}.{}".format(path_str, idx_class_val, val))
                        
            # Check nested functions in class methods
            for idx_internal, val_internal in enumerate(class_func_internel_tmp[idx_class][idx]):
                if variable_i == val_internal:
                    if (flag == 3) or (flag == 2):
                        path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
                    if flag == 1:
                        path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                            
                    add_str.append("{}.{}.{}.{}".format(path_str, idx_class_val, val, val_internal))
    return add_str    

# Find variable references in functions
def variable_find_function(variable_i, function_tmp, function_internal_tmp, function_internal_internal_tmp, flag, find_file, dir_name):
    add_str = [] 
    
    # Check if variable is a function
    if variable_i in function_tmp:
        path_str = ''
        if (flag == 3) or (flag == 2):
            path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
        if flag == 1:
            path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
        add_str.append("{}.{}".format(path_str, variable_i))

    # Check nested functions
    for idx, val in enumerate(function_internal_tmp):
        if variable_i in val:
            if (flag == 3) or (flag == 2):
                path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
            if flag == 1:
                path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                    
            add_str.append("{}.{}.{}".format(path_str,function_tmp[idx], variable_i))  
        
        # Check deeply nested functions
        if variable_i in function_internal_internal_tmp[idx]:
            if (flag == 3) or (flag == 2):
                path_str = os.path.dirname(find_file).replace(dir_name,"").replace('/','.')
            if flag == 1:
                path_str = find_file.replace('.py','').replace(dir_name,"").replace('/','.')
                    
            add_str.append("{}.{}.{}.{}".format(path_str,function_tmp[idx], function_internal_tmp[idx][0], variable_i))  
    
    return add_str

# Find variable references in imports
def variable_find_import(variable_i, module_tmp, fromimport_tmp, as_tmp, level_tmp, find_file, dir_name):
    add_str = [] 
    
    # Iterate through all import statements
    for idx_module, val in enumerate(as_tmp):
        for idx_from, val_as in enumerate(val):
            if val_as == None:
                # Case when import doesn't use 'as' alias
                if fromimport_tmp[idx_module][idx_from] == variable_i:
                    # Direct import match
                    if level_tmp[idx_module] == 0:
                        # Absolute import
                        if module_tmp[idx_module] == None:
                            add_str.append("{}".format(fromimport_tmp[idx_module][idx_from]))
                        else:
                           add_str.append("{}.{}".format(module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))

                    if level_tmp[idx_module] == 1:
                        # Relative import (from . import)
                        path_str = os.path.dirname(find_file)
                        path_str = path_str.replace(dir_name,"").replace('/','.')
                        
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
                            
                    if level_tmp[idx_module] == 2:
                        # Relative import (from .. import)
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"").replace('/','.')
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
                
                elif fromimport_tmp[idx_module][idx_from] == "*":
                    # Wildcard import
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
                # Case when import uses 'as' alias
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
                        path_str = os.path.dirname(os.path.dirname(find_file)).replace(dir_name,"")
                        if module_tmp[idx_module] == None:
                            add_str.append("{}.{}".format(path_str, fromimport_tmp[idx_module][idx_from]))
                        else:
                            add_str.append("{}.{}.{}".format(path_str, module_tmp[idx_module], fromimport_tmp[idx_module][idx_from]))
    
    return add_str

# Extract import statements from the AST
def get_importfrom(tree_node):
    module_tmp = []
    level_tmp = []
    importfrom_tmp = []
    as_tmp = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Import):
            # Regular import statement
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
            # From import statement
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

# Extract classes and their methods from the AST
def get_class(tree_node):
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

# Extract decorators from a class definition
def get_decoratorclass_func(tree_node):
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
            
            # Process decorator arguments
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

# Extract details about a specific class
def get_certainclass(tree_node, check_class):
    decorator_package_function = {}
    other_v = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            if node.name == check_class:
                # Get decorators
                decorator_package_function = get_decoratorclass_func(node)
                
                # Process decorator names
                for n in node.decorator_list:
                    other_v.extend(get_Name(n))
                    
                # Process class body for variables and attributes
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Namelist(k))
                        decorator_package_function = merge_dict(decorator_package_function, get_Attribute_func(k))

    # Remove duplicates
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    # Clean up attribute dictionary
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

# Extract details about a specific method in a class
def get_certainclass_func(tree_node, check_class, check_func):
    decorator_package_function = {}
    other_v = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            if node.name == check_class:
                # Get class decorators
                decorator_package_function = get_decoratorclass_func(node)
                
                for n in node.decorator_list:
                    other_v.extend(get_Name(n))
                    
                # Process class body for variables and attributes
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Namelist(k))
                        decorator_package_function = merge_dict(decorator_package_function, get_Attribute_func(k))

                # Find the specific method
                for node_class in ast.walk(node):
                    if isinstance(node_class, ast.FunctionDef):
                        a,b = get_certainfunction(node_class, check_func)
                        other_v.extend(a)
                        decorator_package_function = merge_dict(decorator_package_function, b)

    # Remove duplicates
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    # Clean up attribute dictionary
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

# Extract details about a nested function in a class method
def get_certainclass_func_internal(tree_node, check_class, check_func, check_func_internal):
    decorator_package_function = {}
    other_v = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.ClassDef):
            if node.name == check_class:
                # Get class decorators
                decorator_package_function = get_decoratorclass_func(node)
                
                for n in node.decorator_list:
                    other_v.extend(get_Name(n))
                    
                # Process class body for variables and attributes
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Namelist(k))
                        decorator_package_function= merge_dict(decorator_package_function, get_Attribute_func(k))
                
                # Find the nested function
                a, b = get_nestedfunction(tree_node, check_func, check_func_internal)
                other_v.extend(a)
                decorator_package_function = merge_dict(decorator_package_function, b)
                
    # Remove duplicates
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    # Clean up attribute dictionary
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

# Extract functions and their nested functions from AST
def get_function_subfunction(tree_node):
    function_tmp = [] 
    function_internal_tmp = [] 
    function_internal_tmp_node = []
    
    # Find all function definitions
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            function_tmp.append(node.name+"")
            tmp, tmp_node = get_function(node)
            # Remove the function itself from its nested functions
            tmp.remove(node.name)
            tmp_node.remove(node)
            function_internal_tmp.append(tmp)
            function_internal_tmp_node.append(tmp_node)

    return function_tmp, function_internal_tmp, function_internal_tmp_node

# Extract functions and their nested functions up to 3 levels deep
def get_function_3subfunction(tree_node):
    function_tmp = [] 
    function_internal_tmp = [] 
    function_internal_internal_tmp = [] 
    
    # Find all function definitions
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            function_tmp.append(node.name+"")
            tmp1, tmp2, tmp2_node = get_function_subfunction(node)
            
            # Remove the function itself from its nested functions
            tmp1.remove(node.name)
            
            second_func = []
            third_func = []
            
            # Find functions at the third level
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
            
            # Separate second level functions that aren't also third level
            for each_i in tmp2:
                for each_each_i in each_i:
                    if (each_each_i not in third_func) and (each_each_i not in second_func):
                        second_func.append(each_each_i)

            second_func=list(set(second_func))
            function_internal_tmp.append(second_func)
            function_internal_internal_tmp.append(third_func)

    return function_tmp, function_internal_tmp, function_internal_internal_tmp

# Extract all function names from an AST
def get_function(tree_node):
    function_tmp = []
    function_tmp_node = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            function_tmp.append(node.name+"")
            function_tmp_node.append(node)
            
    return function_tmp, function_tmp_node

# Extract details about a specific function
def get_certainfunction(tree_node, check_func):
    other_v = []
    func_map = {}
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            if node.name == check_func:
                # Process function body for variables and attributes
                for k in ast.iter_child_nodes(node):
                    if not isinstance(k, ast.FunctionDef):
                        other_v.extend(get_Name(k))
                        func_map = merge_dict(func_map, get_Attribute_func(k))
    
    # Remove duplicates
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    # Clean up attribute dictionary
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

# Extract details about a nested function
def get_nestedfunction(tree_node, check_func, check_nestfunc):
    other_v = []
    func_map = {}
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            if node.name == check_func:
                # Get parent function details
                a, b = get_certainfunction(node, check_func)
                other_v.extend(a)
                func_map = merge_dict(func_map, b)
                
                # Get nested function details
                c, d = get_certainfunction(node, check_nestfunc)
                other_v.extend(c)
                func_map = merge_dict(func_map, d)
    
    # Remove duplicates
    T = []
    for i in other_v:
        if not i in T:
            T.append(i)
    
    # Clean up attribute dictionary
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

# Extract all Name nodes from AST and remove duplicates
def get_Name(tree_node):
    Name_tmp = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Name):
            Name_tmp.append(node.id)
    
    # Remove duplicates
    T = []
    for i in Name_tmp:
        if not i in T:
            T.append(i)
            
    return T

# Extract all Name nodes from AST without removing duplicates
def get_Namelist(tree_node):
    Name_tmp = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.Name):
            Name_tmp.append(node.id)
    
    return Name_tmp

# Extract attribute access patterns from AST
def get_Attribute_func(tree_node):
    func_map = {}
    
    for node in ast.walk(tree_node):
        # Check for attribute access
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                if node.value.id in func_map.keys():
                    func_map[node.value.id].append(node.attr)
                else:
                    tmp = []
                    tmp.append(node.attr)
                    func_map[node.value.id] = tmp

        # Check for method calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id in func_map.keys():
                        func_map[node.func.value.id].append(node.func.attr)
                    else:
                        tmp = []
                        tmp.append(node.func.attr)
                        func_map[node.func.value.id] = tmp
            
            # Check for attribute access in call arguments
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

# Merge two dictionaries by combining their values
def merge_dict(dict1, dict2):
    combined_keys = dict1.keys() | dict2.keys()
    d_comb = {key: dict1.get(key, []) + dict2.get(key, []) for key in combined_keys}
    return d_comb

# Extract items from __all__ list in a module
def get_assign(tree_node):
    all_variable = []
    
    for node in ast.walk(tree_node):
        # Check for __all__ assignment
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ["__all__", "__ALL__"]:
                if isinstance(node.value, ast.List):
                    for i in node.value.elts:
                        all_variable.append(i.s)
        
        # Check for __all__ augmented assignment (+=)
        if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            if node.target.id in ["__all__", "__ALL__"]:
                if isinstance(node.value, ast.List):
                    for i in node.value.elts:
                        all_variable.append(i.s)
                        
    return all_variable

# Extract top-level names, attributes, and __all__ variables from a file
def get_File_Name(tree_node):
    # Get all names in the file
    Name_tmp = get_Namelist(tree_node)
    
    # Get all attributes in the file
    func_map = get_Attribute_func(tree_node)
    
    # Get variables from __all__ list
    all_variable = get_assign(tree_node)

    # Variables and attributes found in functions and classes
    functionclass_variable_tmp = []
    functionclass_func_tmp = {}
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            # Collect names used in functions
            functionclass_variable_tmp.extend(get_Namelist(node))
            functionclass_func_tmp = merge_dict(functionclass_func_tmp, get_Attribute_func(node))
        
        if isinstance(node, ast.ClassDef):
            # Collect decorators and attributes in classes
            functionclass_func_tmp = merge_dict(functionclass_func_tmp, get_decoratorclass_func(node))
            
            for n in node.decorator_list:
                functionclass_variable_tmp.extend(get_Name(n))
            
            # Process class body except for methods
            for k in ast.iter_child_nodes(node):
                if not isinstance(k, ast.FunctionDef):
                    functionclass_variable_tmp.extend(get_Namelist(k))
                    functionclass_func_tmp = merge_dict(functionclass_func_tmp, get_Attribute_func(k))

    # Remove variables defined in functions/classes from top-level names
    if len(functionclass_variable_tmp)>0:
        for i in functionclass_variable_tmp:
            for idx, j in enumerate(Name_tmp):
                if i == j:
                    Name_tmp[idx] = ''
                    break
    
    # Clean up the names list
    T = []
    for i in Name_tmp:
        if len(str(i))> 0:
            if not i in T:
                T.append(i)

    # Remove attributes defined in functions/classes from top-level attributes
    for i in functionclass_func_tmp.keys():
        if i in func_map.keys():
            for j in functionclass_func_tmp[i]:
                for idx, k in enumerate(func_map[i]):
                    if j == k:
                        func_map[i][idx]= ''
                        break
                        
    # Clean up the attributes map
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

# Find keys that are present in values but not in keys
def update_key(load_dict):
    keylist = load_dict.keys()
    add_key = []
    
    for value in load_dict.values():
        for i in value:
            if not i in keylist:
                add_key.append(i)
                
    add_key = list(set(add_key))
    
    return add_key

# Update the dependency graph with new information
def update_output(load_dict, rel_dir, dir_name, py_all, package_name=None):
    for key_i in load_dict.keys():
        # Split the key into components
        temp_key = key_i.split('.')
        
        # Check if the file exists
        flag, target_file, loc = file_exsit(rel_dir, temp_key, 0)
        
        find_file = ''
        fun_component = ''

        # Process based on the type of file found
        if flag ==1 and loc < len(temp_key)-1:
            # Regular Python file with more components in the key
            full_key_i = "{}.{}".format(rel_dir, key_i)
            fun_rep = full_key_i.replace("{}.".format(target_file),"")
            
            find_file = "{}.py".format(target_file.replace('.','/'))
            fun_component = fun_rep
             
        if flag == 1 and loc == len(temp_key)-1:
            # Regular Python file with no more components
            find_file = "{}.py".format(target_file.replace('.','/'))
                
        if flag == 2:
            # Parent package (__init__.py)
            find_file = "{}.py".format(target_file.replace('.','/'))
            fun_component = '.'.join(temp_key[loc+1:len(temp_key)])
            
        if flag == 3:
            # Package (__init__.py)
            find_file = "{}.py".format(target_file.replace('.','/'))
        
        add_str = []

        # Process the file based on flag type
        if flag ==2 or (flag ==1 and loc < len(temp_key)-1):
            # Process specific component within file
            add_str = handler12_process(find_file, flag, fun_component, dir_name, py_all)
        
        if flag == 3 or (flag == 1 and loc == len(temp_key)-1):
            # Process whole file
            add_str = handler13_process(find_file, flag, dir_name)

        # Add package name to paths if provided
        if package_name:
            add_str_with_package = []
            for path_str in add_str:
                parts = path_str.split('.')
                if len(parts) > 1:
                    for i, part in enumerate(parts):
                        if part == "ServerlessApp-main20220225" and i+1 < len(parts):
                            parts.insert(i+1, package_name)
                            break
                    add_str_with_package.append(".".join(parts))
                else:
                    add_str_with_package.append(path_str)
            add_str = add_str_with_package

        # Add to existing dependencies and remove duplicates
        if key_i in load_dict.keys():
            add_str.extend(load_dict[key_i])
            
        T = []
        for i in add_str:
            if not i in T:
                T.append(i)

        load_dict[key_i] = T
    
    return load_dict

# Main function to add information to the dependency graph
def add_info(path, jsoninput, handler_file, moshu_file, jsonoutput, package_name=None):
    # Get all __all__ variables from Python files
    py_all = get_all_value(path)

    dir_name = "{}/".format(path)
    
    # Use base directory name if package_name not provided
    if package_name is None:
        package_name = os.path.basename(path)

    # Load existing dependency graph
    load_dict = read_context(jsoninput)

    # Process each handler file
    for handler_i in handler_file:
        load_dict = handler_file_handle(handler_i, load_dict, dir_name, py_all, moshu_file, package_name)

    # Write the updated dependency graph to output file
    with open(jsonoutput, "w", encoding='utf-8') as f:
        f.write(json.dumps(load_dict))
    
    f.close

# Process a handler file and update the dependency graph
def handler_file_handle(handler_i, load_dict, dir_name, py_all, moshu_file, package_name=None):
    print("Processing--------{}".format(handler_i))
    rel_path = os.path.realpath(handler_i)
    
    # Get the directory path as a dot-separated string
    rel_dir = os.path.splitext(rel_path)[0].split('/')[:-1]
    rel_dir = ".".join([path for path in rel_dir])

    print("start 0")

    # Update dependency graph with existing keys
    load_dict = update_output(load_dict, rel_dir, dir_name, py_all, package_name)
    
    print('key value')
    
    # Find keys that need to be added
    add_key = update_key(load_dict)

    # Add special keys
    special_key = ['numpy.fromfunction']
    add_key.extend(special_key)

    print('ttttttttttt')

    # Add keys from the moshu file
    for line in open(moshu_file):
        line = line.strip('\n')
        add_key.append(line)

    print('add key')
    num = 1

    # Process all keys until no more new keys are found
    while len(add_key)>0:
        num = num +1
        print("start {} loop".format(num))
        add_keydict = {}
        for add_key_i in add_key:
            add_keydict[add_key_i] = []

        # Update with new keys
        load_dict.update(update_output(add_keydict, rel_dir, dir_name, py_all, package_name))
        
        # Find if there are any more keys to add
        add_key = update_key(load_dict)
    
    return load_dict

# Extract __all__ variables from all Python files in a directory
def get_all_value(path):
    dir_name = "{}/".format(path)
    py_all = {}
    handle_file= ""
    
    # Walk through all Python files in the directory
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = ""+os.path.join(root, name)
                tree_node = get_ast(handle_file)
                all_tmp = get_assign(tree_node)
                py_name = handle_file.replace(dir_name,'').split(".")[0].replace('/','.')
                py_all[py_name] = all_tmp

    return py_all