
import os

#find all js files
def collect_files(dir):
    filelist = []
    file_size = 0
    print(dir)
    for parent, dirnames, filenames in os.walk(dir):
        
        for filename in filenames:
            # print('nnnn')
            file_size = file_size + os.path.getsize(os.path.join(parent,filename))
            if filename.endswith('.js'):
                #put file name and directory name into list
                # print(os.path.join(parent,filename))
                filelist.append(os.path.join(parent,filename))
    # print('aa')
    return filelist, file_size

#calculate LOC of a single file
def calc_linenum(file):
    with open(file) as f:
        code_lines = 0       #code lines
        comment_lines = 0    #Number of comment lines
        blank_lines = 0      #blank line
        is_comment = False
        start_comment_index = 0 #comment start
        for index,line in enumerate(f, start=1):
            line = line.strip() # remove blank character in start and end
            if not is_comment:
                if line.startswith("'''") or line.startswith('"""'):
                    is_comment = True
                    start_comment_index = index
                #Single line comments
                elif line.startswith('//'):
                    comment_lines+=1
                # blank line
                elif line == '':
                    blank_lines +=1
                # code line
                else:
                    code_lines +=1
            else:
                if line.endswith("'''") or line.endswith('"""'):
                    is_comment = False
                    comment_lines +=index-start_comment_index +1
                else:
                    pass

   
    return code_lines,blank_lines,comment_lines


def main(base_path):
    
    files, files_size = collect_files(base_path)
    total_code_num = 0   
    total_blank_num = 0   
    total_annotate_num = 0  
    for f in files:
        
        code_num, blank_num, annotate_num = calc_linenum(f)
        
        # if code_num>100:
        #     print(code_num)
        #     print(f)
        total_code_num += code_num
        total_blank_num += blank_num
        total_annotate_num += annotate_num

    print("application size (unzip): {} MB".format(files_size/1000000))
    print("code lines: {}".format(total_code_num))  
    print("blank lines: {}".format(total_blank_num))
    print("comment lines: {}".format(total_annotate_num))

if __name__ == '__main__':
    
    # application directory
    # base_path = '../test_application/test-init-numpy'
    base_path = 'your app path'
    main(base_path)
    