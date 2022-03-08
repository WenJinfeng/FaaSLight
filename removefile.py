import os
import shutil

def delFiles(dirpath, assetsDir):
    for root , dirs, files in os.walk(dirpath):
        for dir in dirs:
            if dir in assetsDir["ignorDir"]:
                shutil.rmtree(os.path.join(root, dir))
            for dirhouzhui in assetsDir["ignorSpeDir"]:
                if dir.endswith(dirhouzhui):
                    shutil.rmtree(os.path.join(root, dir))

        for name in files:
            for houzhui in assetsDir["ignorFile"]:
                if name.endswith(houzhui):
                    os.remove(os.path.join(root, name))
                    print ("Delete File: " + os.path.join(root, name))
                    continue


if __name__ == "__main__":
    pass