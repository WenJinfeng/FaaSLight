
import os
import json
import shutil

import time

time_start = time.time()

input_package  = "XXXApp_name"

dir_name = input_package.split('/')[-1]
output_file = "{}/output.json".format(input_package)

assetsDir = {
    # ignore
    "ignorDir" : ["__pycache__", "tests", ".serverless", "pip", "pkg_resources", "setuptools", "wheel", "_distutils_hack"], 

    "ignorSpeDir": [],  
    
    "ignorFile": [".pyc", ".pyi", ".pth", ".virtualenv","_virtualenv.py",".md"],
}


def prepare():
    import removefile
    removefile.delFiles(input_package, assetsDir)


def serverless_func():
    entry_py = ["handler"]
    input_entry_point =[]
    for i in entry_py:
        input_entry_point.append("{}/{}.py".format(input_package, i))
    
    ymlFile= "{}/serverless.yml".format(input_package)
    seedfun_list = []
    if os.path.exists(ymlFile):
        import utiltool
        seedfun_list = utiltool.foryml(ymlFile)
    return ymlFile,seedfun_list,entry_py,input_entry_point

def magic_func():
    Identify_name = "Bert"
    moshu_file = "moshu_functions/{}.txt".format(Identify_name)
    os.system("python3 find_magic_origin.py --dirname {} --path {} --moshuoutput {}".format(dir_name, input_package, moshu_file))
    # Meanwhile, find serverless functions and save into entry_point.txt to service the component construct_graph()
    return Identify_name,moshu_file


def special_rule():
    global Identify_name,used_fun_result_output,input_package
    used_package_name = "used_func_result/used_package_{}.txt".format(Identify_name)

    import isContainPackage
    isContainPackage.getPackgaeName(used_fun_result_output, input_package, used_package_name)

    # find magic functions related to used packages
    moshu_file_update = "moshu_functions/{}_update.txt".format(Identify_name)
    os.system("python3 find_magic.py --dirname {} --path {} --packageset {} --moshuoutput {}".format(dir_name, input_package, used_package_name, moshu_file_update))

    # optinal: start - pre-loaded function generation for any package

    # input_package_dynamic_copy = "{}-dynamic".format(input_package)
    # shutil.copytree(input_package,input_package_dynamic_copy)

    # os.system("python3 importprocess.py --path {} ".format(input_package_dynamic_copy))

    # find_package_name = "sklearn"
    # log_name = "log-{}.log".format(find_package_name)
    # execute_py = "lambda_function.py"
    # os.system("python3 {}/{} >log/{}".format(input_package_dynamic_copy,execute_py,log_name))

    # log_genrate = "log/{}".format(log_name)
    # log_handle = "import-prefunc/{}-python36.txt".format(find_package_name)

    # import importsort
    # importsort.sortresult(log_genrate, input_package_dynamic_copy, log_handle)

    # shutil.rmtree(input_package_dynamic_copy)

    # optinal:  end - pre-loaded function generation



    # whitelist customization
    special_key=["requests.utils.set_environ", 
    "requests.sessions.Session.request", 
    "requests.adapters.HTTPAdapter.send", 
    "urllib3.connectionpool.connection_from_url",
    "numpy.linalg.lapack_lite", 
    "numpy.lib._iotools.NameValidator",
    "numpy.lib._iotools._decode_line",
    "numpy.lib._iotools.easy_dtype",
    "numpy.lib.npyio.loadtxt",
    "numpy.lib.npyio.loadtxt.flatten_dtype_internal",
    "numpy.lib.npyio.loadtxt.read_data",
    "numpy.lib.npyio.loadtxt.pack_items",
    "numpy.lib.npyio.loadtxt.split_line",
    "mpl_toolkits.axes_grid1.parasite_axes.host_axes_class_factory",
    "sklearn.ensemble._forest._parallel_build_trees",
    "pandas.io.parsers._read",
    "pandas.io.excel._xlwt._XlwtWriter",
    "pandas.io.excel._xlsxwriter._XlsxWriter",
    "pandas.io.excel._openpyxl._OpenpyxlWriter",
    "pandas.io.excel._odswriter._ODSWriter",
    "pandas.io.excel._base.ExcelWriter",
    "tensorflow.python.platform.resource_loader.get_path_to_datafile",
    "tensorflow.python.training.saving.saveable_object_util.saveable_objects_for_op",
    "tensorflow.python.keras.saving.saved_model.serialized_attributes.CommonEndpoints",
    "tensorflow.python.training.saver.BaseSaverBuilder",
    "tensorflow.python.summary.writer.writer.FileWriter",
    "tensorflow.python.keras.engine.base_layer.Layer",
    "urllib3.request.RequestMethods",
    "keras.saving.saved_model.load_context.load_context",
    "absl.third_party.unittest3_backport.result.TextTestResult",
    "keras.optimizer_v1.Optimizer"
    ]
    moshu_file_final = "moshu_functions/{}_final.txt".format(Identify_name)

    import processUtil
    processUtil.moshu_update(moshu_file_update, special_key, moshu_file_final)

    # generate the final useful function set (used_fun_result_output_final.txt)
    global seedfun_list,re_FunRel,input_entry_point

    
    used_fun_result_output_update = "used_func_result/used_func_{}_update.txt".format(Identify_name)
    processUtil.getDynamicContent(seedfun_list, input_package, re_FunRel, input_entry_point, moshu_file_final, used_fun_result_output_update)
    used_fun_result_output_final = "used_func_result/used_func_{}_final.txt".format(Identify_name)

    special_key_append = ["unittest.TestCase"]
    special_key_append = []
    processUtil.result_process(input_package, used_fun_result_output_update,used_fun_result_output_final, special_key_append)

    
    return used_package_name,moshu_file_final,used_fun_result_output_final


def construct_graph():
    global seedfun_list,input_entry_point

    re_FunRel = "{}/output-re.json".format(input_package)


    if len(seedfun_list)<=0:
        user_handler = []
        if os.path.exists("entry_point.txt"):
            for line in open("entry_point.txt"):
                line = line.strip('\n')
                if len(line)>0:
                    user_handler.append(line)
        if len(user_handler)>0:
            seedfun_list.extend(user_handler)
            for i in user_handler:
                temp = i.split(".")
                if len(temp)>1:
                    new_seed = ".".join(temp[:-1])
                    seedfun_list.append(new_seed)

    if not os.path.exists(output_file):
        os.mknod(output_file)
        intial_key={}
        for seed_i in seedfun_list:
            intial_key[seed_i] = []
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(json.dumps(intial_key))
        f.close()

    import staticAdd
    staticAdd.add_info(input_package, output_file, input_entry_point, moshu_file, re_FunRel)

    return re_FunRel

def initial_func():
    global Identify_name
    used_fun_result_output = "used_func_result/used_func_{}.txt".format(Identify_name)
    import processUtil
    processUtil.getDynamicContent_new(seedfun_list, input_package, re_FunRel, input_entry_point, used_fun_result_output)
    return used_fun_result_output



def func_rewrite():
    global Identify_name,used_fun_result_output_final,used_package_name

    used_fun_result_output_final_re = "used_func_result/used_func_{}_final_re.txt".format(Identify_name)
    prefunc_dir = "import-prefunc"

    import processUtil
    processUtil.result_addlibray(used_fun_result_output_final, used_package_name, prefunc_dir, used_fun_result_output_final_re)

    dir_name = input_package.split('/')[-1]
    buits_list_file = "built_list.txt"

    import removefile
    removefile.delFiles(input_package, assetsDir)

    gzip_file = "{}/gzipinfo.txt".format(input_package)
    os.system("python3 Fun_rewriting.py --dirname {} --path {} --usedfuntionlist {} --unused_gzip_dir {} --builtlist {}".format(dir_name, input_package, used_fun_result_output_final_re, gzip_file, buits_list_file))
    
    shutil.copy("custom_funtemplate_final_clear.py", "{}/custom_funtemplate.py".format(input_package))
    
    return used_fun_result_output_final_re,buits_list_file

if __name__ == "__main__": 
    
    # Step1: Optional File Elimination
    print("step1 start")
    prepare()
    print("step1 end")

    # Step2: Serverless Function Recognition
    print("step2 start")
    ymlFile,seedfun_list,entry_py,input_entry_point = serverless_func()
    print("step2 end")

    # Step3: Special Function Recognition
    print("step3 start")
    Identify_name,moshu_file = magic_func()
    used_package_name,moshu_file_final,used_fun_result_output_final = special_rule()
    print("step3 end")

    # Step4: Optional Function Generation 
    print("step4 start")
    re_FunRel = construct_graph()
    used_fun_result_output = initial_func()
    print("step4 end")

    # Step5: Function-level Rewriting
    print("step5 start")
    used_fun_result_output_final_re,buits_list_file = func_rewrite()
    print("step5 end")
