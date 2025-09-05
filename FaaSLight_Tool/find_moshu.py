import os
import astroid
from astroid import parse
import argparse


sta_file="" # Base directory name to start from
moshu_save = [] # List to store found magic methods

# Transform function to identify and extract magic methods from AST nodes
# Parameters:
#   node: An astroid FunctionDef node representing a function definition
# Returns:
#   The original node (transformation is for side effects only)
def function_transform(node: astroid.FunctionDef):
    body = []

    # Navigate up the AST to build the full function path
    newnode = node
    parent_func = [ node.name ]
    while newnode.parent:
        if newnode.parent.__class__ == astroid.FunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    # Extract file path components
    road=handle_file.split("/")

    str_name=road.pop().split(".")
    parent_func.append(str_name[0])

    # Build the complete path up to the base directory
    while len(road)>0:
        x=road.pop()
        if x==sta_file:
            break
        parent_func.append(x)

    # Clean up and reverse to get correct order (package.module.class.function)
    parent_func= [i for i in parent_func if(len(str(i))!=0)]
    parent_func.reverse()

    # List of magic methods to look for
    moshu_func = ["__getitem__", "__setitem__", "__delitem__","__len__", "__iter__"]

    # Check if the current function is a magic method we're interested in
    if node.name in moshu_func:
        print(".".join(parent_func))
        if not ".".join(parent_func) in moshu_save:
            moshu_save.append(".".join(parent_func))
        
    return node

if __name__ == "__main__": 
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dirname",
        default=""
    )
    parser.add_argument(
        "--path",
        default=""
    )
    parser.add_argument(
        "--packageset",
        default=""
    )
    parser.add_argument(
        "--moshuoutput",
        default=""
    )
    args = parser.parse_args()
    sta_file = args.dirname  # Base directory name
    path = args.path  # Path to search in
    packageset = args.packageset  # File containing package names to filter
    moshu_file = args.moshuoutput  # Output file for magic methods

    # Load package filter set from file
    dirset=[]
    for line in open(packageset):
        line = line.strip('\n')
        if len(line)>0:
            dirset.append(line)

    print(dirset)    
    # Register the transformation function with astroid
    astroid.MANAGER.register_transform(
        astroid.nodes.FunctionDef,
        function_transform,
    )

    # Walk through all Python files in the specified path
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                print(os.path.join(root, name))
                handle_file = ""+os.path.join(root, name)
                for dir_i in dirset:
                    # Convert package notation to file path
                    dir_i = dir_i.replace(".","/")
                    if dir_i in handle_file:
                        # Parse the Python file and apply transformations
                        with open(handle_file,'r',encoding='utf-8') as f:
                            content = f.read()
                        
                        tree = parse(content)

    # Print and save the found magic methods
    print(moshu_save)
    moshu_output = open(moshu_file, 'w', encoding='utf-8')

    for i in moshu_save:
        moshu_output.write(i)
        moshu_output.write("\n")
    
    
    moshu_output.close()


