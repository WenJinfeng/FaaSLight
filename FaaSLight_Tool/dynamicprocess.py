import json
import os

# Reads and parses a JSON configuration file
def read_context(fileinput):
    with open(fileinput,'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict

# Processes a list of seed functions to identify all related functions without using magic file
# Parameters:
#   seedfun_list: Initial list of seed functions to analyze
#   path: Base path for the application
#   jsoninput: Path to the JSON file containing function relationships
#   handler_file: List of handler files to process
#   dynamic_file_result_output: Output file path for the results
def getDynamicContent_new(seedfun_list, path, jsoninput, handler_file, dynamic_file_result_output):
    
    dir_name = "{}/".format(path)

    # Load function relationship dictionary from JSON
    load_dict = read_context(jsoninput)
    
    # Initialize main function list with seed functions
    main_func = []
    main_func.extend(seedfun_list)

    # Initialize the list of functions in use
    use_func = []
    use_func.extend(main_func)

    # Process each handler file to find related functions
    for handler_i in handler_file:
        use_func = handler_i_hanler(handler_i, use_func,load_dict)

    print("add result")
    # Filter out builtin functions
    final_functions = []
    for use_func_i in use_func:
        if '<builtin>' not in use_func_i:
            final_functions.append(use_func_i)

    # Sort the final function list
    final_functions.sort()
    
    # Write results to output file
    w = open(dynamic_file_result_output, "w")
    for i in final_functions:
        w.write(i+"\n")
    w.close
    print("done！")
    
# Processes a single handler file to find all related functions
# Parameters:
#   handler_i: Path to the handler file
#   use_func: Current list of functions in use
#   load_dict: Dictionary of function relationships
# Returns:
#   Updated list of functions in use
def handler_i_hanler(handler_i, use_func,load_dict):

    print("processing---------------{}".format(handler_i))
    
    # Get the real path of the handler file
    rel_path = os.path.realpath(handler_i)
    
    # Extract the directory path
    rel_dir = os.path.splitext(rel_path)[0].split('/')[:-1]
    rel_dir = ".".join([path for path in rel_dir])

    print('====================================================')
    # Find related functions for the current list
    use_func = seed_func_relation(use_func, load_dict, rel_dir)
    print(list(set(use_func)))
    print('end====================================================')

    print("find possible note")
    
    # Find potential directory modules
    add_dir = []
    for func_i in use_func:
        func_i_list = func_i.split('.')
        is_dir = rel_dir
        for i in range(0, len(func_i_list)):
            is_dir =  "{}.{}".format(is_dir, func_i_list[i])
            if os.path.exists(is_dir.replace('.','/')):
                add_dir.append(is_dir.replace(rel_dir+".", ""))
                
    # Remove duplicates
    add_dir = list(set(add_dir))
    
    # Add directories to the function list
    use_func.extend(add_dir)

    print("start")
    use_func_size = 0
    
    # Recursively find all related functions until no new ones are found
    num = 0
    while len(use_func) > use_func_size:
        num = num +1
        print('start====={}==========='.format(num))
        use_func_size = len(use_func)
        use_func = seed_func_relation(use_func, load_dict, rel_dir)

    return use_func

# Similar to getDynamicContent_new but also incorporates "magic" functions from a file
# Parameters:
#   seedfun_list: Initial list of seed functions
#   path: Base path for the application
#   jsoninput: Path to the JSON file with function relationships
#   handler_file: List of handler files to process
#   moshu_file: Path to the "magic" file containing additional functions
#   dynamic_file_result_output: Output file for results
def getDynamicContent(seedfun_list, path, jsoninput, handler_file, moshu_file, dynamic_file_result_output):
    
    dir_name = "{}/".format(path)

    # Load function relationship dictionary
    load_dict = read_context(jsoninput)
    
    # Initialize main function list with seed functions
    main_func = []
    main_func.extend(seedfun_list)

    print("start magic")
    
    # Add functions from the magic file
    for line in open(moshu_file):
        line = line.strip('\n')
        if not line in main_func:
            main_func.append(line)

    use_func = []
    use_func.extend(main_func)

    # Process each handler file
    for handler_i in handler_file:
        use_func = handler_i_hanler(handler_i, use_func,load_dict)

    print("write in")
    # Filter out builtin functions
    final_functions = []
    for use_func_i in use_func:
        if '<builtin>' not in use_func_i:
            final_functions.append(use_func_i)

    # Sort the final function list
    final_functions.sort()
    
    # Write results to output file
    w = open(dynamic_file_result_output, "w")
    for i in final_functions:
        w.write(i+"\n")
    w.close
    print("done！")
    

# Extends a list of functions by recursively adding their dependencies
# Parameters:
#   main_func: Initial list of functions
#   load_dict: Dictionary of function relationships
# Returns:
#   Extended list of functions including all dependencies
def extend_func(main_func, load_dict):
    
    list_size = 0
    use_func = []
    main_func = list(set(main_func))

    for i in main_func:
        use_func.append(i)
    num = 0
    print(use_func)
    # Continue adding dependencies until no new functions are found
    while len(use_func) > list_size:
        list_size = len(use_func)
        num =num+1
        
        use_func_tmp = []
        for j in use_func:
            use_func_tmp.append(j)
            if j in load_dict.keys():
                print('{}----cunzai'.format(num))
                use_func_tmp.extend(load_dict[j])
        use_func = list(set(use_func_tmp))
    
    return use_func

# Finds related functions for a list of seed functions
# Parameters:
#   main_func: List of seed functions
#   load_dict: Dictionary of function relationships
#   rel_dir: Relative directory path for resolving imports
# Returns:
#   Extended list of functions with resolved imports
def seed_func_relation(main_func, load_dict, rel_dir):
    
    use_func = []
    use_func.extend(main_func)
    
    # Remove duplicates
    main_func = list(set(main_func))
    use_func = list(set(use_func))
    
    # Extend the function list with dependencies
    use_func.extend(extend_func(main_func, load_dict))
    
    # Filter out builtin functions
    use_functions = []
    for use_func_i in use_func:
        if '<builtin>' not in use_func_i:
            use_functions.append(use_func_i)

    use_functions = list(set(use_functions))
    
    # Find Python files corresponding to function names
    pyuse_functions = []

    for key_i in use_functions:
        temp_key = key_i.split('.')
        flag, target_file, loc = findfile(rel_dir, temp_key, 0)
            
        if flag ==1:
            target_file = target_file.replace(rel_dir+".","")
            pyuse_functions.append(target_file)
    
    # Extend with dependencies of Python files
    use_functions.extend(extend_func(pyuse_functions,load_dict))
        
    # Remove duplicates
    use_functions = list(set(use_functions))
    
    return use_functions

# Recursively searches for a Python module or package in the file system
# Parameters:
#   rel_dir: Base directory to start the search
#   one_package_str: Package/module path split into components
#   i: Current index in the package path
# Returns:
#   Tuple of (flag, target_file, loc) where:
#     flag: 0 for not found, 1 for file found, 2 for __init__ in parent, 3 for directory with __init__
#     target_file: Path to the found file
#     loc: Index position in one_package_str
def findfile(rel_dir, one_package_str, i):
    
    # Construct the path to check
    temp_file = "{}.{}".format(rel_dir, one_package_str[i])
    
    # Check if the path exists as a directory
    if os.path.exists(temp_file.replace('.','/')):
        
        # If not at the end of the package path, continue recursively
        if (len(one_package_str)-1) > i:
            f, t, l = findfile(temp_file, one_package_str, i+1)
            return f, t, l
        else:
            # Check if it's a package (has __init__.py)
            if os.path.exists("{}/__init__.py".format(temp_file.replace('.','/'))):
                flag = 3
                return flag, '{}.__init__'.format(temp_file), i
            else:
                # Not a package
                flag = 0
                return flag, temp_file, i

    # If the path doesn't exist as a directory, check if it's a Python file
    else:
        if os.path.exists("{}.py".format(temp_file.replace('.','/'))):
            return 1, temp_file, i
        else:
            # Check if parent directory is a package
            h = temp_file.replace('.','/').split('/')[:-1]
            
            if os.path.exists('{}/__init__.py'.format('/'.join(h))):
                return 2, '{}/__init__'.format('/'.join(h)).replace('/','.'), i-1
            else:
                flag = 0
                return flag, temp_file, i
 
# Processes the raw results from dynamic analysis to normalize paths and add special keys
# Parameters:
#   path: Base path for the application
#   dynamic_file_result_output: Input file with raw results
#   dynamic_file_result_output_re: Output file for processed results
#   special_key_append: Additional special keys to append
# Returns:
#   List of processed results
def result_process(path, dynamic_file_result_output, dynamic_file_result_output_re, special_key_append):
    
    dir_name = "{}/".format(path)
    
    # Extract relative directory path
    rel_dir = dir_name.split('/')[:-1]
    rel_dir = ".".join([path for path in rel_dir])
    
    # Open output file
    re_result_output = open(dynamic_file_result_output_re, "w")

    # Initialize result list
    save_result = []
    
    # Process each line from the input file
    for line in open(dynamic_file_result_output):
        line = line.strip('\n')
        save_result.append(line)
        
        print("-------------")
        print(line)
        # Split the function path
        temp_key = line.split('.')
        
        # Find the corresponding file
        flag, target_file, loc = findfile(rel_dir, temp_key, 0)
        print(findfile(rel_dir, temp_key, 0))

        # Extract function component
        fun_component = ""
        for i in range(loc+1, len(temp_key)):
            fun_component= fun_component+"."+temp_key[i]
        
        # Combine file path with function component
        content = "{}{}".format(target_file, fun_component)
        content= content.replace(rel_dir+".","")
        
        print(content)
        
        save_result.append(content)
        
        # Process __init__ modules specially
        re_content= content.split(".")

        if len(re_content) > 1:
            re = re_content[0]
            if re_content[-1] == "__init__":
                if len(re_content)< 3:
                    print(re)
                    save_result.append(re)
                    
                if len(re_content) >= 3:
                    for i in range(1, len(re_content)-1):
                        re = re + "."+ re_content[i]

                    print(re)
                    save_result.append(re)
                    
    # Add special keys
    save_result.extend(special_key_append)
    save_result = list(set(save_result))
    save_result.sort()

    # Write results to output file
    for save_result_i in save_result:
        re_result_output.write(save_result_i)
        re_result_output.write("\n")

    re_result_output.close
    return save_result
    
# Adds standard library dependencies to the results
# Parameters:
#   dynamic_file_result_output_re: Input file with processed results
#   add_libray: File containing libraries to add
#   prefunc_dir: Directory containing predefined function lists
#   used_fun_final: Output file for final results
def result_addlibray(dynamic_file_result_output_re, add_libray, prefunc_dir, used_fun_final):

    # Initialize with template function
    save_result = ['custom_funtemplate.rewrite_template']

    # Add processed results
    for line in open(dynamic_file_result_output_re):
        line = line.strip('\n')
        save_result.append(line)

    # Add library dependencies
    used_package = []
    for line in open(add_libray):
        line = line.strip('\n')
        
        # Check if it's a package with multiple components
        line_content = line.split(".")
        if len(line_content)>1:
            tmp_file = "{}/{}-python36.txt".format(prefunc_dir, line_content[0])
            
            if os.path.exists(tmp_file):
                print("{}".format(tmp_file))
                
                for each_i in open(tmp_file):
                    each_i = each_i.strip('\n')
                    save_result.append(each_i)
            else:
                print("{}".format("{}/{}-python36.txt".format(prefunc_dir, line_content[0])))

        # Check for the complete module
        tmp_file = "{}/{}-python36.txt".format(prefunc_dir, line)
        if os.path.exists(tmp_file):
            print("{}".format(tmp_file))
            
            for each_i in open(tmp_file):
                each_i = each_i.strip('\n')
                save_result.append(each_i)

        else:
            print("{}".format("{}/{}-python36.txt".format(prefunc_dir, line)))

    # Remove duplicates and sort
    save_result = list(set(save_result))
    save_result.sort()
    
    # Write to output file
    re_result_output = open(used_fun_final, "w")
    for save_result_i in save_result:
        re_result_output.write(save_result_i)
        re_result_output.write("\n")

    re_result_output.close

# Updates the magic function list with new special keys
# Parameters:
#   moshu_file: Original magic function file
#   special_key: Special keys to consider adding
#   moshu_file_re: Output file for updated magic functions
def moshu_update(moshu_file, special_key, moshu_file_re):
    # Read existing magic functions
    moshulist=[]
    for line in open(moshu_file):
        line = line.strip('\n')
        if len(line)>0:
            moshulist.append(line)
    
    # Find matching special keys to add
    new_add = []
    for special_key_i in special_key:
        for moshu_i in moshulist:
            if special_key_i.split('.')[0] in moshu_i.split('.')[0]:
                new_add.append(special_key_i)
                print("添加")
                print(special_key_i)
                break
    
    # Add new functions to the list
    moshulist.extend(new_add)
    
    # Write updated list to output file
    moshu_output = open(moshu_file_re, 'w', encoding='utf-8')
    
    for i in moshulist:
        moshu_output.write(i)
        moshu_output.write("\n")
    
    moshu_output.close()

# Updates the list of used functions with new additions
# Parameters:
#   usedfunction_funal: Original used function file
#   newadd_function: File containing new functions to add
#   usedfunction_funal_update: Output file for updated function list
def used_function_update(usedfunction_funal, newadd_function, usedfunction_funal_update):
    # Read existing functions
    funclist=[]

    ff = open(usedfunction_funal)
    fflines = ff.readlines()
    for line in fflines:
        line = line.strip('\n')
        if len(line)>0:
            funclist.append(line)
    ff.close()
    
    funclist = list(set(funclist))
    
    # Read new functions to add
    newlist=[]
    for line in open(newadd_function):
        line = line.strip('\n')
        if len(line)>0:
            newlist.append(line)

    newlist = list(set(newlist))

    # Combine lists and remove duplicates
    funclist.extend(newlist)
    funclist = list(set(funclist))

    # Write updated list to output file
    func_output = open(usedfunction_funal_update, 'w', encoding='utf-8')
    
    for i in funclist:
        func_output.write(i)
        func_output.write("\n")
    
    func_output.close()


if __name__ == "__main__":

    print()



















