import os
import shutil
# def del_files(path,a):
#     print('sss')
#     for root , dirs, files in os.walk(path):
#         for name in files:
#             # print(name)
#             if name.endswith(a):
#                 os.remove(os.path.join(root, name))
#                 print ("" + os.path.join(root, name))


def delFiles(dirpath, assetsDir):
    for root , dirs, files in os.walk(dirpath):
        for dir in dirs:
            if dir in assetsDir["ignorDir"]:
                shutil.rmtree(os.path.join(root, dir))
                print ("Delete Dir: " + os.path.join(root, dir))
            for dirhouzhui in assetsDir["ignorSpeDir"]:
                if dir.endswith(dirhouzhui):
                    shutil.rmtree(os.path.join(root, dir))
                    print ("Delete Specific Dir: " + os.path.join(root, dir))

        for name in files:
            for houzhui in assetsDir["ignorFile"]:
                if name.endswith(houzhui):
                    os.remove(os.path.join(root, name))
                    print ("Delete File: " + os.path.join(root, name))
                    continue


if __name__ == "__main__":
    path = "/home/wenjinfeng/test_application/test-numpy/test-init-numpy-test-right"
    assetsDir = {
    
    "ignorDir" : ["__pycache__", "tests"], 
    
    "ignorSpeDir": [".dist-info"],  
    
    "ignorFile": [".pyc"],
}
    # a = '.pyc'
    delFiles(path,assetsDir)