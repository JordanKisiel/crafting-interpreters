import sys
from src.Lox_Error import Lox_Error

def main():
    # incorrect number of args
    # must equal 3 because first arg is always the name of this script
    if len(sys.argv) != 3:
        print("Must provide source and destination files. Usage: python3 main.py <lox source> <python dest>")
        sys.exit(64)
    else:
        compile_to_lox(sys.argv[1], sys.argv[2])

def compile_to_lox(source_file, dest_file):
    with open(source_file, 'r') as source:
        source = source.read()
        generated_python = compile_file(source) 
    with open(f"compiled_files/{dest_file}", "w") as dest:
        dest.write(generated_python)

def compile_file(source_file):
    scanner = Scanner(source_file)
    tokens = scanner.scanTokens()

    # don't compile if there are errors
    if Lox_Error.had_error:
        sys.exit(65)

    # for now just print the tokens
    for token in tokens:
        print(token)



if __name__ == "__main__":
    main()