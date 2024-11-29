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
        base_file.writelines([
            f"class {base_name}:\n",
            "   def __init__(self):\n",
            "       pass\n",
            "\n"
        ])

        for type in types_list:
            class_name = type.split(":")[0].strip()
            fields_str = type.split(":")[1].strip()
            define_type(base_file, base_name, class_name, fields_str)

def define_type(file, base_name, class_name, fields_str):
    fields = fields_str.split(", ")
    fields = [f"        self.{field} = {field}\n" for field in fields]
    file.writelines([
        f"class {class_name}({base_name}):\n",
        f"  def __init__(self, {fields_str}):\n",
        *fields,
        "\n"
    ])

main()