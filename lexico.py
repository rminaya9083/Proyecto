import re

class Lexer:
    def __init__(self):
        # Definir tokens usando expresiones regulares
        self.token_patterns = [
            (r'[ \t\n]+', None),  # Espacios en blanco (se ignoran)
            (r'#[^\n]*', 'COMMENT'),  # Comentarios
            (r'\".*?\"|\'[^\']*\'', 'STRING'),  # Cadenas
            (r'\b\d+\b', 'NUMBER'),  # Números enteros
            (r'\b(def|class|if|else|while|for|return|import|from|as|in|try|except|finally|with|lambda|True|False|None)\b', 'KEYWORD'),  # Palabras clave
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # Identificadores
            (r'[+\-*/%]', 'OPERATOR'),  # Operadores
            (r'[=><!]=?|==|!=', 'COMPARISON'),  # Operadores de comparación
            (r'[{}()\[\],.;:]', 'SYMBOL')  # Símbolos, incluyendo ":"
        ]

    def tokenize(self, code):
        tokens = []
        while code:
            match_found = False
            for pattern, token_type in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(code)
                if match:
                    match_found = True
                    value = match.group(0)
                    if token_type:  # Ignorar los tokens que no tienen tipo
                        tokens.append((token_type, value))
                    code = code[len(value):]  # Reducir el código analizado
                    break
            if not match_found:
                raise SyntaxError(f"Carácter inválido: {code[0]}")
        return tokens
