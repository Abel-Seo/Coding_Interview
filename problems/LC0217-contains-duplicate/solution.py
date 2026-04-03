from typing import List

"""
LC0217 — Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

유형: Array, Hash Table, Sorting
난이도: Easy

접근법:
    -

시간복잡도: O()
공간복잡도: O()
"""


# ── LeetCode 제출용 ─────────────────────────────────────────
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False
        pass


# ── 로컬 테스트용 래퍼 ────────────────────────────────────────
def contains_duplicate(nums):
    return Solution().containsDuplicate(nums)
