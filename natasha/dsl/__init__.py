

class Normalizable(object):
    pass


def can_be_normalized(item):
    return isinstance(item, Normalizable)
