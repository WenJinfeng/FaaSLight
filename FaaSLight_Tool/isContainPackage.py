import os

def getPackgaeName(used_fun_result_output, input_package, output_file):
    package_name = []
    
    for line in open(used_fun_result_output):
        line = line.strip('\n')
        line_content = line.split(".")
        print(line_content)
        rootName = ""
        if len(line_content)>1:
            print("1")
            rootName = line_content[0] + "/" +line_content[1]
            print(rootName)
        else:
            print("2")
            rootName = line_content[0]

        if os.path.exists("{}/{}".format(input_package, rootName)):
            rootName = rootName.replace("/",".")
            if rootName not in package_name:
                package_name.append(rootName)
        
    print(package_name)
    out = open(output_file, 'w', encoding='utf-8')
    for i in package_name:
        out.write(i)
        out.write("\n")

    out.close()









if __name__ == '__main__':
    print('hh')
    input_package  = "/disk/wjf/Lxml_requests-test/sourcepython38slim2"
    used_fun_result_output = "used_func_result-requetslxml-python38.txt"
    output_file = "used_package-requetslxml-python38"
    getPackgaeName(used_fun_result_output, input_package, output_file)
