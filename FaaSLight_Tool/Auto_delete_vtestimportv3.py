import os
import json
import astroid
from astroid import parse
import argparse


# Global variables for tracking file paths and states
handle_file = ""  # Current file being processed
flag = {}  # Dictionary to track function/class usage status
sta_file = ""  # Starting directory for the analysis
unused_dir = ""  # Directory for unused functions
jug_module = {}  # Dictionary to identify if import is a module or callable


soimport_name = []  # List to store shared object (.so) file names

# Lists for handling import transformations
import_rewrite = []  # Store import statements to be rewritten
import_rewrite_loc = []  # Store locations of imports to be rewritten
import_flag = []  # Flags to track if import transformation occurred


# Flag to control transformation phases
T = 0  # 0: Pre-processing phase, 1: Transformation phase


# List to store built-in function names
builtin_global = [] 


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
        # Fall back to parsing the entire code if extract_node fails
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


def import_transform(node: astroid.Import):
    """
    Transform regular import statements to lazy imports
    for modules and callables that are not used
    
    Args:
        node: Import node from AST
    Returns:
        Transformed node or empty node if all imports are rewritten
    """
    # Lists to track imports
    import_list = []
    import_rewrite_self = []

    # Build import path information
    newnode = node
    parent_imp = []
    
    # Extract path components from file path
    road = handle_file.split("/")
    str_name = road.pop().split(".")
    
    # Build the parent import path
    while len(road) > 0:
        x = road.pop()
        if x == sta_file:
            break
        parent_imp.append(x)

    parent_imp = [i for i in parent_imp if(len(str(i)) != 0)]
    parent_imp.reverse()

    # Get the file path as a dotted module path
    file_rd = ".".join(parent_imp)
    
    # Process each imported name
    for i in node.names:
        if i[0] != "lazy_import" and i[0] != "custom_funtemplate":
            if i[0] != '*':
                # Check if this import should be transformed to lazy import
                if file_rd != "":
                    # Check if module is unused
                    if (flag.get(file_rd+"."+i[0], 'no') == 0) and (isContainedStr(file_rd+"."+i[0], flag) == "0"):
                        # Check if it's a module or callable
                        if jug_module.get(file_rd+"."+i[0], 'no') == 1:
                            if i[1] == None:
                                # Convert to lazy module import
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[1], i[0]))
                        else:
                            if i[1] == None:
                                # Convert to lazy callable import
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[1], i[0]))
                    else:    
                        # Keep original import
                        import_list.append(i)
                else:
                    # Similar logic for top-level imports
                    if (flag.get(i[0], 'no') == 0 or flag.get(i[0], 'no') == "no") and (isContainedStr(i[0], flag) == "0"):
                        if jug_module.get(i[0], 'no') == 1:
                            if i[1] == None:
                                # Convert to lazy module import
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[1], i[0]))
                        else:
                            if i[1] == None:
                                # Convert to lazy callable import
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[0].split('.')[-1], i[0]))
                            else:
                                import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[1], i[0]))
                    else:    
                        # Keep original import
                        import_list.append(i)
        else:
            # Don't transform lazy_import or custom_funtemplate imports
            return node

    # Handle different parent contexts for import statements
    if isinstance(node.parent, astroid.Module):
        # If parent is a module, store rewrites for later application
        import_rewrite.append(import_rewrite_self)
        loc = 0
        for idx, i in enumerate(node.parent.body):
            if i == node:
                loc = idx
                break
        import_rewrite_loc.append(loc)
    else:
        # If parent is not a module, handle inline
        if len(node.names) == 1 and len(import_rewrite_self) > 0:
            template_import = import_rewrite_self[0]
            import_flag.append("1")
            return code2node(template_import)
        elif len(node.names) > 1 and len(import_rewrite_self) > 0:
            # Store for later processing
            import_rewrite.append(import_rewrite_self)
            loc = 0
            tempnode = node
            while tempnode.parent:
                if isinstance(tempnode.parent, astroid.Module):
                    for idx, i in enumerate(tempnode.parent.body):
                        if i == tempnode:
                            loc = idx
                            tempnode = tempnode.parent
                            break
                else:
                    tempnode = tempnode.parent
            import_rewrite_loc.append(loc)

    # If all imports were transformed, return empty node
    if (len(import_list) == 0):
        return code2node("()")

    # Update the import names list
    node.names = import_list
    
    return node


def importfrom_transform(node: astroid.ImportFrom):
    """
    Transform 'from ... import ...' statements to lazy imports
    for modules and callables that are not used
    
    Args:
        node: ImportFrom node from AST
    Returns:
        Transformed node or empty node if all imports are rewritten
    """
    # Get the module name being imported from
    module_name = node.modname

    import_rewrite_self = []
    import_list = []

    # Build import path information
    node_temp = node
    parent_imp = []
    
    # Extract path components from file path
    road = handle_file.split("/")
    str_name = road.pop().split(".")
    
    # Build the parent import path
    while len(road) > 0:
        x = road.pop()
        if x == sta_file:
            break
        parent_imp.append(x)

    parent_imp = [i for i in parent_imp if(len(str(i)) != 0)]
    parent_imp.reverse()

    # Skip processing for .so module imports
    if module_name in soimport_name:
        return node

    # Handle relative imports
    if node.level == None:
        parent_imp = module_name.split(".")
    else:
        # For relative imports, adjust the parent path
        if len(parent_imp) > 0:
            for i in range(1, node.level):
                parent_imp.pop()
            parent_imp.append(module_name)
            parent_imp = [i for i in parent_imp if(len(str(i)) != 0)]
        
    # Get the full module path
    file_rd = ".".join(parent_imp)
    
    # Process each imported name
    for i in node.names:
        if i[0] == '*':
            # Keep wildcard imports as is
            import_list.append(i)
    
        if i[0] != '*':
            # Check if this import should be transformed to lazy import
            if (flag.get(file_rd+"."+i[0], 'no') == 0) and (isContainedStr(file_rd+"."+i[0], flag) == "0"):
                # Build the full import path
                valuetemp = file_rd+"."+i[0]
                valuetemp = valuetemp.split(".")
                if i[1] == None:
                    # For imports without aliases
                    if (flag.get(file_rd, 'no') != 1):
                        if (jug_module.get('.'.join(valuetemp), 'no') == 1):
                            # Convert to lazy module import
                            import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(valuetemp[-1], ".".join(valuetemp)))
                        else:
                            # Convert to lazy callable import
                            import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(valuetemp[-1], ".".join(valuetemp)))
                    else:
                        # Keep original import
                        import_list.append(i)
                else:
                    # For imports with aliases
                    if (flag.get(file_rd, 'no') != 1):
                        if jug_module.get('.'.join(valuetemp), 'no') == 1:
                            # Convert to lazy module import
                            import_rewrite_self.append("{} = lazy_import.lazy_module('{}')".format(i[1], ".".join(valuetemp)))
                        else:
                            # Convert to lazy callable import
                            import_rewrite_self.append("{} = lazy_import.lazy_callable('{}')".format(i[1], ".".join(valuetemp)))
                    else:
                        # Keep original import
                        import_list.append(i)
            else:    
                # Keep original import
                import_list.append(i)

    # Handle different parent contexts for import statements
    if isinstance(node.parent, astroid.Module):
        # If parent is a module, store rewrites for later application
        import_rewrite.append(import_rewrite_self)
        loc = 0
        for idx, i in enumerate(node.parent.body):
            if i == node:
                loc = idx
                break
        import_rewrite_loc.append(loc)
    else:
        # If parent is not a module, handle inline
        if len(node.names) == 1 and len(import_rewrite_self) > 0:
            template_import = import_rewrite_self[0]
            import_flag.append("1")
            return code2node(template_import)
        elif len(node.names) > 1 and len(import_rewrite_self) > 0:
            # Store for later processing
            import_rewrite.append(import_rewrite_self)
            loc = 0
            tempnode = node
            while tempnode.parent:
                if isinstance(tempnode.parent, astroid.Module):
                    for idx, i in enumerate(tempnode.parent.body):
                        if i == tempnode:
                            loc = idx
                            tempnode = tempnode.parent
                            break
                else:
                    tempnode = tempnode.parent
            import_rewrite_loc.append(loc)

    # If all imports were transformed, return empty node
    if (len(import_list) == 0):
        return code2node("()")

    # Update the import names list
    node.names = import_list
    
    return node


def isContainedStr(importstr, flag):
    """
    Check if an import string is contained in any used function/class path
    
    Args:
        importstr: Import string to check
        flag: Dictionary of function/class usage status
    Returns:
        "1" if the import is used somewhere, "0" otherwise
    """
    for key_i in flag.keys():
        if (importstr in key_i) and (flag[key_i] == 1):
            return "1"
    return "0"


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

def get_sofile(path):
    """
    Find all shared object (.so) files in the given path
    
    Args:
        path: Directory path to search
    Returns:
        List of .so file names without extension
    """
    so_name = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.so'):
                so_name.append(name.split(".")[0])
    return so_name


if __name__ == "__main__": 
    """
    Main execution flow of the program:
    1. Parse command line arguments
    2. Collect function/class information in first pass
    3. Mark used functions/classes
    4. Transform imports to lazy imports in second pass
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
        "--builtlist",
        default=""
    )
    parser.add_argument(
        "--module_name",
        default=""
    )
    args = parser.parse_args()
    sta_file = args.dirname
    path = args.path
    used_functionlist = args.usedfuntionlist
    buits_list_file = args.builtlist
    module_name = args.module_name

    # Read built-in function names and .so files
    builtin_global = read_built(buits_list_file)
    soimport_name = get_sofile(path)

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

    # Read list of module names
    with open(module_name, "r", encoding="utf-8") as f:
        content = f.read()

    list_name = content.split("\n")
    if len(list_name) > 0:
        for i in list_name:
            jug_module[i] = 1

    # Set flag for second pass
    T = 1
    
    # Register AST transforms for second pass
    astroid.MANAGER.register_transform(
        astroid.nodes.ImportFrom,
        importfrom_transform,
    )
    astroid.MANAGER.register_transform(
        astroid.nodes.Import,
        import_transform,
    )

    # Second pass: Transform imports
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.py'):
                handle_file = "" + os.path.join(root, name)
                print(handle_file)
                import_rewrite = []
                import_rewrite_loc = []
                import_flag = []
                
                with open(handle_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = parse(content)

                # Apply collected import rewrites
                if len(import_rewrite) > 0:
                    for idx, import_rewrite_i in enumerate(import_rewrite):
                        import_rewrite_i_temp = list(set(import_rewrite_i))
                        if len(import_rewrite_i_temp) > 0:
                            # Get location to insert rewrites
                            loc = import_rewrite_loc[idx]
                            
                            # Create new body with space for rewrites
                            num = len(import_rewrite_i_temp)
                            new_tree = [] 
                            for k in range(0, len(tree.body) + num):
                                new_tree.append("temp")

                            # Copy existing nodes and make space for new imports
                            for i in range(0, len(tree.body)):
                                if i <= loc:
                                    new_tree[i] = tree.body[i]
                                elif i > loc:
                                    new_tree[i + num] = tree.body[i]
                
                            # Insert new import statements
                            for id_re, re in enumerate(import_rewrite_i_temp):
                                template_import = '''
                                {}
                                '''.format(re)
                                print("rewrite：" + re)
                                new_tree[loc + id_re + 1] = code2node(template_import)

                            # Update locations for subsequent rewrites
                            import_rewrite_loc = [h + num for h in import_rewrite_loc]

                            # Update tree body
                            tree.body = new_tree
                            import_flag.append("1")

                # Add lazy_import import if any transformations were made
                if "1" in import_flag:
                    # Special handling for __future__ imports
                    if isinstance(tree.body[0], astroid.ImportFrom):
                        count = 0
                        C = 0
                        while (isinstance(tree.body[count], astroid.ImportFrom)) and (tree.body[count].modname == "__future__"):
                            C = C + 1
                            count = count + 1
                        if C > 0:
                            # Insert after all __future__ imports
                            treetmp = []
                            for k in range(0, len(tree.body) + 1):
                                treetmp.append("temp")
                            for i in range(0, len(tree.body)):
                                if i <= (C - 1):
                                    treetmp[i] = tree.body[i]
                                elif i > (C - 1):
                                    treetmp[i + 1] = tree.body[i]
                            treetmp[C] = code2node("import lazy_import")
                            tree.body = treetmp
                        else:
                            tree.body.insert(0, code2node("import lazy_import"))
                    else:
                        # Insert at the beginning
                        tree.body.insert(0, code2node("import lazy_import"))

                # Reset lists for next file
                import_rewrite = []
                import_rewrite_loc = []
                import_flag = []

                # Write transformed code back to file
                w = open(handle_file, 'w', encoding='utf-8')