from typing import List

"""
LC0049 — Group Anagrams
https://leetcode.com/problems/group-anagrams/

유형: Array, Hash Table, String, Sorting
난이도: Medium

접근법:
    -

시간복잡도: O()
공간복잡도: O()
"""


# ── LeetCode 제출용 ─────────────────────────────────────────
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}

        for val in strs:
            cur = tuple(sorted(val))
            if cur in groups:
                groups[cur].append(val)
            else:
                groups[cur] = [val]

        return list(groups.values())
        pass


# ── 로컬 테스트용 래퍼 ────────────────────────────────────────
def group_anagrams(strs):
    return Solution().groupAnagrams(strs)
