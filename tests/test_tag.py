from domain.tag import Tag
import pytest

test_tag = "  My_Tag-1  "

def test_tag_lower_strip():
    file_tag = Tag(test_tag)
    assert file_tag.value == test_tag.lower().strip()


def test_raise_value_error_empty_string():
    incorrect_tag = " "
    with pytest.raises(ValueError):
        Tag(incorrect_tag)


def test_raise_value_error_above_max_length():
    incorrect_tag = "r" * 33
    with pytest.raises(ValueError):
        Tag(incorrect_tag)


def test_raise_value_error_incorrect_symbols():
    incorrect_tag = "@my_tag%"
    with pytest.raises(ValueError):
        Tag(incorrect_tag)
