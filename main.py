class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, code):
        lines = code.split("\n")
        print(code)


f = open('run_me.ez', encoding="utf-8")  # open json file
code = f.read()
f.close()  # close file

interpreter = Interpreter()
interpreter.interpret(code)