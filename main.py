import re


class Interpreter:
    def __init__(self):
        self.variables = {}

    def error(self, message):
        exit("\n" + message)

    def evaluate(self, arithmetic):
        for variable in self.variables:
            if variable in arithmetic:
                arithmetic = arithmetic.replace(variable, str(self.variables[variable]))
        return eval(arithmetic)

    def interpret(self, code):
        tokens = ['save', 'as', 'if', 'equals', 'above', 'below', 'repeat', 'forever', 'until', 'times', 'and', 'or',
                  'and', 'display', 'otherwise', 'stop']
        lines = code.split("\n")
        saved_lines = ""
        saving = False
        repeat_type = None

        for line in lines:
            split_line = re.split(r' \s*(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

            if saving and not line.startswith("end"):
                saved_lines += line + "\n"
                continue

            # storing variable
            if line.startswith("save "):
                if split_line[2] == "as":
                    variable_name = split_line[1]
                    if variable_name not in tokens:
                        raw_value = split_line[3]
                        # number
                        if raw_value.isdigit():
                            self.variables[variable_name] = raw_value
                        # string
                        elif raw_value.startswith('"') and raw_value.endswith('"'):
                            self.variables[variable_name] = raw_value[1:-1]
                        # variables
                        else:
                            # just variable
                            if bool(re.match("[a-zA-Z_-]*$", raw_value)):
                                if raw_value in self.variables:
                                    self.variables[variable_name] = self.variables[raw_value]
                                else:
                                    Interpreter.error(self, "Invalid token - Incorrect variable name.")
                            else:
                                solution = Interpreter.evaluate(self, raw_value)
                                self.variables[variable_name] = solution
                                #Interpreter.error(self, "Invalid token - Tokens must only contain letters, underscores, or dashes.")
                    else:
                        Interpreter.error(self, "Invalid token - Invalid variable name.")
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
                    if bool(re.match("[a-zA-Z_]*$", split_line[1])):
                        if split_line[1] in self.variables:
                            print(self.variables[split_line[1]])
                        else:
                            Interpreter.error(self, "Invalid token - Incorrect variable name.")
                    else:
                        solution = Interpreter.evaluate(self, split_line[1])
                        print(solution)

            # loops
            elif line.startswith("repeat "):
                # forever
                if split_line[1] == "forever":
                    saving = True
                    repeat_type = "forever"
                # set amount of times
                elif split_line[2] == "times":
                    if split_line[1].isdigit():
                        repeat_type = split_line[1]
                        saving = True
                    else:
                        Interpreter.error(self, "Invalid token - Disallowed repeat amount")

            # end if, repeat, etc
            elif line.startswith("end "):
                if split_line[1] == "repeat":
                    saving = False
                    interpreter_repeat = Interpreter()

                    if repeat_type == "forever":
                        while True:
                            interpreter_repeat.interpret(saved_lines)
                    elif repeat_type.isdigit():
                        for x in range(0, int(repeat_type)):
                            interpreter_repeat.interpret(saved_lines)


f = open('run_me.ez', encoding="utf-8")  # open json file
code = f.read()
f.close()  # close file

interpreter = Interpreter()
interpreter.interpret(code)