# coding: utf-8
from __future__ import unicode_literals, print_function


TABLE = [
    ('<', '&lt;'),
    ('>', '&gt;'),
]


def escape(text):
    for char, code in TABLE:
        text = text.replace(char, code)
    return text


def format_markup_html(text, spans):
    spans = sorted(spans)
    previous = 0
    for span in spans:
        start, stop = span
        yield escape(text[previous:start])
        yield '<mark>'
        yield escape(text[start:stop])
        yield '</mark>'
        previous = stop
    yield escape(text[previous:])


def format_markup_css(text, spans):
    yield '<style>'
    yield """

.markup {
    white-space: pre-wrap;
}

.markup > mark {
    line-height: 1;
    display: inline-block;
    border-radius: 0.25em;
    border: 1px solid #fdf07c;
    background: #ffffc2;
}
    """
    yield '</style>'
    yield '<div class="markup tex2jax_ignore">'
    yield ''.join(format_markup_html(text, spans))
    yield '</div>'


def show_markup_notebook(text, spans):
    from IPython.display import HTML, display

    html = ''.join(format_markup_css(text, spans))
    display(HTML(html))


def format_markup(text, spans):
    spans = sorted(spans)
    previous = 0
    for span in spans:
        start, stop = span
        yield text[previous:start]
        yield '[['
        yield text[start:stop]
        yield ']]'
        previous = stop
    yield text[previous:]


def show_markup(text, spans):
    print(''.join(format_markup(text, spans)))


def format_json(data):
    import json

    return json.dumps(data, indent=2, ensure_ascii=False)


def show_json(data):
    print(format_json(data))
