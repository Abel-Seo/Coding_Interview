"""
LC0242 — Valid Anagram
https://leetcode.com/problems/valid-anagram/

유형: Hash Table, String, Sorting
난이도: Easy

접근법:
    -

시간복잡도: O()
공간복잡도: O()
"""

# ── LeetCode 제출용 ─────────────────────────────────────────
from collections import Counter

# class Solution:
#     def isAnagram(self, s: str, t: str) -> bool:
#         if len(s) != len(t):
#             return False

#         s_dict = {}
#         t_dict = {}

#         for char1 in s:
#             s_dict[char1] = s_dict.get(char1, 0) + 1
#         for char2 in t:
#             t_dict[char2] = t_dict.get(char2, 0) + 1

#         return s_dict == t_dict
#         pass


# Another Solution
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)


# ── 로컬 테스트용 래퍼 ────────────────────────────────────────
def valid_anagram(s, t):
    return Solution().isAnagram(s, t)
