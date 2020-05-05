
from collections import OrderedDict


def parse_annotation(annotation):
    type = annotation or str

    repeatable = False
    if isinstance(annotation, list):  # [Fact]
        repeatable = True
        type = annotation[0]

    is_record = issubclass(type, Record)

    return type, repeatable, is_record


class Record(object):
    __attributes__ = []
    __annotations__ = {}

    def __init__(self, *args, **kwargs):
        for key, value in zip(self.__attributes__, args):
            self.__dict__[key] = value
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and all(
                (getattr(self, _) == getattr(other, _))
                for _ in self.__attributes__
            )
        )

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return (getattr(self, _) for _ in self.__attributes__)

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(
            '{key}={value!r}'.format(
                key=_,
                value=getattr(self, _)
            )
            for _ in self.__attributes__
        )
        return '{name}({args})'.format(
            name=name,
            args=args
        )

    def _repr_pretty_(self, printer, cycle):
        name = self.__class__.__name__
        if cycle:
            printer.text('{name}(...)'.format(name=name))
        else:
            printer.text('{name}('.format(name=name))
            keys = self.__attributes__
            size = len(keys)
            if size:
                with printer.indent(4):
                    printer.break_()
                    for index, key in enumerate(keys):
                        printer.text(key + '=')
                        value = getattr(self, key)
                        printer.pretty(value)
                        if index < size - 1:
                            printer.text(',')
                            printer.break_()
                printer.break_()
            printer.text(')')

    @property
    def as_json(self):
        data = OrderedDict()
        for key in self.__attributes__:
            annotation = self.__annotations__.get(key)
            _, repeatable, is_record = parse_annotation(annotation)

            value = getattr(self, key)
            if value is None:
                continue

            if repeatable and is_record:
                value = [_.as_json for _ in value]
            elif is_record:
                value = value.as_json

            data[key] = value
        return data

    @classmethod
    def from_json(cls, data):
        args = []
        for key in cls.__attributes__:
            annotation = cls.__annotations__.get(key)
            type, repeatable, is_record = parse_annotation(annotation)
            value = data.get(key)
            if value is None and repeatable:
                value = []
            elif value is not None:
                if repeatable and is_record:
                    value = [type.from_json(_) for _ in value]
                elif is_record:
                    value = type.from_json(value)
            args.append(value)
        return cls(*args)
