import os
import json
import astroid
from astroid import parse
import argparse

# Global variables for tracking file paths and states
handle_file = ""  # Current file being processed
flag = {}  # Dictionary to track function usage status
sta_file = ""  # Starting directory for the analysis
unused_dir = ""  # Directory for unused functions

# Dictionary to store unused functions
pickle_dict = {}

# Flag to control transformation phases
T = 0  # 0: Pre-processing phase, 1: Transformation phase

# Lists to collect various code elements during analysis
decorator_info = []  # Stores decorator information
var_save = []  # Stores variable names
import_save = []  # Stores import names
functiondef_save = []  # Stores function definitions
classdef_save = []  # Stores class definitions
func_para_save = []  # Stores function parameters
assignname_save = []  # Stores assigned variable names
returnnum_save = []  # Stores number of return values
builtin_global = []  # Stores built-in function names


def code2node(code):
    """
    Convert code string to AST node
    Args:
        code: Python code as string
    Returns:
        AST node representing the code
    """
    try:
        return astroid.extract_node(code)
    except ValueError:
        tree = astroid.parse(code)
        return astroid.nodes.Const(tree.doc)


def pre_function_transform(node: astroid.FunctionDef):
    """
    First-pass transformation for functions
    Identifies function paths and marks them in the flag dictionary
    
    Args:
        node: Function definition node
    Returns:
        The original node
    """
    if (T == 1): return node
    body = []
    
    # Build function path by traversing parent hierarchy
    newnode = node
    
    parent_func = [node.name]
    while newnode.parent:
        if newnode.parent.__class__ == astroid.FunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
            
        else:
            newnode = newnode.parent
            continue

    # Extract path components from file path
    road = handle_file.split("/")

    str_name = road.pop().split(".")
    parent_func.append(str_name[0])

    while len(road) > 0:
        x = road.pop()
        if x == sta_file:
            break
        parent_func.append(x)

    # Clean and reverse the path for proper ordering
    parent_func = [i for i in parent_func if(len(str(i)) != 0)]
    parent_func.reverse()

    # Mark function as not used (0) in flag dictionary
    flag[".".join(parent_func)] = 0
    
    return node


def pre_class_transform(node: astroid.ClassDef):
    """
    First-pass transformation for classes
    Similar to pre_function_transform but for class definitions
    
    Args:
        node: Class definition node
    Returns:
        The original node
    """
    if (T == 1): return node
    body = []
    
    # Build class path by traversing parent hierarchy
    newnode = node
    parent_func = [node.name]
    while newnode.parent:
        if newnode.parent.__class__ == astroid.FunctionDef or newnode.parent.__class__ == astroid.ClassDef:
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
        else:
            newnode = newnode.parent
            continue

    # Extract path components from file path
    road = handle_file.split("/")

    str_name = road.pop().split(".")
    parent_func.append(str_name[0])

    while len(road) > 0:
        x = road.pop()
        if x == sta_file:
            break
        parent_func.append(x)

    # Clean and reverse the path for proper ordering
    parent_func = [i for i in parent_func if(len(str(i)) != 0)]
    parent_func.reverse()

    # Mark class as not used (0) in flag dictionary
    flag[".".join(parent_func)] = 0
    
    return node


def function_transform(node: astroid.FunctionDef):
    """
    Main transformation for functions in second pass
    Identifies unused functions and transforms them to template calls
    
    Args:
        node: Function definition node
    Returns:
        Transformed node or original node
    """
    body = []

    # Build function path with parent hierarchy information
    newnode = node
    
    parent_func = [node.name]
    
    # Track parent information
    parent_flag = 0  # Number of parent levels
    parent_type = ["only_function"]  # Type of each parent
    while newnode.parent:
        
        if newnode.parent.__class__ == astroid.FunctionDef:
            # Parent is a function
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
            parent_flag = parent_flag + 1
            parent_type.append("parent_function")
        elif newnode.parent.__class__ == astroid.ClassDef:
            # Parent is a class
            parent_func.append(newnode.parent.name)
            newnode = newnode.parent
            parent_flag = parent_flag + 1
            parent_type.append("parent_class")
        else:
            # Other parent types
            newnode = newnode.parent
            continue

    # Extract path components from file path
    road = handle_file.split("/")

    # Get file name without extension
    str_name = road.pop().split(".")

    parent_func.append(str_name[0])

    # Add directories up to the starting directory
    while len(road) > 0:
        x = road.pop()
        if x == sta_file:
            break
        parent_func.append(x)

    # Clean and reverse the path for proper ordering
    parent_func = [i for i in parent_func if(len(str(i)) != 0)]
    parent_func.reverse()
    
    # Check for property decorator
    decorator_property_flag = 0
    if node.decorators:
        print(node.decorators)
        for k in node.decorators.nodes:
            if (k.__class__ == astroid.Name) and (k.name == "property"):
                decorator_property_flag = decorator_property_flag + 1
                print(k.name)

    # Determine if this function should be transformed
    # Conditions: It's unused, not a property, not __init__, and either top-level or parent used
    if (".".join(parent_func) in flag.keys()) and (flag[".".join(parent_func)] == 0) and (decorator_property_flag == 0) and (node.name != '__init__'):
        # Check parent relationship conditions
        if (len(parent_func) > 1 and parent_flag > 0 and (flag[".".join(parent_func[:-1])] == 1) and parent_type[1] == "parent_function") or (parent_flag == 0):
            # Count lines of code
            num = 0
            for i in node.body:
                num = num + len(i.as_string().split('\n'))
    
            print('code num')
            print(num)
            
            # Only transform functions with more than 2 lines
            if num > 2:
                unused_file_name = ".".join(parent_func)
                print('............')
                tempnode = node
                
                # Store the function in pickle_dict for later extraction
                pickle_dict[unused_file_name] = tempnode.as_string()
        
                print('............')
                
                # Rewrite the node to call the template instead
                node_re = rewrite_node(node, unused_file_name)

                print('............')
        
                return node_re

    # Return original node if not transformed
    return node


def rewrite_node(node: astroid.FunctionDef, unused_file_name):
    """
    Rewrites a function node to call template function instead
    
    Args:
        node: Function definition node to rewrite
        unused_file_name: Name to identify the unused function
    Returns:
        Transformed node
    """
    # Collect arguments and dependencies
    argskey_temp = []

    decorator_info.clear()

    # Process decorators
    if node.decorators:
        print("you------")
        for i in node.decorators.nodes:
            node_tmp = parse(i.as_string())

    argskey_temp.extend(decorator_info)    
    decorator_info.clear()
        
    # Process function arguments
    if node.args.__class__ == astroid.Arguments:
        if node.args.args:
            for i in node.args.args:
                argskey_temp.append(i.name)
        for j in node.args.kwonlyargs:
            argskey_temp.append(j.name)
        for k in node.args.defaults:
            if isinstance(k, astroid.Name):
                argskey_temp.append(k.name)
        if node.args.vararg:
            argskey_temp.append(node.args.vararg)
        if node.args.kwarg:
            argskey_temp.append(node.args.kwarg)
 
    # Clear tracking lists before analyzing the function body
    var_save.clear()
    import_save.clear()
    functiondef_save.clear()
    classdef_save.clear()
    func_para_save.clear()
    assignname_save.clear()
    returnnum_save.clear()

    # Parse body to collect variables and dependencies
    for i in node.body:
        node_tmp = parse(i.as_string())
        
    # Find variables that are not arguments, imports, or other defined items
    new_add = []
    for i in var_save:
        if i not in argskey_temp:
            if i not in import_save:
                if i not in functiondef_save:
                    if i not in builtin_global:
                        if i not in assignname_save:
                            if i not in func_para_save:
                                if i not in classdef_save:
                                    new_add.append(i)

    # Store global variables needed by the function
    varible_globals = []
    varible_globals.extend(new_add)
     
    # Add arguments to the variable list
    new_add.extend(argskey_temp)
        
    # Track return value count
    return_num = 0
    if len(returnnum_save) > 0:
        return_num = returnnum_save[0]

    # Clear tracking lists
    argskey_temp.clear()
    var_save.clear()
    import_save.clear()
    functiondef_save.clear()
    classdef_save.clear()
    func_para_save.clear()
    assignname_save.clear()
    returnnum_save.clear()

    # Prepare new body
    newbody = []

    # Process function signature to preserve type annotations
    doc_info = node.doc
    new_node = node
    new_node.body = []
    new_node.doc = ''

    # Process argument annotations
    newannotation = []
    if new_node.args.__class__ == astroid.Arguments:
        newannotation = new_node.args.annotations
        for i in newannotation:
            if i != None:
                print("--------")
                print(i)
                print(i.get_children())
                for k in i.get_children():
                    if k.__class__ == astroid.Name:
                        print(k.name)
                        new_add.append(k.name)
                    if k.get_children():
                        for kk in k.get_children():
                            if kk.__class__ == astroid.Name:
                                print("0")  
                                print(kk.name) 
                                new_add.append(kk.name)
                
        temp_newannotation = newannotation.copy()     
        new_node.args.annotations = newannotation.clear()
        
    # Process return type annotation
    if new_node.returns != None:
        if new_node.returns.get_children():
            for mm in new_node.returns.get_children():
                if mm.__class__ == astroid.Name:
                    print("19999")
                    print(mm.name) 
                    new_add.append(mm.name)
                if mm.get_children():
                    for kk in mm.get_children():
                        if kk.__class__ == astroid.Name:
                            print("199991")  
                            print(kk.name) 
                            new_add.append(kk.name)

    # Temporarily remove return annotation
    temp_return = new_node.returns
    new_node.returns = None

    # Extract function signature as string
    funccall_string = new_node.as_string().strip()
    
    # Extract only the function declaration line
    funccalls = funccall_string.split('\n')
    if len(funccalls) > 1:
        for i in funccalls:
            if "def " in i:
                funccall_string = i
        
    # Clean up the function signature string
    funccall_string = funccall_string[4:]  # Remove 'def '
    funccall_string = funccall_string[:-1]  # Remove trailing colon
    
    funccall_string = funccall_string.replace(' *,', '')
    
    # Format for use as docstring
    funccall_string = "\"\"\"{}\"\"\"".format(funccall_string)

    # Restore annotations
    new_node.args.annotations = temp_newannotation
    new_node.returns = temp_return
  
    # Restore docstring
    node.doc = doc_info
    
    # Create new body with template import
    newcontent = '''
    import custom_funtemplate
    '''
    newbody.append(code2node(newcontent))

    # Build variable dictionary for template call
    inputvar = '{' +'}'
    if len(new_add) > 0:
        inputvar = '{'
        for i in new_add:
            inputvar = inputvar + "\'{}\': {},".format(i, i)
        inputvar = inputvar[:-1] + '}'
   
    # Create template call with or without return
    if return_num > 0:
        print(return_num)
        newcontent = '''
        return custom_funtemplate.rewrite_template('{}', {}, {}, {})
        '''.format(unused_file_name, funccall_string, inputvar, return_num)
        newbody.append(code2node(newcontent))
    else:
        newcontent = '''
        custom_funtemplate.rewrite_template('{}', {}, {}, {})
        '''.format(unused_file_name, funccall_string, inputvar, return_num)
        newbody.append(code2node(newcontent))

    # Replace original body with new template call
    node.body = newbody

    return node


def find_Return(node: astroid.Return):
    """
    Analyze return statements to count return values
    
    Args:
        node: Return node from AST
    """
    if node.value.__class__ == astroid.Tuple:
        if len(node.value.elts) not in returnnum_save:
            returnnum_save.append(len(node.value.elts))
    else:
        if 1 not in returnnum_save:
            returnnum_save.append(1)


def find_AssignName(node: astroid.AssignName):
    """
    Track assigned variable names
    
    Args:
        node: AssignName node from AST
    """
    if node.name not in assignname_save:
        assignname_save.append(node.name)


def find_ClaDef(node: astroid.ClassDef):
    """
    Track class definitions
    
    Args:
        node: ClassDef node from AST
    """
    if node.name not in classdef_save:
        classdef_save.append(node.name)


def find_FuncDef(node: astroid.FunctionDef):
    """
    Track function definitions and their parameters
    
    Args:
        node: FunctionDef node from AST
    """
    if node.name not in functiondef_save:
        functiondef_save.append(node.name)
    
    # Collect function parameters
    if node.args.__class__ == astroid.Arguments:
        if node.args.args:
            for i in node.args.args:
                if i.name not in func_para_save:
                    func_para_save.append(i.name)
        for j in node.args.kwonlyargs:
            if j.name not in func_para_save:
                func_para_save.append(j.name)
        for k in node.args.defaults:
            if isinstance(k, astroid.Name):
                func_para_save.append(k.name)
        if node.args.vararg:
            if node.args.vararg not in func_para_save:
                func_para_save.append(node.args.vararg)
        if node.args.kwarg:
            if node.args.kwarg not in func_para_save:
                func_para_save.append(node.args.kwarg)


def find_Import(node: astroid.Import):
    """
    Track imported names
    
    Args:
        node: Import node from AST
    """
    for i in node.names:
        if i[1] is None:
            if i[0] not in import_save:
                import_save.append(i[0])
        else:
            if i[1] not in import_save:
                import_save.append(i[1])


def find_ImportFrom(node: astroid.ImportFrom):
    """
    Track names imported from modules
    
    Args:
        node: ImportFrom node from AST
    """
    for i in node.names:
        if i[1] is None:
            if i[0] not in import_save:
                import_save.append(i[0])
        else:
            if i[1] not in import_save:
                import_save.append(i[1])


def find_Name(node: astroid.Name):
    """
    Track variable names and decorator names
    
    Args:
        node: Name node from AST
    """
    if node.name not in var_save:
        var_save.append(node.name)
    if node.name not in decorator_info:
        decorator_info.append(node.name)


def read_built(inputfile):
    """
    Read built-in function names from file
    
    Args:
        inputfile: Path to file with built-in names
    Returns:
        List of built-in function names
    """
    built_list = []
    file = open(inputfile) 
    for line in file:
       built_list.append(line.strip('\n'))
    file.close()
    return built_list


if __name__ == "__main__": 
    """
    Main execution flow of the program
    """
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
        "--usedfuntionlist",
        default=""
    )
    parser.add_argument(
        "--unused_gzip_dir",
        default=""
    )
    parser.add_argument(
        "--builtlist",
        default=""
    )
    args = parser.parse_args()
    sta_file = args.dirname
    path = args.path
    used_functionlist = args.usedfuntionlist
    unused_gzip_dir = args.unused_gzip_dir
    buits_list_file = args.builtlist

    # Read built-in function names
    builtin_global = read_built(buits_list_file)

    # Register AST transforms for first pass
    astroid.MANAGER.register_transform(
        astroid.nodes.FunctionDef,
        pre_function_transform,
    )
    astroid.MANAGER.register_transform(
        astroid.nodes.ClassDef,
        pre_class_transform,
    )

    # First pass: Identify all functions and classes
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = "" + os.path.join(root, name)
                with open(handle_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                f.close()
                tree = parse(content)
                w = open(handle_file, 'w', encoding='utf-8')
                w.write(tree.as_string())
                w.close()
  
    # Read list of used functions
    with open(used_functionlist, "r", encoding="utf-8") as f:
        content = f.read()
    
    list_name = content.split("\n")
    if len(list_name) > 0:
        for i in list_name:
            flag[i] = 1

    # Set flag for second pass
    T = 1

    # Register AST transforms for second pass
    astroid.MANAGER.register_transform(
        astroid.nodes.FunctionDef,
        function_transform,
    )
    astroid.MANAGER.register_transform(astroid.Name, find_Name)
    astroid.MANAGER.register_transform(astroid.ImportFrom, find_ImportFrom)
    astroid.MANAGER.register_transform(astroid.Import, find_Import)
    astroid.MANAGER.register_transform(astroid.FunctionDef, find_FuncDef)
    astroid.MANAGER.register_transform(astroid.ClassDef, find_ClaDef)
    astroid.MANAGER.register_transform(astroid.AssignName, find_AssignName)
    astroid.MANAGER.register_transform(astroid.Return, find_Return)
      
    # Second pass: Transform unused functions
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                print(os.path.join(root, name))
                handle_file = "" + os.path.join(root, name)
                
                with open(handle_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                f.close()
                tree = parse(content)
                w = open(handle_file, 'w', encoding='utf-8')
                w.write(tree.as_string())
                
                w.close()
    
    # Save unused functions to compressed file
    import gzip
    with gzip.open(unused_gzip_dir, 'w') as fout:
        fout.write(json.dumps(pickle_dict).encode('utf-8'))
    fout.close()