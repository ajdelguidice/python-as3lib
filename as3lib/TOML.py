'''
A simple TOML reader/writer for as3lib. This implementation was created out of
frustration at tomli_w's formatting (mostly the arrays) and only implements
things needed for this library. It is not guaranteed to work for other use
cases.
'''
from io import StringIO
from pathlib import PurePath
import platform
import sys
if sys.hexversion < 0x030b0000:
    import tomli

    readFile = tomli.load
    readString = tomli.loads
else:
    import tomllib

    readFile = tomllib.load
    readString = tomllib.loads


def Value(value):
    if isinstance(value, PurePath):
        value = str(value)
        if platform.system() == 'Windows':
            # workaround: tomli does not parse windows paths correctly.
            # Must use / instead of \
            value = value.replace('\\', '/')
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (list, tuple)):
        return Array(value)
    if isinstance(value, dict):
        return Table(value)
    return f'{value}'


def Table(value):
    with StringIO() as text:
        text.write('{')
        for k, v in value.items():
            text.write(f'{k} = {Value(v)},')
        temp = text.getvalue()
        if temp.endswith(','):  # TODO: Make this better
            return temp[:-1] + '}'
        return temp + '}'


def Array(value):
    with StringIO() as text:
        text.write('[')
        for i in value:
            text.write(f'{Value(i)},')
        text.write(']')
        return text.getvalue()


def dictToTOML(valDict):
    nontables = []
    tables = []
    for k, v in valDict.items():
        if isinstance(v, dict):
            tables.append(k)
        else:
            nontables.append(k)
    with StringIO() as text:
        for k in nontables:
            text.write(f'{k} = {Value(valDict[k])}\n')
        for k in tables:
            text.write(f'\n["{k}"]\n' if str(k).find('.') != -1 else f'\n[{k}]\n')
            for k2, v2 in valDict[k].items():
                text.write(f'{k2} = {Value(v2)}\n')
        return text.getvalue()


Return = dictToTOML


def write(file, valDict, mode='w'):
    with open(file, mode) as f:
        f.write(dictToTOML(valDict))
