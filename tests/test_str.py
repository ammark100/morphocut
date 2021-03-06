from morphocut import Pipeline
from morphocut.str import Format
from morphocut.str import Parse

import pytest

try:
    import parse
    del parse
    PARSE_AVAILABLE = True
except ImportError:
    PARSE_AVAILABLE = False


def test_Format():
    # Assert that the arguments are appended in the right order
    fmt = "{},{},{},{},{},{},{a},{b},{c},{d}"
    args = (1, 2, 3)
    _args = (4, 5, 6)
    _kwargs = {"a": 7, "b": 8}
    kwargs = {"c": 9, "d": 10}

    with Pipeline() as pipeline:
        result = Format(fmt, *args, _args=_args, _kwargs=_kwargs, **kwargs)

    stream = pipeline.transform_stream()
    obj = next(stream)

    assert obj[result] == "1,2,3,4,5,6,7,8,9,10"

    # Assert that the keyword arguments replace as expected
    fmt = "{a},{b}"
    _kwargs = {"a": 1, "b": 2}
    kwargs = {"a": 3, "b": 4}

    with Pipeline() as pipeline:
        result = Format(fmt, _kwargs=_kwargs, **kwargs)

    stream = pipeline.transform_stream()
    obj = next(stream)

    assert obj[result] == "3,4"


@pytest.mark.skipif(not PARSE_AVAILABLE, reason="requires parse.")
def test_Parse():
    # Assert that the string given is rightly parsed
    pattern = "This is a {named}"
    string = "This is a TEST"
    case_sensitive = True

    with Pipeline() as pipeline:
        result = Parse(pattern, string, case_sensitive)

    stream = pipeline.transform_stream()
    obj = next(stream)

    assert obj[result] == {'named': 'TEST'}
