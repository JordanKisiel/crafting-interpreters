import sys

def main():
    # incorrect number of args
    if len(sys.argv) != 2:
        print("Incorrect number of args. Usage: python3 ast_generator.py <output dest>")
        sys.exit(64)
    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
       "Binary : left, operator, right",
       "Grouping : expression",
       "Literal : value",
       "Unary : operator, right"
    ]) 

def define_ast(output_dir, base_name, types_list):
    path = f"{output_dir}/{base_name.lower()}.py"
    with open(path, 'w') as base_file:
        # Expr base class 
        base_file.writelines([
            "from abc import ABC, abstractmethod\n",
            "\n",
            f"class {base_name}(ABC):\n",
            "    @abstractmethod\n"
            "    def __init__(self):\n",
            "        pass\n",
            "\n",
        ])

        # abstract accept method
        base_file.writelines([
            "    @abstractmethod\n"
            "    def accept(self, visitor):\n",
            "        self.visitor = visitor\n",
            "\n"
        ])

        # write the vistior abstract base class
        abstract_methods = []
        for type in types_list:
            type_name = type.split(":")[0].strip()
            method = f"    def visit_{type_name.lower()}_{base_name.lower()}({base_name.lower()}):\n"
            abstract_methods.append("    @abstractmethod\n")
            abstract_methods.append(method)
            abstract_methods.append("        pass\n")
            abstract_methods.append("\n")


        base_file.writelines([
            "class Visitor(ABC):\n",
            *abstract_methods
        ])

        for type in types_list:
            class_name = type.split(":")[0].strip()
            fields_str = type.split(":")[1].strip()
            define_type(base_file, base_name, class_name, fields_str)


def define_type(file, base_name, class_name, fields_str):
    fields = fields_str.split(", ")
    fields = [f"        self.{field} = {field}\n" for field in fields]
    
    # class declaration and constructor
    file.writelines([
        f"class {class_name}({base_name}):\n",
        f"    def __init__(self, {fields_str}):\n",
        *fields,
        "\n"
    ])

    # sub-class specific accept method
    file.writelines([
        "    def accept(self, visitor):\n",
        f"       return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n",
        "\n"
    ])

main()