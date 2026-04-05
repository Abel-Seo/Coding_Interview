from typing import List

"""
LC0001 — Two Sum
https://leetcode.com/problems/two-sum/

유형: Array, Hash Table
난이도: Easy

접근법:
    -

시간복잡도: O()
공간복잡도: O()
"""


# ── LeetCode 제출용 ─────────────────────────────────────────
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dict = {}

        for idx, val in enumerate(nums):
            complement = target - val

            if complement in dict:
                return [dict[complement], idx]
            dict[val] = idx
        pass


# ── 로컬 테스트용 래퍼 ────────────────────────────────────────
def two_sum(nums, target):
    return Solution().twoSum(nums, target)
