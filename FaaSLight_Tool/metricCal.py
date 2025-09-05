
import os

#Count all .py files in the specified directory and return them as a list.
def collect_files(dir):
    filelist = []
    file_size = 0
    print(dir)
    for parent, dirnames, filenames in os.walk(dir):
        # print('kkkk')
        for filename in filenames:
            # print('nnnn')
            file_size = file_size + os.path.getsize(os.path.join(parent,filename))
            if filename.endswith('.py'):
                #Combine filenames and directory names into absolute paths and add them to the list.
                # print(os.path.join(parent,filename))
                filelist.append(os.path.join(parent,filename))
    # print('aa')
    return filelist, file_size

#Count the number of lines of code within a single file
def calc_linenum(file):
    with open(file) as f:
        code_lines = 0       #Number of lines of code
        comment_lines = 0    #Number of comment lines
        blank_lines = 0      #Number of blank lines  Content is ‘\n’, becomes ‘’ after strip()
        is_comment = False
        start_comment_index = 0 #Record the positions of comments beginning with ‘’' or “”"
        for index,line in enumerate(f, start=1):
            line = line.strip() # Remove leading and trailing whitespace
            if not is_comment:
                if line.startswith("'''") or line.startswith('"""'):
                    is_comment = True
                    start_comment_index = index
                #Single-line comment
                elif line.startswith('#'):
                    comment_lines+=1
                # Blank line
                elif line == '':
                    blank_lines +=1
                # lines of code
                else:
                    code_lines +=1
            else:
                if line.endswith("'''") or line.endswith('"""'):
                    is_comment = False
                    comment_lines +=index-start_comment_index +1
                else:
                    pass

    # Return the number of code lines, blank lines, and comment lines.
    return code_lines,blank_lines,comment_lines


def main(base_path):
    # print('kggggg')
    files, files_size = collect_files(base_path)
    total_code_num = 0   #Statistical File Line Count Variable
    total_blank_num = 0   #Variable for counting the number of blank lines in statistical files
    total_annotate_num = 0  #Statistical File Comment Line Count Variable
    for f in files:
        code_num, blank_num, annotate_num = calc_linenum(f)
        total_code_num += code_num
        total_blank_num += blank_num
        total_annotate_num += annotate_num

    print("Application size (uncompressed) is: {} MB".format(files_size/1000000))
    print("The total number of lines of code is: {}".format(total_code_num))  
    print("Total number of blank lines is: {}".format(total_blank_num))
    print("Total number of comment lines is: {}".format(total_annotate_num))

if __name__ == '__main__':
    print()
   
    # base_path = '../test_application/test-init-numpy'
    # base_path = '/home/wenjinfeng/test_application/test-numpy/test-init-numpy-test-right'


    # main(base_path)