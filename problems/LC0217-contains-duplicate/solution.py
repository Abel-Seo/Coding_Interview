"""
LC0217 — contains-duplicate
https://leetcode.com/problems/contains-duplicate/

유형: array, hash-set
난이도: Easy

접근법:
    - set에 넣으면서 이미 있는지 체크
    - set의 lookup은 O(1)이므로 전체 O(n)

시간복잡도: O(n)
공간복잡도: O(n)
"""


def contains_duplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
