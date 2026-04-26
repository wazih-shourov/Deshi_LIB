"""
deshilib — একটি বাংলা প্রোগ্রামিং ভাষা যা Python এ compile হয়।

Basic usage:
    import deshilib
    deshilib.run_code("bol 5 + 3")
    deshilib.run_file("আমার_কোড.bd")
"""

from .lexer import tokenize
from .parser import parse
from .transformer import transform

__version__ = "0.1.0"
__author__  = "deshilib"

def run_code(code: str) -> None:
    """
    সরাসরি Bangla source code string নিয়ে execute করে।

    Example:
        import deshilib
        deshilib.run_code(\"\"\"
            rakho x = 10
            jodi x > 5 thole
                bol "baro"
            nahole
                bol "choto"
        \"\"\")
    """
    tokens = tokenize(code)
    ast    = parse(tokens)
    python_code = transform(ast)
    exec(python_code, {})

def run_file(filename: str) -> None:
    """
    .bd ফাইল path নিয়ে সেটা execute করে।

    Example:
        import deshilib
        deshilib.run_file("program.bd")
    """
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    run_code(code)

def to_python(code: str) -> str:
    """
    Bangla source code কে equivalent Python code এ রূপান্তর করে — execute করে না।

    Example:
        import deshilib
        py = deshilib.to_python("bol 5 + 3")
        print(py)  # print(5 + 3)
    """
    tokens = tokenize(code)
    ast    = parse(tokens)
    return transform(ast)