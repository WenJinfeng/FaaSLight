import os

def getPackgaeName(used_fun_result_output, input_package, output_file):
    """
    Take out the initial set and find the root

    """
    package_name = []

    for line in open(used_fun_result_output):
        line = line.strip('\n')
        line_content = line.split(".")
        rootName = ""

        if len(line_content)>1:
            rootName = line_content[0] + "/" +line_content[1]
        else:
            rootName = line_content[0]

        if os.path.exists("{}/{}".format(input_package, rootName)):
            rootName = rootName.replace("/",".")
            if rootName not in package_name:
                package_name.append(rootName)
        
    out = open(output_file, 'w', encoding='utf-8')
    for i in package_name:
        out.write(i)
        out.write("\n")

    out.close()



if __name__ == '__main__':
    pass
