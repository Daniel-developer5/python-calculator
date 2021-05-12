import re
import math

manual = """\033[94m\nYou can use:\n
    x^a
    x * 10%, to find a percent from x
    sqrt(x)
    sin(x)
    cos(x)
    tan(x)
    factorial(x)\n
To use these operation\n\033[0m
"""

def replaceFormulas(expression, str):
    roots = re.findall(re.compile(str + '\(.+\)'), expression)
    parsedExp = expression

    for root in roots:
        group = re.compile(str + '\((.+)\)').match(root).groups()[0]
        parsedExp = parsedExp.replace(root, 'math.' + str + '(' + group + ')')

    return parsedExp

def checkFormula(formula, expression):
    parsedExp = expression

    if re.compile(formula).search(expression):
        parsedExp = replaceFormulas(expression, formula)

    return parsedExp

def checkDegree(expression):
    parsedExp = expression

    if re.compile('\^').search(expression):
        parsedExp = expression.replace('^', '**')

    return parsedExp

def checkPercent(expression):
    parsedExp = expression
    regExp = '\*\s?\d+%'

    if re.compile(regExp).search(expression):
        percents = re.findall(re.compile(regExp), expression)

        for percent in percents:
            group = re.compile('\*\s?(\d+)%').match(percent).groups()[0]
            parsedExp = parsedExp.replace(percent, '/ 100 * ' + str(group))

    return parsedExp

def calculate():
    expression = input('Enter an expression (input \'c\' to clear, \'m\' to get manual of commands): ')

    if expression.lower() == 'c':
        print('\033[H\033[J')
        start()
    elif expression.lower() == 'm':
        print(manual)
        start()
    else:
        expression = checkFormula('sqrt', expression)
        expression = checkFormula('sin', expression)
        expression = checkFormula('cos', expression)
        expression = checkFormula('tan', expression)
        expression = checkFormula('factorial', expression)
        expression = checkDegree(expression)
        expression = checkPercent(expression)

        print(eval(expression))
        start()

def onCatch(errorText):
    print('\n\033[91m' + errorText + '\033[0m\n')
    start() 

def start(): 
    try:
        calculate()
    except ZeroDivisionError:
        onCatch('There is not allowed to divide on zero')
    except NameError:
        onCatch('Expression is not valid')
    except SyntaxError:
        onCatch('Expression is not valid')
    except KeyboardInterrupt:
        print('\n\nProgramm ended')

start()