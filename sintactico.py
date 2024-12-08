class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def parse(self):
        """
        Inicia el análisis sintáctico y asegura que no haya duplicados.
        """
        result = []
        while self.pos < len(self.tokens):
            try:
                stmt = self.parse_statement()
                if stmt:
                    result.append(stmt)
            except Exception as e:
                self.errors.append(str(e))
                break
        if self.pos < len(self.tokens):
            self.errors.append(f"Error: Tokens restantes sin procesar en la posición {self.pos}.")
        return result

    def parse_statement(self):
        """
        Analiza una declaración.
        """
        if self.match("KEYWORD", "def"):
            return self.parse_function_def()
        elif self.match("KEYWORD", "return"):
            return self.parse_return_statement()
        else:
            self.error("Se esperaba una declaración válida.")
            return None

    def parse_function_def(self):
        """
        Analiza la declaración de una función.
        """
        self.consume("KEYWORD", "def")
        name = self.consume("IDENTIFIER", "Se esperaba el nombre de la función.")
        self.consume("SYMBOL", "(", "Se esperaba `(` para los parámetros de la función.")
        params = self.parse_params()
        if not self.check("SYMBOL", ")"):
            self.error("Se esperaba `)` para cerrar los parámetros de la función.")
        self.consume("SYMBOL", ")", "Se esperaba `)` para cerrar los parámetros.")
        self.consume("SYMBOL", ":", "Se esperaba `:` después de la declaración de la función.")
        return {"type": "function", "name": name, "params": params}

    def parse_params(self):
        """
        Analiza los parámetros de una función.
        """
        params = []
        while not self.check("SYMBOL", ")"):
            params.append(self.consume("IDENTIFIER", "Se esperaba un parámetro."))
            if self.check("SYMBOL", ","):
                self.consume("SYMBOL", ",")
        return params

    def parse_return_statement(self):
        """
        Analiza una declaración `return`.
        """
        self.consume("KEYWORD", "return")
        value = self.parse_expression()
        return {"type": "return", "value": value}

    def parse_expression(self):
        """
        Analiza una expresión.
        """
        left = self.consume("IDENTIFIER", "Se esperaba un identificador.")
        if self.check("SYMBOL", "+"):
            operator = self.consume("SYMBOL", "+")
            right = self.consume("IDENTIFIER", "Se esperaba un identificador.")
            return {"type": "binary_op", "operator": operator, "left": left, "right": right}
        return {"type": "variable", "name": left}

    def match(self, token_type, token_value=None):
        """
        Verifica si el token actual coincide con el tipo y valor esperados.
        """
        if self.pos >= len(self.tokens):
            return False
        token = self.tokens[self.pos]
        if token[0] == token_type and (token_value is None or token[1] == token_value):
            self.pos += 1
            return True
        return False

    def consume(self, token_type, error_message=None):
        """
        Consume un token si coincide con el tipo esperado; lanza un error si no.
        """
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            token = self.tokens[self.pos]
            self.pos += 1
            return token[1]
        self.error(error_message or f"Se esperaba un token de tipo {token_type}.")
        return None

    def check(self, token_type, token_value=None):
        """
        Verifica el token actual sin consumirlo.
        """
        if self.pos >= len(self.tokens):
            return False
        token = self.tokens[self.pos]
        return token[0] == token_type and (token_value is None or token[1] == token_value)

    def error(self, message):
        """
        Registra un error.
        """
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            error_message = f"{message} (token: {token}, posición: {self.pos})"
        else:
            error_message = f"{message} (fin del archivo alcanzado)."
        self.errors.append(error_message)
        raise Exception(error_message)
