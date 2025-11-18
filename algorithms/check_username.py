import re

def is_valid_string(s: str) -> bool:
    # ^ start, $ end → ensures the whole string matches
    # [a-z0-9_]+ → only lowercase letters, digits, and underscores
    return bool(re.fullmatch(r"[a-z0-9_]+", s))

# Examples
while True:
    string = input("String: ")
    print(is_valid_string(string))
    print()