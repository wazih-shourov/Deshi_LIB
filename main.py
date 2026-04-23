import sys
from lexer import tokenize
from parser import parse
from transformer import transform

def run(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    
    tokens = tokenize(code)
    print("Tokens:", [(t.type, t.value, t.line) for t in tokens])
    
    ast = parse(tokens)
    print("AST:", [(type(n).__name__, n.__dict__) for n in ast])
    
    python_code = transform(ast)
    print(f"\nPython Code:\n{python_code}")
    
    print("\nOutput:")
    exec(python_code)

if __name__ == '__main__':
    run(sys.argv[1])