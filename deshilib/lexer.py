import re

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

keywords = {'rakho', 'bol', 'jodi', 'nahole', 'thole', 'jotokhon', 'dhori', 'ferot', 'de'}

def tokenize(code):
    tokens = []
    lines = code.split('\n')
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        
        indent = len(line) - len(line.lstrip())
        if indent > 0:
            tokens.append(Token('INDENT', indent, line_num))
        
        i = 0
        n = len(stripped)
        while i < n:
            ch = stripped[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit():
                j = i
                while j < n and stripped[j].isdigit():
                    j += 1
                tokens.append(Token('NUMBER', int(stripped[i:j]), line_num))
                i = j
                continue
            if ch == '"':
                j = i + 1
                while j < n and stripped[j] != '"':
                    j += 1
                s = stripped[i+1:j]
                tokens.append(Token('STRING', s, line_num))
                i = j + 1
                continue
            if ch.isalpha() or ch == '_':
                j = i
                while j < n and (stripped[j].isalnum() or stripped[j] == '_'):
                    j += 1
                word = stripped[i:j]
                if word in keywords:
                    tokens.append(Token('KEYWORD', word, line_num))
                else:
                    tokens.append(Token('NAME', word, line_num))
                i = j
                continue
            # দুই-অক্ষরের অপারেটর
            if i+1 < n and stripped[i:i+2] in ('>=', '<='):
                tokens.append(Token('OPERATOR', stripped[i:i+2], line_num))
                i += 2
                continue
            if ch in '=+-*/><(),':
                tokens.append(Token('OPERATOR', ch, line_num))
                i += 1
                continue
            raise ValueError(f"Invalid char '{ch}' at line {line_num}")
    return tokens