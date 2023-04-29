'''
generate.py is used to generate variables of a specific class
'''
import random
import math

def __generateDigits(numDigits: int) -> int:
    return random.randrange(0,int(math.pow(10,numDigits)))

def __generateUnicodeString(numChars) -> str:
    '''Generates a random unicode string. Code from: https://stackoverflow.com/questions/1477294/generate-random-utf-8-string-in-python'''
    try:
        get_char = unichr
    except NameError:
        get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [
        ( 0x0021, 0x0021 ),
        ( 0x0023, 0x0026 ),
        ( 0x0028, 0x007E ),
        ( 0x00A1, 0x00AC ),
        ( 0x00AE, 0x00FF ),
        ( 0x0100, 0x017F ),
        ( 0x0180, 0x024F ),
        ( 0x2C60, 0x2C7F ),
        ( 0x16A0, 0x16F0 ),
        ( 0x0370, 0x0377 ),
        ( 0x037A, 0x037E ),
        ( 0x0384, 0x038A ),
        ( 0x038C, 0x038C ),
    ]

    alphabet = [
        get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return ''.join(random.choice(alphabet) for i in range(numChars)) 

def NUMBER(precision: int, scale: int) -> str:
    wholeNumLen = precision-scale

    wholeNum = __generateDigits(wholeNumLen)
    if scale == 0:
        return wholeNum
    decimalNum = __generateDigits(scale)

    return f'{wholeNum}.{decimalNum}'

def NVARCHAR2(size: int) -> str:
    size = random.randint(1,size)
    return __generateUnicodeString(size)

def NCHAR(size:int) -> str:
    # TODO: handle the national dataset difference, and hence the number of characters allowed: https://www.oracletutorial.com/oracle-basics/oracle-nchar/
    return __generateUnicodeString(size)

def INTEGER() -> int:
    return NUMBER(38,0)

def CHAR(size) ->str:
    return __generateUnicodeString(size)

def DATE() -> str:
    