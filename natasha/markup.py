# coding: utf-8
from __future__ import unicode_literals


TABLE = [
    ('<', '&lt;'),
    ('>', '&gt;'),
]


def escape(text):
    for char, code in TABLE:
        text = text.replace(char, code)
    return text


def format_markup_(text, spans):
    # TODO Check and do something with intersecting
    spans = sorted(spans)
    previous = 0
    for index, span in enumerate(spans):
        start, stop = span
        yield escape(text[previous:start])
        yield '<mark>'
        yield escape(text[start:stop])
        yield '<span class="index">'
        yield str(index)
        yield '</span>'
        yield '</mark>'
        previous = stop
    yield escape(text[previous:])


def format_markup(text, spans):
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

.markup > mark > .index {
    font-size: 0.7em;
    vertical-align: top;
    margin-left: 0.1em;
}
    """
    yield '</style>'
    yield '<div class="markup tex2jax_ignore">'
    yield ''.join(format_markup_(text, spans))
    yield '</div>'


def show_markup(text, spans):
    from IPython.display import HTML, display

    html = ''.join(format_markup(text, spans))
    display(HTML(html))
