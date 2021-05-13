import re
import math

manual = """\033[94m\nYou can use:\n
    x^y
    x * y%, to find y percent from x
    sqrt(x)
    sin(x)
    cos(x)
    tan(x)
    factorial(x)
    pi
    e\n
    Print \'rad\' or \'deg\' to switch on appropriate measure\n
To use these operation\n\033[0m
"""

class Angel:
    __measure = 'rad'

    def getMeasure(self):
        return self.__measure

    def setMeasure(self, measure):
        self.__measure = measure

angel = Angel()

def replaceFormulas(expression, str):
    roots = re.findall(re.compile(str + '\(.+\)'), expression)
    parsedExp = expression

    for root in roots:
        group = re.compile(str + '\((.+)\)').match(root).groups()[0]
        replaceStr = 'math.' + str + '(' + group + ')'

        if re.compile('sin|cos|tan').search(expression):
            value = (group if angel.getMeasure() == 'rad' else group + '* (math.pi / 180)')
            replaceStr = 'math.' + str + '(' + value + ')'


        parsedExp = parsedExp.replace(root, replaceStr)

    return parsedExp

def checkFormula(formula, expression):
    parsedExp = expression

    if re.compile(formula).search(expression):
        parsedExp = replaceFormulas(expression, formula)

    return parsedExp

def checkOneCharFormula(expression):
    parsedExp = expression

    if re.compile('\^').search(expression):
        parsedExp = expression.replace('^', '**')

    if re.compile('pi').search(expression):
        parsedExp = expression.replace('pi', 'math.pi')

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
    expression = input('(' + angel.getMeasure() + ') ' + 'Enter an expression (input \'c\' to clear, \'m\' to get manual of commands): ')

    if expression.lower() == 'c':
        print('\033[H\033[J')
        start()
    elif expression.lower() == 'm':
        print(manual)
        start()
    elif expression.lower() == 'rad' or expression.lower() == 'deg':
        angel.setMeasure(expression.lower())
        print('\033[94m\nSwitched to ' + expression.lower() + ' \n\033[0m')
        start()
    else:
        expression = checkFormula('sqrt', expression)
        expression = checkFormula('sin', expression)
        expression = checkFormula('cos', expression)
        expression = checkFormula('tan', expression)
        expression = checkFormula('factorial', expression)
        expression = checkOneCharFormula(expression)
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
    except ValueError:
        onCatch('There is not allowed to get square root from negative number')
    except KeyboardInterrupt:
        print('\n\nProgramm ended')

start()