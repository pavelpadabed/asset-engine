from domain.hash import FileHash
import pytest

original_hash = "ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890"

def test_hash_normalize_lower():
    file_hash = FileHash(original_hash)
    assert file_hash.value == original_hash.lower()


def test_raise_value_error_not_string():
    with pytest.raises(ValueError):
        FileHash(1234)


def test_raise_value_error_incorrect_length():
    incorrect_hash = original_hash[:-1]
    with pytest.raises(ValueError):
        FileHash(incorrect_hash)


def test_raise_value_error_incorrect_hex():
    incorrect_hash = original_hash.lower().replace("a", "g", 1)
    with pytest.raises(ValueError):
        FileHash(incorrect_hash)

