import sys
from .lexer import tokenize
from .parser import parse
from .transformer import transform

def run(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = tokenize(code)
    ast = parse(tokens)
    python_code = transform(ast)
    exec(python_code, {})

def cli():
    """Terminal থেকে: deshilib program.bd"""
    if len(sys.argv) < 2:
        print("ব্যবহার: deshilib <filename.bd>")
        sys.exit(1)
    run(sys.argv[1])

if __name__ == '__main__':
    cli()