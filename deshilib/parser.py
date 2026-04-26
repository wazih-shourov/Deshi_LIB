class VarNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PrintNode:
    def __init__(self, value):
        self.value = value

class IfNode:
    def __init__(self, cond, body, elif_branches=None, else_body=None):
        self.cond = cond
        self.body = body
        self.elif_branches = elif_branches or []  # (cond, body) tuples
        self.else_body = else_body

class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class FuncNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnNode:
    def __init__(self, value):
        self.value = value

# -------- এক্সপ্রেশন পার্সার ----------
def parse_primary(tokens, pos, end):
    if pos >= end:
        return None, pos
    t = tokens[pos]
    if t.type == 'NUMBER':
        return t.value, pos+1
    if t.type == 'STRING':
        return f'"{t.value}"', pos+1
    if t.type == 'NAME':
        # ফাংশন কল চেক
        if pos+1 < end and tokens[pos+1].type == 'OPERATOR' and tokens[pos+1].value == '(':
            func_name = t.value
            pos += 2  # '(' এর পর
            args = []
            while pos < end and not (tokens[pos].type == 'OPERATOR' and tokens[pos].value == ')'):
                arg, pos = parse_binop(tokens, pos, end)
                args.append(arg)
                if pos < end and tokens[pos].type == 'OPERATOR' and tokens[pos].value == ',':
                    pos += 1
            if pos < end and tokens[pos].type == 'OPERATOR' and tokens[pos].value == ')':
                pos += 1
            return CallNode(func_name, args), pos
        else:
            return t.value, pos+1
    return None, pos

def parse_binop(tokens, pos, end):
    left, pos = parse_primary(tokens, pos, end)
    if pos < end and tokens[pos].type == 'OPERATOR' and tokens[pos].value in ('+','-','*','/','>','<','>=','<='):
        op = tokens[pos].value
        pos += 1
        right, pos = parse_binop(tokens, pos, end)
        return BinOpNode(left, op, right), pos
    return left, pos

# -------- স্টেটমেন্ট ও ব্লক পার্সার ----------
def parse_stmt(tokens, i, n):
    if i >= n:
        return None, i
    t = tokens[i]
    if t.type == 'KEYWORD' and t.value == 'bol':
        expr, next_i = parse_binop(tokens, i+1, n)
        return PrintNode(expr), next_i
    elif t.type == 'KEYWORD' and t.value == 'rakho':
        if i+2 >= n or tokens[i+2].type != 'OPERATOR' or tokens[i+2].value != '=':
            return None, i+1
        name = tokens[i+1].value
        expr, next_i = parse_binop(tokens, i+3, n)
        return VarNode(name, expr), next_i
    elif t.type == 'KEYWORD' and t.value == 'ferot' and i+1 < n and tokens[i+1].type == 'KEYWORD' and tokens[i+1].value == 'de':
        expr, next_i = parse_binop(tokens, i+2, n)
        return ReturnNode(expr), next_i
    elif t.type == 'KEYWORD' and t.value == 'dhori':
        if i+1 >= n or tokens[i+1].type != 'NAME':
            return None, i+1
        func_name = tokens[i+1].value
        pos = i+2
        if pos >= n or tokens[pos].type != 'OPERATOR' or tokens[pos].value != '(':
            return None, pos
        pos += 1
        params = []
        while pos < n and not (tokens[pos].type == 'OPERATOR' and tokens[pos].value == ')'):
            if tokens[pos].type == 'NAME':
                params.append(tokens[pos].value)
                pos += 1
                if pos < n and tokens[pos].type == 'OPERATOR' and tokens[pos].value == ',':
                    pos += 1
            else:
                pos += 1
        if pos < n and tokens[pos].type == 'OPERATOR' and tokens[pos].value == ')':
            pos += 1
        body, next_i = parse_block(tokens, pos, n)
        return FuncNode(func_name, params, body), next_i
    else:
        return None, i+1

def parse_block(tokens, i, n):
    stmts = []
    if i >= n or tokens[i].type != 'INDENT':
        return stmts, i
    block_indent = tokens[i].value
    i += 1
    while i < n:
        stmt, i = parse_stmt(tokens, i, n)
        if stmt:
            stmts.append(stmt)
        if i < n and tokens[i].type == 'INDENT':
            if tokens[i].value == block_indent:
                i += 1
                continue
            else:
                break
        else:
            break
    return stmts, i

def parse(tokens):
    ast = []
    i = 0
    n = len(tokens)
    while i < n:
        t = tokens[i]
        if t.type == 'KEYWORD' and t.value in ('rakho', 'bol', 'dhori'):
            stmt, i = parse_stmt(tokens, i, n)
            if stmt:
                ast.append(stmt)
            continue
        elif t.type == 'KEYWORD' and t.value == 'jodi':
            # jodi condition thole
            j = i+1
            cond_parts = []
            while j < n and not (tokens[j].type == 'KEYWORD' and tokens[j].value == 'thole'):
                cond_parts.append(str(tokens[j].value))
                j += 1
            cond = ' '.join(cond_parts)
            i = j+1
            body, i = parse_block(tokens, i, n)

            # এলিফ ও এলস ব্রাঞ্চ পার্স
            elif_branches = []
            else_body = []

            while i < n and tokens[i].type == 'KEYWORD' and tokens[i].value == 'nahole':
                i += 1
                # nahole এর পরে jodi থাকলে → elif
                if i < n and tokens[i].type == 'KEYWORD' and tokens[i].value == 'jodi':
                    i += 1
                    k = i
                    cond_parts = []
                    while k < n and not (tokens[k].type == 'KEYWORD' and tokens[k].value == 'thole'):
                        cond_parts.append(str(tokens[k].value))
                        k += 1
                    elif_cond = ' '.join(cond_parts)
                    i = k+1
                    elif_body, i = parse_block(tokens, i, n)
                    elif_branches.append((elif_cond, elif_body))
                else:
                    # শুধু nahole → else
                    else_body, i = parse_block(tokens, i, n)
                    break

            ast.append(IfNode(cond, body, elif_branches, else_body))
        elif t.type == 'KEYWORD' and t.value == 'jotokhon':
            j = i+1
            cond_parts = []
            while j < n and not (tokens[j].type == 'KEYWORD' and tokens[j].value == 'thole'):
                cond_parts.append(str(tokens[j].value))
                j += 1
            cond = ' '.join(cond_parts)
            i = j+1
            body, i = parse_block(tokens, i, n)
            ast.append(WhileNode(cond, body))
        elif t.type == 'NAME':
            # standalone function call: name(args)
            if i+1 < n and tokens[i+1].type == 'OPERATOR' and tokens[i+1].value == '(':
                expr, i = parse_binop(tokens, i, n)
                if expr is not None:
                    ast.append(expr)
            else:
                i += 1
        else:
            i += 1
    return ast