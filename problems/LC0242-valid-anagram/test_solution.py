"""Tests for LC0242 — Valid Anagram"""
import pytest
from solution import valid_anagram


@pytest.mark.parametrize("s, t, expected", [
    ("anagram", "nagaram", True),
    ("rat", "car", False),
])
def test_examples(s, t, expected):
    assert valid_anagram(s, t) == expected


# ── Edge Cases ─────────────────────────────────────────────


def test_edge_single_char():
    # 한 글자
    result = valid_anagram("a", "a")
    assert result is not None  # TODO: expected 값 채우기

