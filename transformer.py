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

def transform(ast):
    code = []
    for node in ast:
        if node.__class__.__name__ == 'VarNode':
            code.append(f"{node.name} = {expr_to_str(node.value)}")
        elif node.__class__.__name__ == 'PrintNode':
            code.append(f"print({expr_to_str(node.value)})")
        elif node.__class__.__name__ == 'IfNode':
            code.append(f"if {node.cond}:")
            for s in node.body:
                if s.__class__.__name__ == 'PrintNode':
                    code.append(f"    print({expr_to_str(s.value)})")
                elif s.__class__.__name__ == 'VarNode':
                    code.append(f"    {s.name} = {expr_to_str(s.value)}")
            if node.else_body:
                code.append("else:")
                for s in node.else_body:
                    if s.__class__.__name__ == 'PrintNode':
                        code.append(f"    print({expr_to_str(s.value)})")
        elif node.__class__.__name__ == 'WhileNode':
            code.append(f"while {node.cond}:")
            for s in node.body:
                if s.__class__.__name__ == 'PrintNode':
                    code.append(f"    print({expr_to_str(s.value)})")
                elif s.__class__.__name__ == 'VarNode':
                    code.append(f"    {s.name} = {expr_to_str(s.value)}")
        elif node.__class__.__name__ == 'FuncNode':
            params = ', '.join(node.params)
            code.append(f"def {node.name}({params}):")  # no leading space
            for s in node.body:
                if s.__class__.__name__ == 'PrintNode':
                    code.append(f"    print({expr_to_str(s.value)})")
                elif s.__class__.__name__ == 'VarNode':
                    code.append(f"    {s.name} = {expr_to_str(s.value)}")
                elif s.__class__.__name__ == 'ReturnNode':
                    code.append(f"    return {expr_to_str(s.value)}")
                elif s.__class__.__name__ == 'CallNode':
                    code.append(f"    {expr_to_str(s)}")
                elif s.__class__.__name__ == 'IfNode':
                    code.append(f"    if {s.cond}:")
                    for s2 in s.body:
                        if s2.__class__.__name__ == 'PrintNode':
                            code.append(f"        print({expr_to_str(s2.value)})")
                    if s.else_body:
                        code.append("    else:")
                        for s2 in s.else_body:
                            if s2.__class__.__name__ == 'PrintNode':
                                code.append(f"        print({expr_to_str(s2.value)})")
            code.append("")
        elif node.__class__.__name__ == 'CallNode':
            code.append(expr_to_str(node))
    return '\n'.join(code)