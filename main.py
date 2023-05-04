import re

class Interpreter:
    def __init__(self):
        self.variables = {}

    def error(self, message):
        print("\n"+message)

    def interpret(self, code):
        valid_characters = "abcdefghijklmnopqrstuvqxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        lines = code.split("\n")

        for line in lines:
            split_line = line.split(' ')

            # storing variable
            if line.startswith("save "):
                if split_line[2] == "as":
                    variable_name = split_line[1]
                    variable_value = split_line[3]
                    self.variables[variable_name] = variable_value
                else:
                    Interpreter.error(self, "Invalid Syntax - Missing value declaration token.")

            # printing to console
            elif line.startswith("display "):
                # number
                if split_line[1].isdigit():
                    print(split_line[1])
                # text
                elif split_line[1].startswith('"') and split_line[1].endswith('"'):
                    print(split_line[1][1:-1])
                # variable
                else:
                    if bool(re.match("[a-zA-Z_-]*$", split_line[1])):
                        if split_line[1] in self.variables:
                            print(self.variables[split_line[1]])
                        else:
                            Interpreter.error(self, "Invalid token - Incorrect variable name.")
                    else:
                        Interpreter.error(self, "Invalid token - Tokens must only contain letters, underscores, or dashes.")


f = open('run_me.ez', encoding="utf-8")  # open json file
code = f.read()
f.close()  # close file

interpreter = Interpreter()
interpreter.interpret(code)