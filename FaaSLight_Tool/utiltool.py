

import yaml
# import os

def foryml(ymlPath):
    seed_func = []
    open_file = open(ymlPath, 'r', encoding='utf-8')
    result = open_file.read()
    file_dict = yaml.load(result, Loader=yaml.FullLoader)  # 用load方法转字典
    
    i = 0
    j = 0
    for key1 in file_dict['functions'].keys():
        for key2 in file_dict['functions'][key1].keys():
            if key2=="handler":
                seed_func.append(file_dict['functions'][key1][key2])
                seed= file_dict['functions'][key1][key2]
                temp = seed.split(".")
                if len(temp)>1:
                    new_seed = ".".join(temp[:-1])
                    # print(new_seed)
                    seed_func.append(new_seed)
    return seed_func

        
import os        

def get_module(path, output_file):

    dir_name = path.split("/")[-1]
    
    f=open(output_file,"w",encoding="utf-8")
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                # print(os.path.join(root, name))
                file=root.split('/')
                for i in range(len(file)):
                    if file[i]==dir_name:
                        file=file[i+1:]
                        break
                file.append(name.split('.')[0])
                f.write('.'.join(file)+'\n')
        for name in dirs:
            file=root.split('/')
            for i in range(len(file)):
                if file[i]==dir_name:
                    file=file[i+1:]
                    break
            file.append(name)
            f.write('.'.join(file)+'\n')

    

# ymlPath= "/home/wenjinfeng/wineML/slim3/serverless.yml"
# print(foryml(ymlPath))