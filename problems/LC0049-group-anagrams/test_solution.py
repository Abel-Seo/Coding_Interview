"""Tests for LC0049 — Group Anagrams"""
import pytest
from solution import group_anagrams


@pytest.mark.parametrize("strs, expected", [
    (["eat","tea","tan","ate","nat","bat"], [["bat"],["nat","tan"],["ate","eat","tea"]]),
    ([""], [[""]]),
    (["a"], [["a"]]),
])
def test_examples(strs, expected):
    assert group_anagrams(strs) == expected


# ── Edge Cases ─────────────────────────────────────────────


def test_edge_single_element():
    # 원소 1개
    result = group_anagrams([1])
    assert result is not None  # TODO: expected 값 채우기

