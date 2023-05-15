'''
generate.py is used to generate variables of a specific class
'''
from datetime import datetime
import random
import math


def __generateDigits(numDigits: int) -> int:
    return random.randrange(0, int(math.pow(10, numDigits)))


def __generateUnicodeString(numChars) -> str:
    '''Generates a random unicode string. Code from: https://stackoverflow.com/questions/1477294/generate-random-utf-8-string-in-python'''
    try:
        get_char = unichr
    except NameError:
        get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [
        (0x0041, 0x005A),
        (0x0061, 0x007A),
    ]

    alphabet = [
        get_char(code_point) for current_range in include_ranges
        for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return ''.join(random.choice(alphabet) for i in range(numChars))


def NUMBER(precision: int, scale: int, minValue=0, maxValue=None) -> str:
    # TODO: constrain a min and max range
    wholeNumLen = precision-scale

    wholeNum = __generateDigits(wholeNumLen)
    if scale == 0:
        return wholeNum
    decimalNum = __generateDigits(scale)

    return f'{wholeNum}.{decimalNum}'


def NVARCHAR2(size: int) -> str:
    size = random.randint(1, size)
    return __generateUnicodeString(size)


def NCHAR(size: int) -> str:
    # TODO: handle the national dataset difference, and hence the number of characters allowed: https://www.oracletutorial.com/oracle-basics/oracle-nchar/
    return __generateUnicodeString(size)


def INTEGER(minValue=0, maxValue=None) -> int:
    return NUMBER(38, 0, minValue, maxValue)


def CHAR(size) -> str:
    return __generateUnicodeString(size)


def DATE(startDateTimestamp=431995, endDateTimestamp=None) -> str:
    if endDateTimestamp is None:
        endDateTimestamp = datetime.timestamp(datetime.now())
    return datetime.fromtimestamp(random.randrange(int(startDateTimestamp), int(endDateTimestamp))).strftime("%Y-%m-%d")


def FROM(data) -> any:
    if len(data) < 2:
        return data
    return data[random.randint(0, len(data)-1)]


def EMAIL() -> str:
    # From https://www.askpython.com/python/examples/email-address-generator
    validchars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    validoms = 'abcdefghijklmnopqrstuvwxyz'
    login = ''
    server = ''
    loginlen = random.randint(4, 15)
    serverlen = random.randint(3, 9)
    tldlen = random.randint(2, 3)
    tld = ''
    for _ in range(loginlen):
        pos = random.randint(0, len(validchars)-1)
        login = login+validchars[pos]
    if login[0].isnumeric():
        pos = random.randint(0, len(validchars)-10)
        login = validchars[pos]+login
    for _ in range(serverlen):
        pos = random.randint(0, len(validoms)-1)
        server = server+validoms[pos]
    for _ in range(tldlen):
        pos = random.randint(0, len(validoms)-1)
        tld = tld+validoms[pos]
    return login+'@'+server+'.'+tld


def RANDRANGE(start: int, stop: int | None = None, step: int = 1):
    """Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        """

    if start == stop:
        return start

    return random.randrange(start, stop, step)
