import ast
import json

class ASTGenerator:
    def __init__(self):
        pass

    def generate_ast(self, code):
        """
        Genera un Árbol de Sintaxis Abstracta (AST) a partir del código fuente dado y lo devuelve formateado como JSON.
        """
        try:
            parsed_ast = ast.parse(code)  # Analiza el código y genera el AST
            ast_dict = self.format_ast(parsed_ast)  # Convierte el AST a un diccionario
            return json.dumps(ast_dict, indent=4)  # Convierte el diccionario en JSON formateado
        except SyntaxError as e:
            return f"Error de sintaxis: {e}"

    def format_ast(self, node):
        """
        Convierte el AST (basado en clases de ast) en un formato de diccionario.
        """
        if isinstance(node, ast.Module):
            return {
                "type": "module",
                "body": [self.format_ast(child) for child in node.body]
            }
        elif isinstance(node, ast.FunctionDef):
            return {
                "type": "function",
                "name": node.name,
                "params": [arg.arg for arg in node.args.args],
                "body": [self.format_ast(child) for child in node.body]
            }
        elif isinstance(node, ast.Return):
            return {
                "type": "return",
                "value": self.format_ast(node.value)
            }
        elif isinstance(node, ast.BinOp):
            return {
                "type": "binary_op",
                "operator": self.get_operator_name(node.op),
                "left": self.format_ast(node.left),
                "right": self.format_ast(node.right)
            }
        elif isinstance(node, ast.Name):
            return {
                "type": "variable",
                "name": node.id
            }
        elif isinstance(node, ast.Add):
            return "Add"
        return {"type": str(type(node))}

    def get_operator_name(self, op):
        """
        Devuelve el nombre del operador en formato de string.
        """
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        return "unknown"
