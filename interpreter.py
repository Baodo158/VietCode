from textx import metamodel_from_file
import sys

#Load grammar file
viet_mm = metamodel_from_file('VietCode.tx')

#Stored variable
s = {}

#Evauluate expressions
def eval_expr(expr):
    if type(expr) in [str, int, float]:
        return eval_term(expr)

    op = getattr(expr, 'op', None)
    if op:
        left = eval_expr(expr.left)
        right = eval_expr(expr.right)

        if op == 'cộng':
            return left + right
        elif op == 'trừ':
            return left - right
        elif op == 'nhân':
            return left * right
        elif op == 'chia':
            return left / right
        elif op == '%':
            return left % right
        elif op == 'lớn hơn':
            return left > right
        elif op == 'bé hơn':
            return left < right
        elif op == 'bằng':
            return left == right
        elif op == 'khác':
            return left != right
        else:
            raise Exception(f"[Lỗi]: Lệnh không hợp lệ: {op}")
    else:
        return eval_term(expr.left)

#Get value of variables,number or string
def eval_term(term):
    if isinstance(term, str):
        if term.startswith('"') and term.endswith('"'):
            return term[1:-1]  
        elif term in s:
            return s[term]
        else:
            return term  
    return term

#Run single statement
def execute_code(stmt):
    stmt_type = stmt.__class__.__name__

    if stmt_type == 'Assignment':
        s[stmt.var] = eval_expr(stmt.value)

    elif stmt_type == 'Print':
        if stmt.msg:
            msg = stmt.msg
            if msg.startswith('"') and msg.endswith('"'):
                msg = msg[1:-1]
            print(msg)
        else:
            val = s.get(stmt.var, None)
            if val is not None:
                print(val)
            else:
                raise Exception(f"[Lỗi]: '{stmt.var}' không tồn tại")

    elif stmt_type == 'MathExpr':
        result = eval_expr(stmt)
        print(result)

    elif stmt_type == 'IfStmt':
        if eval_expr(stmt.condition):
            for s_ in stmt.thenBlock:
                execute_code(s_)
        elif stmt.elseBlock:
            for s_ in stmt.elseBlock:
                execute_code(s_)

    elif stmt_type == 'WhileLoop':
        while eval_expr(stmt.condition):
            for s_ in stmt.body:
                execute_code(s_)

    elif stmt_type == 'Loop':
        start = s.get(stmt.var, 0)
        end = stmt.end
        for i in range(start, end + 1):
            s[stmt.var] = i
            for s_ in stmt.body:
                execute_code(s_)
    
    elif stmt_type == 'Comment':
        pass  

    else:
        raise Exception(f"[Lỗi]: Lệnh không hợp lệ: {stmt_type}")

#Run the whole program
def run_program(model):
    for stmt in model.statements:
        execute_code(stmt)

#Start point when running the file
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách dùng: python interpreter.py <file.viet>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        model = viet_mm.model_from_file(input_file)
        run_program(model)
    except Exception as e:
        print(f"[Lỗi]: {e}")
