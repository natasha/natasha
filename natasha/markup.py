# coding: utf-8
from __future__ import unicode_literals, print_function


def assert_ipymarkup():
    try:
        import ipymarkup
    except ImportError:
        raise ImportError('pip install ipymarkup')


def get_markup_notebook(text, spans):
    assert_ipymarkup()
    from ipymarkup import BoxMarkup, Span
    from IPython.display import display

    spans = [Span(start, stop) for start, stop in spans]
    return BoxMarkup(text, spans)


def show_markup_notebook(text, spans):
    markup = get_markup_notebook(text, spans)
    display(markup)


def show_markup(text, spans):
    assert_ipymarkup()
    from ipymarkup import AsciiMarkup, Span

    spans = [Span(start, stop) for start, stop in spans]
    markup = AsciiMarkup(text, spans)
    for line in markup.as_ascii:
        print(line)


def format_json(data):
    import json

    return json.dumps(data, indent=2, ensure_ascii=False)


def show_json(data):
    print(format_json(data))
