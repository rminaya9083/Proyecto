import tkinter as tk
from tkinter import filedialog, scrolledtext
from lexico import Lexer
from ast_generator import ASTGenerator
from sintactico import Parser
import sys
import io


class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico, Sintáctico y AST de Python")

        # Área de texto para entrada de código
        self.code_label = tk.Label(root, text="Código Fuente:")
        self.code_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.code_input = scrolledtext.ScrolledText(root, height=10, width=60)
        self.code_input.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        # Botón para analizar el código
        self.analyze_button = tk.Button(root, text="Analizar Código", command=self.analyze_code)
        self.analyze_button.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        # Área de texto para la salida de tokens
        self.tokens_label = tk.Label(root, text="Tokens Generados:")
        self.tokens_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.tokens_output = scrolledtext.ScrolledText(root, height=10, width=30, state="disabled")
        self.tokens_output.grid(row=4, column=0, padx=5, pady=5)

        # Área de texto para la salida de ejecución
        self.execution_label = tk.Label(root, text="Salida de Ejecución:")
        self.execution_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.execution_output = scrolledtext.ScrolledText(root, height=10, width=30, state="disabled")
        self.execution_output.grid(row=4, column=1, padx=5, pady=5)

        # Área de texto para el análisis sintáctico
        self.syntax_label = tk.Label(root, text="Análisis Sintáctico:")
        self.syntax_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.syntax_output = scrolledtext.ScrolledText(root, height=5, width=60, state="disabled")
        self.syntax_output.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Área de texto para la salida del AST
        self.ast_label = tk.Label(root, text="AST Generado:")
        self.ast_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.ast_output = scrolledtext.ScrolledText(root, height=10, width=60, state="disabled")
        self.ast_output.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Instancias del analizador léxico y generador de AST
        self.lexer = Lexer()
        self.ast_generator = ASTGenerator()

    def analyze_code(self):
        """
        Realiza el análisis del código y muestra los resultados.
        """
        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            self.display_error("Error: El código fuente está vacío.")
            return

        # Análisis Léxico
        try:
            tokens = self.lexer.tokenize(code)
            self.display_tokens(tokens)
        except SyntaxError as e:
            self.display_error(f"Error en análisis léxico: {e}")
            return

        # Generación del AST y manejo de errores sintácticos
        ast_output = self.ast_generator.generate_ast(code)
        if "Error de sintaxis" in ast_output:
            self.display_syntax(ast_output)  # Envía el mensaje de error al análisis sintáctico
            self.display_ast(ast_output)    # Opcional: también lo muestra en el AST si deseas
            return
        else:
            self.display_syntax("Compilado correctamente.")

        # Mostrar AST si no hay errores
        self.display_ast(ast_output)

        # Ejecución del código
        self.run_code(code)

    def run_code(self, code):
        """
        Ejecuta el código fuente y captura su salida.
        """
        # Captura de salida
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            exec(code)  # Ejecuta el código dinámico
        except Exception as e:
            output = f"Error al ejecutar el código: {e}"
        else:
            output = redirected_output.getvalue()
        finally:
            sys.stdout = old_stdout

        # Mostrar la salida en el área correspondiente
        self.execution_output.configure(state="normal")
        self.execution_output.delete("1.0", tk.END)
        self.execution_output.insert(tk.END, output)
        self.execution_output.configure(state="disabled")

    def display_tokens(self, tokens):
        """
        Muestra los tokens generados en el área de salida de tokens.
        """
        self.tokens_output.configure(state="normal")
        self.tokens_output.delete("1.0", tk.END)
        for token_type, value in tokens:
            self.tokens_output.insert(tk.END, f"{token_type}: {value}\n")
        self.tokens_output.configure(state="disabled")

    def display_syntax(self, syntax_output):
        """
        Muestra el resultado del análisis sintáctico en el área de salida.
        """
        self.syntax_output.configure(state="normal")
        self.syntax_output.delete("1.0", tk.END)
        self.syntax_output.insert(tk.END, syntax_output)
        self.syntax_output.configure(state="disabled")

    def display_ast(self, ast_output):
        """
        Muestra el AST generado en el área de salida del AST.
        """
        self.ast_output.configure(state="normal")
        self.ast_output.delete("1.0", tk.END)
        self.ast_output.insert(tk.END, ast_output)
        self.ast_output.configure(state="disabled")

    def display_error(self, message):
        """
        Muestra un mensaje de error en todas las áreas de salida.
        """
        self.tokens_output.configure(state="normal")
        self.tokens_output.delete("1.0", tk.END)
        self.tokens_output.insert(tk.END, message)
        self.tokens_output.configure(state="disabled")

        self.execution_output.configure(state="normal")
        self.execution_output.delete("1.0", tk.END)
        self.execution_output.insert(tk.END, message)
        self.execution_output.configure(state="disabled")

        self.syntax_output.configure(state="normal")
        self.syntax_output.delete("1.0", tk.END)
        self.syntax_output.insert(tk.END, message)
        self.syntax_output.configure(state="disabled")

        self.ast_output.configure(state="normal")
        self.ast_output.delete("1.0", tk.END)
        self.ast_output.insert(tk.END, message)
        self.ast_output.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()
