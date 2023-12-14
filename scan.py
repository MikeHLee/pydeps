import ast
import os
import pkg_resources
import stdlib_list

STDLIBS = stdlib_list.stdlib_list()

def is_stdlib(module):
    return module in STDLIBS

def get_package_name(module):
    try:
        package = pkg_resources.get_distribution(module)
        return f"{package.key}=={package.version}"
    except Exception as e:
        print(f"Unable to find package details for : {module}")
        return None

def process_file(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    yield alias.name.split('.')[0]
            elif isinstance(node, ast.ImportFrom):
                yield node.module.split('.')[0]

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield from process_file(os.path.join(root, file))

def save_requirements(modules, filename):
    with open(filename, 'w') as f:
        for module in modules:
            if not is_stdlib(module):
                package = get_package_name(module)
                if package:
                    f.write(package+'\n')

def main(directory, requirements_file):
    modules = set(process_directory(directory))
    save_requirements(modules, requirements_file)

if __name__ == "__main__":
    directory = input("Please enter the directory: ")
    requirements_file = input("Please enter the output file name: ")
    main(directory, requirements_file)
