import ast

def list_functions_in_file(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    # Include both regular and async function definitions
    functions = [
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    return functions

# Example usage
file_location = "my_modules/database_code/db_functions.py"
functions = list_functions_in_file(file_location)

print(f"Total functions: {len(functions)}")
print("Function names:")
for func in functions:
    print(f" - {func}")
