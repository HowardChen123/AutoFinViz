import re
import ast
import importlib
import matplotlib.pyplot as plt
import pandas as pd

def preprocess_code(code: str) -> str:
    """Preprocess code to remove any preamble and explanation text"""

    code = code.replace("<imports>", "")
    code = code.replace("<stub>", "")
    code = code.replace("<transforms>", "")

    # remove all text after chart = plot(df)
    if "fig = plot(df)" in code:
        # print(code)
        index = code.find("fig = plot(df)")
        if index != -1:
            code = code[: index + len("fig = plot(df)")]

    if "```" in code:
        pattern = r"```(?:\w+\n)?([\s\S]+?)```"
        matches = re.findall(pattern, code)
        if matches:
            code = matches[0]

    if "import" in code:
        # return only text after the first import statement
        index = code.find("import")
        if index != -1:
            code = code[index:]

    code = code.replace("```", "")
    if "fig = plot(df)" not in code:
        code = code + "\fig = plot(df)"
    return code

def get_globals_dict(code_string, df):
    # Parse the code string into an AST
    tree = ast.parse(code_string)
    # Extract the names of the imported modules and their aliases
    imported_modules = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = importlib.import_module(alias.name)
                imported_modules.append((alias.name, alias.asname, module))
        elif isinstance(node, ast.ImportFrom):
            module = importlib.import_module(node.module)
            for alias in node.names:
                obj = getattr(module, alias.name)
                imported_modules.append(
                    (f"{node.module}.{alias.name}", alias.asname, obj)
                )

    # Import the required modules into a dictionary
    globals_dict = {}
    for module_name, alias, obj in imported_modules:
        if alias:
            globals_dict[alias] = obj
        else:
            globals_dict[module_name.split(".")[-1]] = obj

    ex_dicts = {"pd": pd, "df": df, "plt": plt}
    globals_dict.update(ex_dicts)
    return globals_dict

# Function to convert JSON to a readable string format
def json_to_readable(data, indent=0):
    readable_str = ""
    indent_str = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            readable_str += f"{indent_str}{key}: "
            if isinstance(value, (dict, list)):
                readable_str += "\n" + json_to_readable(value, indent + 1)
            else:
                readable_str += f"{value}\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                readable_str += json_to_readable(item, indent + 1) + "\n"
            else:
                readable_str += f"{indent_str}- {item}\n"
    else:
        readable_str += f"{indent_str}{data}\n"

    return readable_str