
import pytest

from natasha.obj import Date


tests = [
    [
        '24.01.2017',
        Date(2017, 1, 24)
    ],
    [
        '27. 05.99',
        Date(1999, 5, 27)
    ],
    [
        '2015 год',
        Date(2015)
    ],
    [
        '2014 г',
        Date(2014)
    ],
    [
        '1 апреля',
        Date(None, 4, 1)
    ],
    [
        'май 2017 г.',
        Date(2017, 5)
    ],
    [
        '9 мая 2017 года',
        Date(2017, 5, 9)
    ],
]


@pytest.mark.parametrize('test', tests)
def test_extractor(dates_extractor, test):
    text, target = test
    pred = dates_extractor.find(text).fact
    assert pred == target
