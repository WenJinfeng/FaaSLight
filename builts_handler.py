import ast
def get_ast(input_file):

    with open(input_file,'r',encoding='utf-8') as f:
        content = f.read()
    tree_node = ast.parse(content)
    return tree_node

def get_builtlist(tree_node):
    built_list = []
    
    for node in ast.walk(tree_node):
        if isinstance(node, ast.FunctionDef):
            built_list.append(node.name)
        if isinstance(node, ast.ClassDef):
            built_list.append(node.name)
    built_list = list(set(built_list))
    
    with open('built_list.txt', "w", encoding='utf-8') as f:
        for i in built_list:
            f.write(i)
            f.write('\r\n')
    
    f.close




if __name__ == "__main__":
    find_file = 'builtins.py'
    tree_node = get_ast(find_file)
    get_builtlist(tree_node)
    
