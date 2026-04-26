def expr_to_str(expr):
    if hasattr(expr, '__class__'):
        if expr.__class__.__name__ == 'BinOpNode':
            left = expr_to_str(expr.left) if hasattr(expr.left, '__class__') else str(expr.left)
            right = expr_to_str(expr.right) if hasattr(expr.right, '__class__') else str(expr.right)
            return f"{left} {expr.op} {right}"
        elif expr.__class__.__name__ == 'CallNode':
            args = ', '.join(expr_to_str(a) for a in expr.args)
            return f"{expr.name}({args})"
    return str(expr)

def transform_stmts(stmts, indent=4):
    """যেকোনো statement list কে দেওয়া indent দিয়ে Python code এ রূপান্তর করে।"""
    pad = ' ' * indent
    code = []
    for s in stmts:
        name = s.__class__.__name__
        if name == 'PrintNode':
            code.append(f"{pad}print({expr_to_str(s.value)})")
        elif name == 'VarNode':
            code.append(f"{pad}{s.name} = {expr_to_str(s.value)}")
        elif name == 'ReturnNode':
            code.append(f"{pad}return {expr_to_str(s.value)}")
        elif name == 'CallNode':
            code.append(f"{pad}{expr_to_str(s)}")
        elif name == 'IfNode':
            code.append(f"{pad}if {s.cond}:")
            code.extend(transform_stmts(s.body, indent + 4))
            # nested elif branches
            for (elif_cond, elif_body) in s.elif_branches:
                code.append(f"{pad}elif {elif_cond}:")
                code.extend(transform_stmts(elif_body, indent + 4))
            if s.else_body:
                code.append(f"{pad}else:")
                code.extend(transform_stmts(s.else_body, indent + 4))
        elif name == 'WhileNode':
            code.append(f"{pad}while {s.cond}:")
            code.extend(transform_stmts(s.body, indent + 4))
    return code

def transform(ast):
    code = []
    for node in ast:
        name = node.__class__.__name__
        if name == 'VarNode':
            code.append(f"{node.name} = {expr_to_str(node.value)}")
        elif name == 'PrintNode':
            code.append(f"print({expr_to_str(node.value)})")
        elif name == 'IfNode':
            code.append(f"if {node.cond}:")
            code.extend(transform_stmts(node.body))
            # ── elif branches (nahole jodi) ──
            for (elif_cond, elif_body) in node.elif_branches:
                code.append(f"elif {elif_cond}:")
                code.extend(transform_stmts(elif_body))
            # ── else branch (nahole) ──
            if node.else_body:
                code.append("else:")
                code.extend(transform_stmts(node.else_body))
        elif name == 'WhileNode':
            code.append(f"while {node.cond}:")
            code.extend(transform_stmts(node.body))
        elif name == 'FuncNode':
            params = ', '.join(node.params)
            code.append(f"def {node.name}({params}):")
            code.extend(transform_stmts(node.body))
            code.append("")
        elif name == 'CallNode':
            code.append(expr_to_str(node))
    return '\n'.join(code)