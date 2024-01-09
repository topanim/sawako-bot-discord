def none_if_empty(val: str):
    if val.strip() == '':
        return
    return val


def are_characters_unique(s):
    seen = set()
    for char in s:
        if char in seen:
            return False
        seen.add(char)
    return True
