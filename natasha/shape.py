
import re


ALPHA = 'alpha'
NONALPHA = 'nonalpha'

SHAPE_PART = re.compile(r'''
(?P<alpha>[а-яёa-z]+)
|(?P<nonalpha>[^а-яёa-z]+)
''', re.I | re.X)


class ShapeRecoverError(Exception):
    pass


def shape_parts(word):
    matches = SHAPE_PART.finditer(word)
    for match in matches:
        yield match.lastgroup, match.group(0)


def recover_part_shape(part, ref):
    if ref.islower():
        return part.lower()
    elif ref.isupper():
        return part.upper()
    elif ref.istitle():
        return part.capitalize()
    else:
        raise ShapeRecoverError


def recover_shape_(word, ref):
    if word.lower() == ref.lower():
        yield ref
        return

    parts = list(shape_parts(word))
    ref_parts = list(shape_parts(ref))
    if len(parts) != len(ref_parts):
        raise ShapeRecoverError

    for (type, part), (ref_type, ref_part) in zip(parts, ref_parts):
        if type != ref_type:
            raise ShapeRecoverError

        if type == ALPHA:
            yield recover_part_shape(part, ref_part)
        else:
            yield part


def recover_shape(word, ref):
    try:
        parts = recover_shape_(word, ref)
        return ''.join(parts)
    except ShapeRecoverError:
        return word
