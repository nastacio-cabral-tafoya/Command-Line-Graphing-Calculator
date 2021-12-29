#Assignment: Unrefined Graphing Calculator
#Description: Unrefined Graphing Calculator.
#Name: Nastacio Cabral-Tafoya
#Class: CSC 119 1x1
#Instructor: Fred Pinzenscham
"""
Program Name: "Unrefined Graphing Claculator"
Description:
	This is an unrefined graphing calculator that I
	coded in a period of a few days, so I have not
	gotten a chance to work all of the bugs out.
	Example:
            To make a number negative, you have to subtract it from zero.
                -n would be typed 0-n
        There cannot be more than one space between each command or character in a formula.
        When setting graph parameters, there cannot be any spaces after the colon.
        Closing the turtle window without using the "close graph" command will cause an error.
        There has to be a * symbol when multiplying.
        I coded functions so that they can accept multiple parameters.
            Example:
                power(base, exponent) = base^exponent
                power(2, 10) = 1,024

                However! The formula parser cannot properly parse power(2, 10).
                So as of right now, this code only supports functions with one parameter.

        All variable declarations given to the program in the console or by using a script file will be global.
        If a variable is changed while calculating the value of a function or during graphing it will change everywhere!
"""

import sys
import math
import turtle
import os

def removeEndSpaces(string):
# Parameters string:" var zoom = 115 "
# returns "var zoom = 115"
# If there is a space in position 0 of a string and a space in the last 
# position in the string, it removes the beginning and ending spaces.
    i      = 0
    start  = 0
    end    = 0

    while ((start < len(string)) and (string[start] == ' ')):
        start += 1

    i = start
           
    while (i < len(string)):
        if (string[i] == ' '):
            end -= 1
        else:
            end = 0
        i += 1

    if (end == 0):
        end = None
        
    return (string[start:end])

def getCommandList(string):
    # Parameter string:"var scale = (1 / 5) & var zoom = 115 & var graphMin = (0 - 4)" will
    # return ["var scale = (1 / 5) ", " var zoom = 115 ", " var graphMin = (0 - 4)"]
    # Separates commands into an iterable list so that they can be executed individually.
    retVal = []
    i      = 0
    
    while (i < len(string)):
        line = ""
        
        while ((i < len(string)) and (not(string[i] == '&') and not(string[i] == '\n'))):
            line += string[i]
            i    += 1
        
        retVal.append(removeEndSpaces(line))
        i += 1
    
    return (retVal)

def beginsWith(string, keyword):
    # Determines if a string begins with a specified pattern of characters.
    # beginsWith("open graph", "open ") will return True.
    # beginsWith("open graph", "open") will return False.
    retVal = False
    i      = 0
    
    if (len(keyword) <= len(string)):
        i         = 0
        selection = ""
        
        while (i < len(keyword)):
            selection += string[i]
            i         += 1
        
        if (selection == keyword):
            retVal = True
                
    return (retVal)

def containsChar(string, char):
    # Determines if a string contains a char.
    # containsChar("var n = 100", '=') returns True.
    # containsChar("(n+n^2)/2", '=') returns False.
    retVal = False
    
    for ch in string:
        if (ch == char):
            retVal = True
    
    return (retVal)

def removeChar(string, char, preserveCount):
    # Removes a char from a string after the count of that character supasses the limit from the begining of the string.
    # removeChar("var x = (n + n ^ 2) / 2", ' ', 1) will return "var x=(n+n^2/2)". It removed all but one space.
    # removeChar("x = (n + n ^ 2) / 2", ' ', 0) will return "x=(n+n^2/2)". It removed all spaces.
    retVal     = ""
    spaceCount = 0
    
    for ch in string:
        if (ch == char):
            if (spaceCount < preserveCount):
                retVal     += ch
                spaceCount += 1
        else:
            retVal += ch
    
    return (retVal)

class Calculator:
    # This code contains everything that the calculator ability of this program does.
    # Variable Declaration.
    # Function Declaration.
    # Constant Declaration
    # Infix to Postfix conversion.
    # Operator Precedence.
    # Variable and Function evaluation.
    # Operator Evaluation.
    # Postfix evaluation.
    def __init__(self):
        self.PRECEDENCE = {
            # Stores operators and their precedence.
            # Functions such as sin(x) or a user declared f(x) are considered single operand operators.
            # sin(x) only requires one operand to work.
            # 2 + 2 requires two operands to work.
            "!":11,      #Factoral
            chr(130):11, #Sqare Root
            chr(131):11, #Sine
            chr(132):11, #Cosine
            chr(133):11, #Tangent
            chr(134):11, #asine
            chr(135):11, #acosine
            chr(136):11, #atangent
            chr(137):11, #cosecant
            chr(138):11, #secant
            chr(139):11, #cotangent
            chr(140):11, #Natural Log
            chr(141):11, #Log Base 10
            chr(142):11, #Absolute Value
            "^":10,      #Exponent
            "*":9,       #Multiplication
            "/":9,       #Division
            "+":8,       #Addition
            "-":8,       #Subtraction
            "(":-1,
            ")":-1,
            "NONE":-1
        }
        self.SINGLEOPPS = {
            # Stores all of the single operators and their precedence.
            # This dictionary helps the evaluatePost() function to determine whether it
            # needs to pop two operands from a stack or only one to properly perform an operation.
            "!":11,      #Factoral
            chr(130):11, #Sqare Root
            chr(131):11, #Sine
            chr(132):11, #Cosine
            chr(133):11, #Tangent
            chr(134):11, #asine
            chr(135):11, #acosine
            chr(136):11, #atangent
            chr(137):11, #cosecant
            chr(138):11, #secant
            chr(139):11, #cotangent
            chr(140):11, #Natural Log
            chr(141):11, #Log Base 10
            chr(142):11, #Absolute Value
        }
        self.CONVERSIONS = {
            # Stores the conversion string for a function so that the convert1ParamOpps() function can convert
            # the user's "sqrt(x)" entry to "0x82(x)".
            # For simpliity in converting infix to postfix, single operand operators are not evaluated as "sqrt(x)" or "f(x)".
            # The function names are converted into a byte that signifies that function to the evaluateFromStack() function in this object.
            # The function "sqrt(x)" would be evaluated as "0x82(x)".
            # All bytes from the decimal value 150 and above are for user defined functions.
            "sqrt(":(chr(130) + "("),
            "log(":(chr(141) + "("),
            "ln(":(chr(140) + "("),
            "sin(":(chr(131) + "("),
            "cos(":(chr(132) + "("),
            "tan(":(chr(133) + "("),
            "asin(":(chr(134) + "("),
            "acos(":(chr(135) + "("),
            "atan(":(chr(136) + "("),
            "csc(":(chr(137) + "("),
            "sec(":(chr(138) + "("),
            "cot(":(chr(139) + "("),
            "abs(":(chr(142) + "(")
        }
        self.FUNCTIONNAMES = {} #Stores user defined function names and their parameters. Example: {"f":"(n))", "g":"(x)"}
        self.FUNCTIONS     = {} #Stores user defined function names and their definitions. Example: {"f(n)":"(n + n ^ 2) / 2", "g(x)":"sin(x)"}
        self.CONSTANTS     = {
            # Stores constant variables.
            # Some constants are defined by default.
            # This also stores user defined constants.
            "pi":math.pi,
            "e":math.e,
            "gr":1.618033988749895
        }
        self.VARIABLES  = {}  #Stores user defined variables. Example: {"n":100, "s":2}
        self.baseChars  = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15} # Contains characters and their values for base 2 - 16 number systems.
        self.history    = ""  #Stores the calculators calculation history every time the calculate() function is called.
        self.conversion = 150 #All bytes above the decimal value 150 are allocated for user defined functions. Each time a user defines a new function, this value is incremented.

    def getHistory(self):
        # returns the calculation history string.
        return(self.history)
    
    def setVariable(self, var, val):
        # sets a new user defined variable.
        # Example: setVariable("n", 100) will add {"n":100} to the VARIABLES dictionary.
        if self.isValidVar(var):
            self.VARIABLES[var] = val
        else:
            print("\"" + var + "\" is not a valid variable name!")
    
    def getVariable(self, var):
        # Returns the variable's value.
        # Example: getVariable("n") will return 100 based on the comments above.
        retVal = None
        
        if (var in self.VARIABLES):
            retVal = self.VARIABLES[var]
        elif (var in self.CONSTANTS):
            retVal = self.CONSTANTS[var]
        
        return(retVal)

    def printVariables(self):
        # Displays the list of variables currently stored in the VARIABLES dictionary in the console window
        # so that the user can see the variables that they have declared.
        print("Variable Assigned:")

        for var in self.VARIABLES:
            print("\t" + var + " = " + str(self.VARIABLES[var]))
        print("\n")

    def printConstants(self):
        # Displays the list of constants currently stored in the CONSTANTS dictionary in the console window
        # so that the user can see the constants that they have declared.
        print("Constants Assigned:")

        for const in self.CONSTANTS:
            print("\t" + const + " = " + str(self.CONSTANTS[const]))
        print("\n")
    
    def setFunction(self, identifier, formula):
        # Sets a user defined function.
        # Example: setFunction("summation(n)", "(n + n ^ 2) / 2") will add {"summation":"(n)"} to the FUNCTIONNAMES dictionary.
        #                                                         will add {"summation(n)":"(n + n ^ 2) / 2"} to the FUNCTIONS dictionary.
        #                                                         will add {"summation(":"[byte for function]("} to the CONVERSIONS dictionary.
        #                                                         will add {"[byte for function]":precedence"} to the SINGLEOPPS dictionary.
        #                                                         will add {"[byte for function]":precedence"} to the PRECEDENCE dictionary.
        functionName = ""
        i            = 0
        errors       = True

        while (i < len(identifier)):
            if (identifier[i] == "("):
                errors = False
                break
            else:
                functionName += identifier[i]
            i += 1

        if not errors:
            if containsChar((functionName + identifier[i]), "("):
                self.FUNCTIONNAMES[identifier.split('(')[0]]           = ('(' + identifier.split('(')[1])
                self.FUNCTIONS[identifier]                             = formula
                self.CONVERSIONS[functionName + identifier[i]]         = (chr(self.conversion) + identifier[i])
                self.CONVERSIONS[chr(self.conversion) + identifier[i]] = (functionName + identifier[i])
                self.SINGLEOPPS[chr(self.conversion)]                  = 11
                self.PRECEDENCE[chr(self.conversion)]                  = self.SINGLEOPPS[chr(self.conversion)]
                self.conversion                                       += 1
            else:
                print("Invalid Function Name!")
        else:
            print("Invalid Function Name!")

    def evaluateFunction(self, identifier):
        # Evaluates a function.
        # Example: evaluateFunction("summation(100)") based on the comments above will return 5050.
        retVal        = None
        segments      = identifier.split('(')
        functionName  = segments[0]
        parameterList = removeChar(segments[1].split(')')[0], " ", 0).split(',')
        
        if (functionName in self.FUNCTIONNAMES):
            parameterVars = removeChar(self.FUNCTIONNAMES[functionName][1:-1], " ", 0).split(',')

            if (len(parameterList) == len(parameterVars)):
                for index, var in enumerate(parameterVars):
                    self.setVariable(var, self.calculate(parameterList[index]))
                    
                retVal = self.calculate(self.FUNCTIONS[functionName + self.FUNCTIONNAMES[functionName]])
            else:
                if (len(parameterList) > len(parameterVars)):
                    print("Too many values were passed to the function.")
                else:
                    print("Not enough values were passed ot the function.")
        else:
            print("The function does not exist.")
        return (retVal)

    def getFunctionDefinition(self, identifier):
        # Gets the function definition.
        # Example: getFunctionDefinition("summation(n)") based on the comments above will return "(n + n ^ 2) / 2"
        return(self.FUNCTIONS[identifier])

    def printFunctions(self):
        # Displays the list of user defined functions currently stored in the FUNCTIONS dictionary in the console window
        # so that the user can see the functions that they have declared. 
        print("Functions Assigned:")

        for function in self.FUNCTIONS:
            print("\t" + function + " = " + str(self.FUNCTIONS[function]))
        print("\n")

    def incrementVariable(self, var, increment):
        # Increments a variable in the VARIABLES dictionary.
        # Example: incrementVariable("n", 1) will add 1 to the variable's value.
        # Example: if var n = 0, then incrementVariable("n", 1) will set n equal to 1.
        # If ran again, n would be equal to 2 and so-on.
        if (var in self.VARIABLES):
            self.VARIABLES[var] += increment
        else:
            print("The variable \"" + var + "\" has not been declared!")

    def setConstant(self, const, val):
        # sets a new user defined constant.
        # Example: setConstant("s", 2) will add {"s":2} to the CONSTANTS dictionary.
        if not(const in self.CONSTANTS):
            if self.isValidVar(const):
                self.CONSTANTS[const] = val
            else:
                print("\"" + const + "\" is not a valid variable name!")
        else:
            print("A constant cannot be changed after it has been declared!")
        
    def gamma(self, number):
        # Gamma function.
        # This is a python generator.
        # It will only iterate 1000000 times.
        # It will iterate between 0 and 100.
        # Example: gamma(5) yields a series of numbers that summate to 120.
        # Example: gamma(0.5) yields a series of numbers that summate to (sqrt(pi) / 2).
        i      = 0

        while (i < 100):
            try:
                yield((i ** number) * (math.e ** (-i)))
            except ZeroDivisionError as e:
                break
            i += 0.0001

    def factorial(self, number):
        # Factorial Function
        # Summation of the values of the gamma function.
        # Example: factorial(5) returns 120.
        # Example: factorial(0.5) returns (sqrt(pi) / 2)
        retVal = 0
        
        for g in self.gamma(number):
            retVal += g

        # The result of the summation above for some reason gets multiplied by 10 for every decimal place I decreased the increment in the gama function.
        # I don't know how or why, but my work around was to divide the result by (1 / increment) from the gama function.
        return (round((retVal / 10000), 5))

    def convert1ParamOpps(self, string):
        # Converts single operand operators to their byte value.
        # Example, convert1ParamOpps("sqrt(sin(n)) - n") will return "0x82(0x83(n)) - n"
        retVal = ""
        i      = 0
        
        while (i < len(string)):
            j       = i
            testStr = ""
            
            while (j < len(string)):
                if (not(string[j] in self.PRECEDENCE)):
                    testStr += string[j]
                    j       += 1
                else:
                    break
                
            if(j < len(string)):
                testStr += string[j]
            
            if (testStr in self.CONVERSIONS):
                retVal += self.CONVERSIONS[testStr]
            else:
                retVal += testStr
            i = j
            i += 1
            
        return (retVal)

    def parseFormulaVar(self, string):
        # Parses x out of f(x).
        # Example: parseFormulaVar("f(x)") will return "x".
        retVal            = ""
        insideParenthesis = False
        i                 = 0
    
        while (i < len(string)):
            if (string[i] == '('):
                insideParenthesis = True
                i += 1
            elif (string[i] == ')'):
                insideParenthesis = False
    
            if (insideParenthesis and (i < len(string))):
                retVal += string[i]
            i += 1
    
        return (retVal)

    def isValidVar(self, string):
        # Determines whether or not a variable is valid, not already declared in the CONSTANTS dictionary, and that it does not contain any operators.
        # Example: isValidVar("1n") will return False.
        # Example: isValidVar("n1") will return True.
        # Example: isValidVar("+n") will return False.
        retVal = True
    
        if (((ord(string[0]) >= 48) and (ord(string[0]) <= 57)) or (string in self.CONSTANTS)):
            retVal = False
        else:
            for ch in string:
                if (ch in self.PRECEDENCE):
                    retVal = False
    
        return (retVal)

    def upper(self, string):
        # Converts a string to uppercase.
        # Example: upper("The quick brown fox jumped over the lazy dogs.") will return "THE QUICK BROWN FOX JUMPED OVER THE LAZY DOGS."
        retVal = ""
        i      = 0
        while (i < len(string)):
            if ((ord(string[i]) >= 97) and (ord(string[i]) <= 122)):
                retVal += chr(ord(string[i]) - 32)
            else:
                retVal += string[i]
            i += 1
            
        return (retVal)
    
    def validNumberForBase(self, string, base):
        # Determines whether or not a string contains valid characters for the base that it is going to be converted to.
        # Example: validNumberForBase("1010", 2) will return True.
        # Example: validNumberForBase("10103", 2) will return False.
        # Example: validNumberForBase("f", 16) will return True.
        # Example: validNumberForBase("g", 16) will return False.
        # Example: validNumberForBase("8", 8) will return False.
        # Example: validNumberForBase("7", 8) will return True.
        retVal = True
        for ch in string:
            if (ch in self.baseChars):
                if (self.baseChars[ch] > (base - 1)):
                    retVal = False
            else:
                retVal = False
                
        return (retVal)
        
    def baseToDec(self, string, base):
        # Binary to Decimal Converter using Recursion.
        # Example: baseToDec("1100100", 2) will return 100.
        # Example: baseToDec("64", 16) will return 100.
        if len(string) == 0:
            return 0
        else:
            return(self.baseChars[string[0]] * (base ** (len(string) - 1)) + self.baseToDec(string[1:], base))

    def alphaNumeric(self, ch):
        # Determines whether or not a character is a part of a variable/number, or an operator.
        # Example: alphaNumeric("100") will return True.
        # Example: alphaNumeric("+") will return False.
        # Example: alphaNumeric("!") will return False.
        # Example: alphaNumeric("x") will return True.
        retVal = True
        
        for operator in self.PRECEDENCE:
            if (ch == operator):
                retVal = False
                
        return (retVal)

    def isNumeric(self, string):
        # This function needs to be rewritten because it may not return True for the correct values at the moment.
        # Example: isNumeric("-100.00") will return True.
        # Example: isNumeric("n1") will return False.
        retVal = True
    
        for ch in string:
            if (((ord(ch) < 48) or (ord(ch) > 57)) and not(ch == ".") and not(ch == "-")):
                retVal = False
                break

        return (retVal)

    def stackTop(self, stack):
        # Returns the top value in a stack.
        # Example: stackTop([1, 2, 3, 4, 5]) will return 5.
        retVal = "NONE"
    
        if (len(stack) > 0):
            retVal = stack[len(stack) - 1]
        
        return (retVal)

    def evaluateVariable(self, var):
        # Evalutates an alphanumeric string.
        # Example: evaluateVariable("pi") will return 3.14159263xxxxxxxxxxxxx
        # Example: evaluateVariable("100") will return 100.
        # This function also determines whether or not a binary, octal, or hexadecimal switch has been added to a number.
        # Example: evaluateVariable("1010b") will return 10.0.
        retVal = None
        
        if (var in self.VARIABLES):
            retVal = self.VARIABLES[var]
        elif (var in self.CONSTANTS):
            retVal = self.CONSTANTS[var]
        else:
            try:
                if (len(var) > 0):
                    if ('|' in var):
                        operands = var.split('|')
                        
                        if (len(operands) == 2):
                            try:
                                if self.validNumberForBase(operands[0], int(operands[1])):
                                    retVal = float(self.baseToDec(operands[0], int(operands[1])))
                                else:
                                    print("\"" + operands[0] + "\" does not contain valid characters for base " + operands[1] + "!")
                                    retVal = None
                            except ValueError as e:
                                print("\"" + operand + "\" is not formatted correctly!\n\tThe correct format is:\n\t\t[<int>number]|[<int>base]\n")
                                retVal = None
                        elif (len(operands) < 2):
                            print("\"" + operand + "\" is not formatted correctly!\n\tThe correct format is:\n\t\t[<int>number]|[<int>base]\n")
                            retVal = None
                        else:
                            print("\"" + var + "\" is an unknown switch\n\t The correct format is:\n\t\t[<int>number]|[<int>base]\n")
                            retVal = None
                    else:
                        retVal = float(var)
                else:
                    retVal = float(var)
            except (ValueError, TypeError) as e:
                retVal = None
    
        return (retVal)
    
    def evaluateFromStack(self, left, right, operator):
        # After the stack in evaluatePost() has popped the values that it needed to, it sends them to this function.
        # This function determines the operation to perform based on the operator that it receives on the opperands that it recieves.
        retVal = None
    
        leftOpp  = self.evaluateVariable(left)
        rightOpp = self.evaluateVariable(right)
        
        try:
            if (operator == "^"):
                retVal = str(leftOpp ** rightOpp)
            elif (operator == "*"):
                retVal = str(leftOpp * rightOpp)
            elif (operator == "/"):
                try:
                    retVal = str(leftOpp / rightOpp)
                except:
                    retVal = None
            elif (operator == "+"):
                retVal = str(leftOpp + rightOpp)
            elif (operator == "-"):
                retVal = str(leftOpp - rightOpp)
            else:
                if (operator == "!"):
                    retVal = str(self.factorial(leftOpp))
                elif (operator == chr(130)):
                    try:
                        retVal = str(math.sqrt(leftOpp))
                    except ValueError as e:
                        retVal = None
                elif (operator == chr(131)):
                    retVal = str(math.sin(leftOpp))
                elif (operator == chr(132)):
                    retVal = str(math.cos(leftOpp))
                elif (operator == chr(133)):
                    retVal = str(math.tan(leftOpp))
                elif (operator == chr(134)):
                    try:
                        retVal = str(math.asin(leftOpp))
                    except:
                        retVal = None
                elif (operator == chr(135)):
                    try:
                        retVal = str(math.acos(leftOpp))
                    except:
                        retVal = None
                elif (operator == chr(136)):
                    retVal = str(math.atan(leftOpp))
                elif (operator == chr(137)):
                    retVal = str(1 / math.sin(leftOpp))
                elif (operator == chr(138)):
                    retVal = str(1 / math.cos(leftOpp))
                elif (operator == chr(139)):
                    retVal = str(1 / math.tan(leftOpp))
                elif (operator == chr(140)):
                    try:
                        retVal = str(math.log(leftOpp))
                    except ValueError as e:
                        retVal = None
                elif (operator == chr(141)):
                    try:
                        retVal = str(math.log10(leftOpp))
                    except ValueError as e:
                        retVal = None
                elif (operator == chr(142)):
                        retVal = abs(leftOpp)
                else:
                    if (operator in self.PRECEDENCE):
                        try:
                            retVal = str(self.evaluateFunction(self.CONVERSIONS[operator + "("] + str(leftOpp) + ")"))
                        except ValueError as e:
                            retVal = None
                    else:
                        print("Undeclared Function!")
        except TypeError as e:
            varList = {left:leftOpp, right:rightOpp}

            for var in varList:
                if (varList[var] == None):
                    retVal = None
        
        return (str(retVal))

    def evaluatePost(self, postExp):
        # Evaluates a postfix formula.
        # Example: evaluatePost(["100", "2", "*"]) will return 200.
        stack = []
        i     = 0
    
        while (i < len(postExp)):
            if (self.alphaNumeric(postExp[i])):
                stack.append(postExp[i])
            else:
                if (postExp[i] in self.SINGLEOPPS):
                    left  = stack.pop()
                    right = ""
                    stack.append(self.evaluateFromStack(left, right, postExp[i]))
                else:
                    right = stack.pop()
                    left  = stack.pop()
                    stack.append(self.evaluateFromStack(left, right, postExp[i]))
                    
            i += 1
        
        return (self.evaluateVariable(stack.pop()))
        
    def infToPost(self, string):
        # Converts an infix formula to a postfix formula.
        # Example: infToPost("100*2") will return ["100", "2", "*"].
        postfix = []
        stack   = []
        i       = 0

        while (i < len(string)):
            if (self.alphaNumeric(string[i])):
                number = ""
    
                while ((i < len(string)) and self.alphaNumeric(string[i])):
                    number += string[i]
                    i += 1
                i -= 1
                postfix.append(number)
            elif (string[i] == "^"):
                stack.append(string[i])
            elif (string[i] == "("):
                stack.append(string[i])
            elif (string[i] == ")"):
                while (not(self.alphaNumeric(self.stackTop(stack))) and not(self.stackTop(stack) == "(")):
                    postfix += stack.pop()
                stack.pop()
            else:
                if (self.PRECEDENCE.get(string[i]) > self.PRECEDENCE.get(self.stackTop(stack))):
                    stack.append(string[i])
                else:
                    if (len(stack) > 0):
                        while (not(self.alphaNumeric(self.stackTop(stack))) and (self.PRECEDENCE.get(string[i]) <= self.PRECEDENCE.get(self.stackTop(stack)))):
                            postfix += stack.pop()
                        stack.append(string[i])
            i += 1
    
        while (not(self.alphaNumeric(self.stackTop(stack))) and (len(stack) > 0)):
            postfix += stack.pop()
        
        return (postfix)

    def calculate(self, string):
        # Calculates an infix expression.
        # Example: calculate("(100+100^2)/2") returns 5050.

        result = self.evaluatePost(self.infToPost(removeChar(self.convert1ParamOpps(string), " ", 0)))

        self.history += (str(result) + " = " + string + chr(10))

        return (result)

class GraphingCalculator:
    # This class contains everything that is involved in the graphing abilities of this graphing calculator.
    # The graph window.
    # Graph settings.
    # Plotting a graph.
    # Everything including the calculator is done through this class.
    # This class relies on the Calculator class.
    def __init__(self, xMin = -100, xMax = 100, yMin = -100, yMax = 100, xZoom = 20, yZoom = 20, resolution = 1, xScale = 1, yScale = 1):
        self.xMin       = xMin
        self.xMax       = xMax
        self.yMin       = yMin
        self.yMax       = yMax
        self.xZoom      = xZoom
        self.yZoom      = yZoom
        self.resolution = (resolution / (self.xZoom * 10))
        self.xScale     = xScale
        self.yScale     = yScale
        self.GRAPH      = None
        self.CALCULATOR = Calculator() # This is where the calculator object is instantiated.
        self.history    = ""
        self.state      = False

    def printHistory(self):
        # Prints the Calculator's calculation history, and the graphing history in the console for the user to see.
        print("\nCalculator History:\n\t" + self.CALCULATOR.getHistory()+ "\n\nGraphing History:\n\t" + self.history)
    
    def setVariable(self, var, val):
        # Sets a user defined variable.
        self.CALCULATOR.setVariable(var, val)
    
    def getVariable(self, var):
        # Gets the value stored in a variable.
        return(self.CALCULATOR.getVariable(var))

    def getFunctionDefinition(self, identifier):
        # Gets the definition of a function.
        return(self.CALCULATOR.getFunctionDefinition(identifier))

    def printVariables(self):
        # Displays declared the variables on the screen.
        self.CALCULATOR.printVariables()

    def printConstants(self):
        # Displays the declared constants on the screen.
        self.CALCULATOR.printConstants()

    def setFunction(self, identifier, formula):
        # Sets a user defined function.
        self.CALCULATOR.setFunction(identifier, formula)
    
    def printFunctions(self):
        # Prints the user defined functions on the screen.
        self.CALCULATOR.printFunctions()
    
    def setConstant(self, const, val):
        # Sets a user defined constant.
        self.CALCULATOR.setConstant(const, val)
    
    def getCalculator(self):
        # Returns the Calculator object stored in this class.
        return(self.CALCULATOR)

    def calculate(self, string):
        # Evaluates an infix formula.
        return(self.CALCULATOR.calculate(string))

    def evaluateVariable(self, var):
        # Evaluates an alphanumeric string.
        return(self.CALCULATOR.evaluateVariable(var))

    def evaluateFunction(self, identifier):
        # Evaluates a function.
        return(self.CALCULATOR.evaluateFunction(identifier))

    def graphFunction(self, identifier, formula = ""):
        # Draws a function's curve on the graph in the turtle window.
        # Example: graphFunction("f(x)", "x^2") will draw the x^2 curve on the graph.
        # This function uses a python generator to determine the y coordinate.
        if (len(formula) == 0):
            formula = self.getFunctionDefinition(identifier)

        postFormula = self.CALCULATOR.infToPost(self.CALCULATOR.convert1ParamOpps(removeChar(formula, " ", 0)))
        var         = self.CALCULATOR.parseFormulaVar(identifier)
        self.setVariable(var, self.xMin)

        self.setFunction(identifier, formula)
        self.history += (identifier + " = " + formula + "\n")

        for y in self.evaluateYCoordinates(var, postFormula):
            self.GRAPH.goto((self.getVariable(var) * self.xZoom), (y * self.yZoom))
            turtle.update()
    
    def evaluateYCoordinates(self, var, postFormula):
        # Determines the y coordinate.
        # This is a python generator.
        # This has no return statement.
        # This only has yield statements.
        previousInBounds  = True
        previousNone      = False
        adjustedOutBounds = False
        previousValue     = None
        
        self.GRAPH.penup()

        # This may look repedative, but I had to do it.
        # Sometimes a stray line would appear across the graph when graphing certain functions, most notably when graphing tan(x).
        # The next 15 lines stopped the stray line from appearing on the graph.
        # It also makes sure that the graph does't start trying to draw a functions curve until the function gives a value that can be graphed on the real plane.
        #Example: The graph will not start drawing sqrt(x) until (x >= 0) is True, so the turtle will immediately go to the first valid x,y coordinate on the real plane.
        y = self.CALCULATOR.evaluatePost(postFormula)
        
        while ((self.getVariable(var) <= self.xMax) and (y == None)):
            y = self.CALCULATOR.evaluatePost(postFormula)
            self.CALCULATOR.incrementVariable(var, self.resolution)
            if not previousNone:
                previousNone = True
        
        yield(y)
        
        if ((y <= self.yMax) and (y >= self.yMin) and not(previousNone)):
            self.GRAPH.pendown()
        else:
            previousInBounds = False
            previousNone     = False
            
        # The rest of this code draws the curve of a function while checking that the current and previous y coordinates
        # are within the graphing area, and that the current and previous y coordinate exists in the real plane.
        # If the current or previous y coordinate given by the function does not exist in the real plane, or is out of bounds,
        # This function quits drawing until both conditions are True again. This prevents the line crossing pi/2 from appearing
        # While graphing tan(x) and the line crossing 0 when graphing 1/x. This also prevents lines appearing between each real
        # segment of sqrt(sin(x)).
        while(self.getVariable(var) <= self.xMax):
            y = self.CALCULATOR.evaluatePost(postFormula)
            
            while ((self.getVariable(var) <= self.xMax) and (y == None)):
                self.GRAPH.penup()
                y = self.CALCULATOR.evaluatePost(postFormula)
                self.CALCULATOR.incrementVariable(var, self.resolution)
                if not previousNone:
                    previousNone = True

            if not(y == None):
                if ((y <= self.yMax) and (y >= self.yMin) and previousInBounds and not(previousNone)):
                    previousValue = None
                    self.GRAPH.pendown()
                else:   
                    previousNone = False
                    self.GRAPH.penup()
                
                yield(y)
                
                previousInBounds  = ((y <= self.yMax) and (y >= self.yMin))
                adjustedOutBounds = False
                self.CALCULATOR.incrementVariable(var, self.resolution)
    
    def setGridLines(self):
        # Draws the grid and the axis lines in the turtle window.
        # Puts the axis numbers along the axis line.
        x = self.xMin
        y = self.yMin
        
        while (round(x, 1) <= self.xMax):
            self.GRAPH.penup()
        
            if (round(x, 1) == 0):
                self.GRAPH.pencolor((0, 0, 0))
            else:
                self.GRAPH.pencolor((230, 230, 230))
            
            self.GRAPH.goto((x * self.xZoom), (self.yMin * self.yZoom))
            self.GRAPH.pendown()
            self.GRAPH.goto((x * self.xZoom), (self.yMax * self.yZoom))
            self.GRAPH.penup()
            self.GRAPH.pencolor((0 , 0, 0))
            self.GRAPH.goto((x * self.xZoom), -5)
            self.GRAPH.pendown()
            self.GRAPH.goto((x * self.xZoom), 5)
            self.GRAPH.penup()
            if (x == 0):
                self.GRAPH.goto(-5, -15)
                self.GRAPH.write(str(round(x, 1)), align = "right", font=("Verdanda", 8, "normal"))
            else:
                self.GRAPH.goto(((x * self.xZoom) + 1), -20)
                self.GRAPH.write(str(round(x, 1)), align = "center", font=("Verdanda", 8, "normal"))
            x += self.xScale
        
        while (round(y, 1) <= self.yMax):
            self.GRAPH.penup()
            
            if (round(y, 1) == 0):
                self.GRAPH.pencolor((0 , 0, 0))
            else:
                self.GRAPH.pencolor((230,230,230))
            
            self.GRAPH.goto((self.xMin * self.xZoom), (y * self.yZoom))
            self.GRAPH.pendown()
            self.GRAPH.goto((self.xMax * self.xZoom), (y * self.yZoom))
            self.GRAPH.penup()
            self.GRAPH.pencolor((0 , 0, 0))
            self.GRAPH.goto(-5, (y * self.yZoom))
            self.GRAPH.pendown()
            self.GRAPH.goto(5, (y * self.yZoom))
            self.GRAPH.penup()
            if not(y == 0):
                self.GRAPH.goto(-5, ((y * self.yZoom) - 6))
                self.GRAPH.write(str(round(y, 1)), align = "right", font=("Verdanda", 8, "normal"))
            y += self.yScale
        
        turtle.update()

    def parseParameters(self, parameterStr, validParameterList):
        # Parses parameters given for the graph.
        # Example: parseParameters("xzoom:100") will return {"xzoom":100}
        retVal          = None
        parameters      = parameterStr.split(':')
        number          = self.calculate(parameters[1])
        
        if (len(parameters) == 2):
            if not(number == None):
                if (parameters[0] in validParameterList):
                    retVal                = {}
                    retVal[parameters[0]] = float(number)
                else:
                    print("\"" + parameters[0] + "\" is not a valid parameter!")
            else:
                print("Invalid Command")
        elif (len(parameters) < 2):
            print("Not enough parameters have been given!")
        elif (len(parameters) > 2):
            print("Too many parameters have been given!")

        return (retVal)

    def setRange(self, parameter1, parameter2, parameter3, parameter4):
        # Sets the graph's x and y axis range.
        # Example setRange("xmin:0-100", "xmax:100", "ymin:0-100", "ymax:100") will set the minimum and maximum x and y values of the x and y axis.
        try:
            if self.state:
                self.GRAPH.clear()
            
            validParameterList = ["xmin", "xmax", "ymin", "ymax"]
            parameters         = (self.parseParameters(parameter1, validParameterList) | self.parseParameters(parameter2, validParameterList) | self.parseParameters(parameter3, validParameterList) | self.parseParameters(parameter4, validParameterList))
            self.xMin          = parameters["xmin"]
            self.xMax          = parameters["xmax"]
            self.yMin          = parameters["ymin"]
            self.yMax          = parameters["ymax"]
            
            if self.state:
                self.setGridLines()
        except TypeError as e:
            print("Invalid parameters were given!")

    def setZoom(self, parameter1, parameter2):
        # Sets the zoom of the graph. (Makes the graph bigger or smaller along the x and y axis's)
        # setZoom("xzoom:20", "yzoom:30") will zoom in more on the y axis than the x axis. So the x axis will be closer together than the y axis.
        try:
            if self.state:
                self.GRAPH.clear()
            
            validParameterList = ["xzoom", "yzoom"]
            parameters         = (self.parseParameters(parameter1, validParameterList) | self.parseParameters(parameter2, validParameterList))
            self.xZoom         = round(abs(parameters['xzoom']), 1)
            self.yZoom         = round(abs(parameters['yzoom']), 1)
            
            if self.state:
                self.setGridLines()
        except TypeError as e:
            print("Invalid parameters were given!")
            
    def setScale(self, parameter1, parameter2):
        # Sets the scale of the graph.
        # Example: setScale("xscale:1/5", "yscale:1") this will set the x scale to 1/5 and the y scale to 1.
        try:
            if self.state:
                self.GRAPH.clear()
            
            validParameterList = ['xscale', 'yscale']
            parameters         = (self.parseParameters(parameter1, validParameterList) | self.parseParameters(parameter2, validParameterList))
            self.xScale        = round(abs(parameters['xscale']), 1)
            self.yScale        = round(abs(parameters['yscale']), 1)
            
            if self.state:
                self.setGridLines()
        except TypeError as e:
            print("Invalid parameters were given!")
            
    def clear(self):
        # Erases the graph and redraws it based on the graph's settings.
        if self.state:
            self.GRAPH.clear()
            self.setGridLines()
        else:
            print("The graph window is not active!\n")

    def getState(self):
        # If the graph window is open, this function will return True.
        # If the graph window is closed, this function will return False.
        return(self.state)
        
    def stop(self):
        # Closes the turtle window.
        if self.state:
            self.state = False
            self.GRAPH = None
            
            turtle.bye()
            
            turtle.Turtle._screen        = None
            turtle.TurtleScreen._RUNNING = True
        else:
            print("The graph window is not active!\n")
        
    def start(self):
        # Opens the turtle window and sets up the graph.
        if not self.state:
            self.GRAPH = turtle.Turtle()
            
            self.GRAPH.hideturtle()
            turtle.colormode(255)
            turtle.tracer(False)
            self.setGridLines()
            self.state = True
        else:
            print("The graph window is already active!\n")

graphCalc = GraphingCalculator()

def parseCommand(command):
    # Parses the user's input and determines what to do based on the information in the user's input.
    # Example parseCommand("var n = 100") will set a variable "n" equal to 100 in the calculator object.
    # Example parseCommand("close graph") will close the graph window.
    # Example parseCommand("(n + n ^ 2) / 2") will print "(n + n ^ 2) / 2 = 5050.0" in the consle window.
    retVal = False
    
    if containsChar(command, "="):
        if beginsWith(command, "var "):
            assignment = removeChar(command, " ", 1).split(" ")[1].split("=")
            graphCalc.setVariable(assignment[0], graphCalc.calculate(assignment[1]))
        elif beginsWith(command, "function "):
            assignment = removeChar(command, " ", 1).split(" ")[1].split("=")
            graphCalc.setFunction(assignment[0], assignment[1])
        elif beginsWith(command, "const "):
            assignment = removeChar(command, " ", 1).split(" ")[1].split("=")
            graphCalc.setConstant(assignment[0], graphCalc.calculate(assignment[1]))
        elif beginsWith(command, "graph "):
            assignment = removeChar(command, " ", 1).split(" ")[1].split("=")

            if graphCalc.getState():
                graphCalc.graphFunction(assignment[0], assignment[1])
            else:
                print("The graph window is not active!\n")
        else:
            assignment = removeChar(command, " ", 0).split("=")
            
            if not(graphCalc.getVariable(assignment[0]) == None):
                graphCalc.setVariable(assignment[0], graphCalc.calculate(assignment[1]))
            else:
                print("The variable \"" + assignment[0] + "\" has not been declared!")
    else:
        if beginsWith(command, "show "):
            statement = command.split(" ")

            if (statement[1] == "variables"):
                graphCalc.printVariables()
            elif (statement[1] == "constants"):
                graphCalc.printConstants()
            elif(statement[1] == "history"):
                graphCalc.printHistory()
            elif(statement[1] == "functions"):
                graphCalc.printFunctions()
            else:
                print("Invalid Command")
        elif beginsWith(command, "graph "):
            statement = command.split(" ")

            if graphCalc.getState():
                graphCalc.graphFunction(statement[1])
            else:
                print("The graphing window is not active!\n")
        elif beginsWith(command, "open "):
            statement = command.split(" ")

            if (statement[1] == "graph"):
                graphCalc.start()
            else:
                print("Invalid Command")
        elif beginsWith(command, "close "):
            statement = command.split(" ")

            if (statement[1] == "graph"):
                graphCalc.stop()
            else:
                print("Invalid Command")
        elif beginsWith(command, "set "):
            statement = command.split(" ")

            if (statement[1] == "graph"):
                if (statement[2] == "scale"):
                    if (len(statement) == 5):
                        graphCalc.setScale(statement[3], statement[4])
                    elif (len(statement) < 5):
                        print("Not enough parameters have been given!")
                    elif (len(statement) > 5):
                        print("Too many parameters have been given!")
                elif (statement[2] == "zoom"):
                    if (len(statement) == 5):
                        graphCalc.setZoom(statement[3], statement[4])
                    elif (len(statement) < 5):
                        print("Not enough parameters have been given!")
                    elif (len(statement) > 5):
                        print("Too many parameters have been given!")
                elif (statement[2] == "range"):
                    if (len(statement) == 7):
                        graphCalc.setRange(statement[3], statement[4], statement[5], statement[6])
                    elif (len(statement) < 7):
                        print("Not enough parameters have been given!")
                    elif (len(statement) > 7):
                        print("Too many parameters have been given!")
                else:
                    print("Invalid Command")
            else:
                print("Invalid Command")
        elif beginsWith(command, "pause"):
            os.system("pause")
        elif beginsWith(command, "timeout "):
            statement = command.split(" ")
            os.system("timeout " + statement[1])
        elif beginsWith(command, "clear"):
            statement = command.split(" ")

            if (len(statement) > 1):
                if (statement[1] == "graph"):
                    graphCalc.clear()
                else:
                    print("Invalid Command")
            else:
                os.system("cls")
        elif (command == "exit"):
            if graphCalc.getState():
                graphCalc.stop()
                
            retVal = True
        else:
            print("" + command + " = " + str(graphCalc.calculate(command)))

    return (retVal)

def cmdLine(userInput):
    # Iterates through each command in a list of commands and evaluates them with the parseCommand() function.
    # Example: cmdLine(["var n = 100", "const s = 2", "function summation(x) = (x + x ^ s) / s", "summation(n)"]) will
    # set the variable n to equal 100, set the constant s to equal 2, set the definition of summation(x) to equal "(x + x ^ s) / s", evaluate summation(n) and print summation(x) = 5050.0 on the screen.
    retVal      = False
    commandList = getCommandList(userInput)

    for command in commandList:
        if parseCommand(command):
            retVal = True
            break

    return (retVal)

def removeComments(line):
    # Removes commented sections of text from the script being read by this code.
    # Example: removeComments("var n = 100//Variable Declaration") will return "var n = 100".
    # Example: removeComments("//This is a comment.") will return "".
    retVal = line[0]
    i      = 1
    
    while (i < len(line)):
        if ((line[i] + line[i - 1]) == "//"):
            retVal = retVal[:-1]
            break
        else:
            retVal += line[i]
        i += 1

    return (retVal)

showCommands = True #This is is a global variable that is used to determine whether or not to display the commands in the script being read by this program.

# The following code is free code that is not contained within a function or a class.
if (len(sys.argv) == 1):
    # If the length of the arguments list passed to the program only contains the program's name then no arguments were passed.
    # The program executes on its own.
    while (True):
        print("Math >", end = " ")
        if cmdLine(input()):
            break
else:
    # If more than just the program name was passed to the program, then it should be opening a script file.
    file = open(sys.argv[1]).read().split('\n')

    for line in file:
        if (len(line) > 0):
            if not beginsWith(line, "//"):
                if beginsWith(line, "hide "):
                    statement = line.split(' ')

                    if (statement[1] == "commands"):
                        showCommands = False
                elif beginsWith(line, "show "):
                    statement = line.split(' ')

                    if(statement[1] == "commands"):
                        showCommands = True
                else:
                    command = removeComments(line)
                    
                    if showCommands:
                        print(command)
                        
                    cmdLine(command) # Commands are sent to the cmdLine() function to be executed by the program line by line.

    print("\n")

#This code supports custom functions with more than 1 parameter.
#This code does not support parsing it yet though.
#The code below should work if ran in the python terminal.
#
#graphCalc = GraphingCalculator()
#graphCalc.setFunction("f(x, s)", "x^s")
#print(graphCalc.evaluateFunction("f(6, 2)"))



















































