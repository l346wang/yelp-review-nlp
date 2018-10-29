import re
from constants import SYMBOLS_REGEX
symbols_patter = re.compile(SYMBOLS_REGEX)
print(symbols_patter.match('.'))
print(re.match(SYMBOLS_REGEX, "asfasd#!f.afdfsd"))