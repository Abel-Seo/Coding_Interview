"""Tests for LC0001 — Two Sum"""
import pytest
from solution import two_sum


@pytest.mark.parametrize("nums, target, expected", [
    ([2,7,11,15], 9, [0,1]),
    ([3,2,4], 6, [1,2]),
    ([3,3], 6, [0,1]),
])
def test_examples(nums, target, expected):
    assert two_sum(nums, target) == expected


# ── Edge Cases ─────────────────────────────────────────────


def test_edge_empty_list():
    # 빈 리스트
    result = two_sum([], 1)
    assert result is not None  # TODO: expected 값 채우기


def test_edge_single_element():
    # 원소 1개
    result = two_sum([1], 1)
    assert result is not None  # TODO: expected 값 채우기

