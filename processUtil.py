import json
import os

def read_context(fileinput):
    with open(fileinput,'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict

def getDynamicContent_new(seedfun_list, path, jsoninput, handler_file, dynamic_file_result_output):
    
    dir_name = "{}/".format(path)
    load_dict = read_context(jsoninput)

    main_func = []
    use_func = []
    main_func.extend(seedfun_list)
    use_func.extend(main_func)

    for handler_i in handler_file:
        use_func = handler_i_hanler(handler_i, use_func,load_dict)

    """write result"""
    final_functions = []
    for use_func_i in use_func:
        if '<builtin>' not in use_func_i:
            final_functions.append(use_func_i)

    final_functions.sort()
    w = open(dynamic_file_result_output, "w")
    for i in final_functions:
        w.write(i+"\n")
    w.close
    

def handler_i_hanler(handler_i, use_func,load_dict):

    """get relative path"""
    rel_path = os.path.realpath(handler_i)

    """get absolute path"""
    rel_dir = os.path.splitext(rel_path)[0].split('/')[:-1]
    
    """connect in the form of . """
    rel_dir = ".".join([path for path in rel_dir])

    use_func = seed_func_relation(use_func, load_dict, rel_dir)


    add_dir = []
    for func_i in use_func:
        func_i_list = func_i.split('.')
        is_dir = rel_dir
        for i in range(0, len(func_i_list)):
            is_dir =  "{}.{}".format(is_dir, func_i_list[i])
            if os.path.exists(is_dir.replace('.','/')):
                add_dir.append(is_dir.replace(rel_dir+".", ""))
                

    add_dir = list(set(add_dir))
    use_func.extend(add_dir)

    use_func_size = 0
    num = 0
    while len(use_func) > use_func_size:
        num = num +1
        use_func_size = len(use_func)
        use_func = seed_func_relation(use_func, load_dict, rel_dir)

    return use_func



def getDynamicContent(seedfun_list, path, jsoninput, handler_file, moshu_file, dynamic_file_result_output):
    
    dir_name = "{}/".format(path)
    load_dict = read_context(jsoninput)
    main_func = []
    main_func.extend(seedfun_list)


    for line in open(moshu_file):
        line = line.strip('\n')
        if not line in main_func:
            main_func.append(line)

    use_func = []
    use_func.extend(main_func)

    for handler_i in handler_file:
        use_func = handler_i_hanler(handler_i, use_func,load_dict)

    final_functions = []
    for use_func_i in use_func:
        if '<builtin>' not in use_func_i:
            final_functions.append(use_func_i)


    final_functions.sort()
    w = open(dynamic_file_result_output, "w")
    for i in final_functions:
        w.write(i+"\n")
    w.close
    

def extend_func(main_func, load_dict):
    """
    extend function collection
    
    """
    list_size = 0
    use_func = []
    main_func = list(set(main_func))

    for i in main_func:
        use_func.append(i)
    num = 0
    while len(use_func) > list_size:
        list_size = len(use_func)
        num =num+1
        use_func_tmp = []
        for j in use_func:
            use_func_tmp.append(j)
            if j in load_dict.keys():
                use_func_tmp.extend(load_dict[j])
        use_func = list(set(use_func_tmp))
    
    return use_func


def seed_func_relation(main_func, load_dict, rel_dir):
    
    use_func = []
    use_func.extend(main_func)
    main_func = list(set(main_func))
    use_func = list(set(use_func))
    use_func.extend(extend_func(main_func, load_dict))
    use_functions = []

    for use_func_i in use_func:
        if '<builtin>' not in use_func_i:
            use_functions.append(use_func_i)

    use_functions = list(set(use_functions))
    pyuse_functions = []

    for key_i in use_functions:
        temp_key = key_i.split('.')
        flag, target_file, loc = findfile(rel_dir, temp_key, 0)
            
        if flag ==1:
            target_file = target_file.replace(rel_dir+".","")
            pyuse_functions.append(target_file)
    
    use_functions.extend(extend_func(pyuse_functions,load_dict))
    use_functions = list(set(use_functions))
    
    return use_functions


def findfile(rel_dir, one_package_str, i):
    """
    Determine file type
    
    """
    temp_file = "{}.{}".format(rel_dir, one_package_str[i])
    if os.path.exists(temp_file.replace('.','/')):
        if (len(one_package_str)-1) > i:
            f, t, l = findfile(temp_file, one_package_str, i+1)
            return f, t, l
        else:
            if os.path.exists("{}/__init__.py".format(temp_file.replace('.','/'))):
                flag = 3
                return flag, '{}.__init__'.format(temp_file), i
            else: 
                flag = 0
                return flag, temp_file, i

    else:
        """Not a directory, judge whether it is a py file"""   
        if os.path.exists("{}.py".format(temp_file.replace('.','/'))):
            return 1, temp_file, i
        else:
            h = temp_file.replace('.','/').split('/')[:-1]

            if os.path.exists('{}/__init__.py'.format('/'.join(h))):
                return 2, '{}/__init__'.format('/'.join(h)).replace('/','.'), i-1
            else:
                flag = 0
                return flag, temp_file, i
 

def result_process(path, dynamic_file_result_output, dynamic_file_result_output_re, special_key_append):
    
    dir_name = "{}/".format(path)
    """Get the absolute path of the current file"""
    rel_dir = dir_name.split('/')[:-1]
    """connect in the form of . """
    rel_dir = ".".join([path for path in rel_dir])

    re_result_output = open(dynamic_file_result_output_re, "w")
    save_result = []

    for line in open(dynamic_file_result_output):
        line = line.strip('\n')
        save_result.append(line)
        temp_key = line.split('.')
        flag, target_file, loc = findfile(rel_dir, temp_key, 0)

        fun_component = ""
        for i in range(loc+1, len(temp_key)):
            fun_component= fun_component+"."+temp_key[i]
        
        content = "{}{}".format(target_file, fun_component)
        content= content.replace(rel_dir+".","")

        save_result.append(content)
        re_content= content.split(".")

        if len(re_content) > 1:
            re = re_content[0]
            if re_content[-1] == "__init__":
                if len(re_content)< 3:
                    save_result.append(re)
                if len(re_content) >= 3:
                    for i in range(1, len(re_content)-1):
                        re = re + "."+ re_content[i]
                    save_result.append(re)

    save_result.extend(special_key_append)
    save_result = list(set(save_result))
    save_result.sort()

    for save_result_i in save_result:
        re_result_output.write(save_result_i)
        re_result_output.write("\n")

    re_result_output.close
    return save_result
    
def result_addlibray(dynamic_file_result_output_re, add_libray, prefunc_dir, used_fun_final):

    save_result = ['custom_funtemplate.rewrite_template']

    for line in open(dynamic_file_result_output_re):
        line = line.strip('\n')
        save_result.append(line)

    used_package = []
    for line in open(add_libray):
        line = line.strip('\n')
        line_content = line.split(".")
        if len(line_content)>1:
            tmp_file = "{}/{}-python36.txt".format(prefunc_dir, line_content[0])
            
            if os.path.exists(tmp_file):
                """
                If there is a preload for this function, add to the useful set
                """
                for each_i in open(tmp_file):
                    each_i = each_i.strip('\n')
                    save_result.append(each_i)

        
        tmp_file = "{}/{}-python36.txt".format(prefunc_dir, line)
        if os.path.exists(tmp_file):
            """
            If there is a preload for this function, add to the useful set
            """
            for each_i in open(tmp_file):
                each_i = each_i.strip('\n')
                save_result.append(each_i)

    
    save_result = list(set(save_result))
    save_result.sort()
    
    re_result_output = open(used_fun_final, "w")
    for save_result_i in save_result:
        re_result_output.write(save_result_i)
        re_result_output.write("\n")
    re_result_output.close


def moshu_update(moshu_file, special_key, moshu_file_re):
    moshulist=[]
    for line in open(moshu_file):
        line = line.strip('\n')
        if len(line)>0:
            moshulist.append(line)
    
    new_add = []
    for special_key_i in special_key:
        for moshu_i in moshulist:
            if special_key_i.split('.')[0] in moshu_i.split('.')[0]:
                new_add.append(special_key_i)
                break

    moshulist.extend(new_add)
    moshu_output = open(moshu_file_re, 'w', encoding='utf-8')
    for i in moshulist:
        moshu_output.write(i)
        moshu_output.write("\n")
    moshu_output.close()

def used_function_update(usedfunction_funal, newadd_function, usedfunction_funal_update):
    funclist=[]

    ff = open(usedfunction_funal)
    fflines = ff.readlines()
    for line in fflines:
        line = line.strip('\n')
        if len(line)>0:
            funclist.append(line)
    ff.close()
    
    funclist = list(set(funclist))
    newlist=[]
    for line in open(newadd_function):
        line = line.strip('\n')
        if len(line)>0:
            newlist.append(line)

    newlist = list(set(newlist))
    funclist.extend(newlist)
    funclist = list(set(funclist))


    func_output = open(usedfunction_funal_update, 'w', encoding='utf-8')
    for i in funclist:
        func_output.write(i)
        func_output.write("\n")
    
    func_output.close()


if __name__ == "__main__":
    pass
