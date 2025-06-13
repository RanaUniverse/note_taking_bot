import ast

def get_function_info(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_type = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
            functions.append({
                "name": node.name,
                "type": func_type,
                "line": node.lineno
            })

    return functions

# Example usage
file_location = "my_modules/database_code/db_functions.py"
function_info = get_function_info(file_location)

print(f"Total functions: {len(function_info)}")
print("Functions:")
for func in function_info:
    print(f" - {func['type']} {func['name']} (line {func['line']})")
