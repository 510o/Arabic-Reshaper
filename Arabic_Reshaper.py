from unicodedata import lookup, combining, name as chartype; import importlib.util
from itertools import takewhile; from urllib.request import Request, urlopen

def reshape(text: str, harakat: bool = True, get_display: bool = False) -> str:
    data = {}; [data.__setitem__(l[2], chr(int(l[0], 16)) + data.get(l[2], '')) for l in ([x.strip() for x in line.split(';')] for line in urlopen(Request("https://www.unicode.org/Public/UCD/latest/ucd/ArabicShaping.txt", headers={"User-Agent": "Mozilla/5.0"})).read().decode().splitlines() if line.strip() and not line.startswith('#'))]
    if not harakat: text = clear_movements(text)
    reshape_text = list(text)
    for i, letter in enumerate(text):
        if letter in data['D']+data['R']:
            _k = 1 + sum(1 for _ in takewhile(lambda c: combining(c), (text[j] for j in range(i-1, -1, -1))))
            k_ = 1 + sum(1 for _ in takewhile(lambda c: combining(c), (text[j] for j in range(i+1, len(text)))))
            _letter, letter_ = [l for l in [text[i - _k] if i > 0 else None, text[i + k_] if i + k_ < len(text) else None]]
            Connect = 0
            if _letter and _letter in data['D']+data['L']+data['C']: Connect += 1
            if letter in data['D'] and letter_ and letter_ in data['D']+data['R']+data['C']: Connect += 2
            reshape_text[i] = chr(ord(isolated(letter)) + Connect)
    if get_display: reshape_text = getdisplay(''.join(reshape_text))
    else: reshape_text = ''.join(reshape_text)
    return reshape_text

def getdisplay(text: str):
    if not importlib.util.find_spec(lib):
        from sys import executable; from subprocess import check_call
        check_call([executable, "-m", "pip", "install", "python-bidi"])
    from bidi.algorithm import  get_display; return get_display(text)

def clear_movements(text: str) -> str: return ''.join([letter for letter in text if not combining(letter)])
def isolated(l):
        try: return lookup(chartype(l) + " ISOLATED FORM")
        except (LookupError, ValueError, TypeError): return None

print(reshape(input())[::-1])