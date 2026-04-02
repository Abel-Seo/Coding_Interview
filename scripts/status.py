"""
오늘 날짜 기준 진행 상황 확인

사용법:
    python scripts/status.py
    make status
"""

import os
import glob
from datetime import date

# ── NeetCode 150 일정 ────────────────────────────────────────
STAGES = [
    {
        "stage": 1,
        "category": "Arrays & Hashing",
        "start": date(2026, 4, 1),
        "end": date(2026, 4, 20),
        "problems": [
            (217, "Contains Duplicate"),
            (242, "Valid Anagram"),
            (1, "Two Sum"),
            (49, "Group Anagrams"),
            (347, "Top K Frequent Elements"),
            (238, "Product of Array Except Self"),
            (36, "Valid Sudoku"),
            (271, "Encode and Decode Strings"),
            (128, "Longest Consecutive Sequence"),
        ],
    },
    {
        "stage": 2,
        "category": "Two Pointers",
        "start": date(2026, 4, 21),
        "end": date(2026, 5, 4),
        "problems": [
            (125, "Valid Palindrome"),
            (167, "Two Sum II"),
            (15, "3Sum"),
            (11, "Container With Most Water"),
            (42, "Trapping Rain Water"),
        ],
    },
    {
        "stage": 3,
        "category": "Sliding Window",
        "start": date(2026, 5, 5),
        "end": date(2026, 5, 18),
        "problems": [
            (121, "Best Time to Buy and Sell Stock"),
            (3, "Longest Substring Without Repeating Characters"),
            (424, "Longest Repeating Character Replacement"),
            (567, "Permutation in String"),
            (76, "Minimum Window Substring"),
            (239, "Sliding Window Maximum"),
        ],
    },
    {
        "stage": 4,
        "category": "Stack",
        "start": date(2026, 5, 19),
        "end": date(2026, 6, 8),
        "problems": [
            (20, "Valid Parentheses"),
            (155, "Min Stack"),
            (150, "Evaluate Reverse Polish Notation"),
            (22, "Generate Parentheses"),
            (739, "Daily Temperatures"),
            (853, "Car Fleet"),
            (84, "Largest Rectangle in Histogram"),
        ],
    },
    {
        "stage": 5,
        "category": "Binary Search",
        "start": date(2026, 6, 9),
        "end": date(2026, 6, 29),
        "problems": [
            (704, "Binary Search"),
            (74, "Search a 2D Matrix"),
            (875, "Koko Eating Bananas"),
            (33, "Search in Rotated Sorted Array"),
            (153, "Find Minimum in Rotated Sorted Array"),
            (981, "Time Based Key-Value Store"),
            (4, "Median of Two Sorted Arrays"),
        ],
    },
    {
        "stage": 6,
        "category": "Linked List",
        "start": date(2026, 6, 30),
        "end": date(2026, 7, 26),
        "problems": [
            (206, "Reverse Linked List"),
            (21, "Merge Two Sorted Lists"),
            (143, "Reorder List"),
            (19, "Remove Nth Node From End of List"),
            (138, "Copy List with Random Pointer"),
            (2, "Add Two Numbers"),
            (141, "Linked List Cycle"),
            (287, "Find the Duplicate Number"),
            (146, "LRU Cache"),
            (23, "Merge k Sorted Lists"),
            (25, "Reverse Nodes in k-Group"),
        ],
    },
    {
        "stage": 7,
        "category": "Trees",
        "start": date(2026, 7, 27),
        "end": date(2026, 8, 16),
        "problems": [
            (226, "Invert Binary Tree"),
            (104, "Maximum Depth of Binary Tree"),
            (543, "Diameter of Binary Tree"),
            (110, "Balanced Binary Tree"),
            (100, "Same Tree"),
            (572, "Subtree of Another Tree"),
            (235, "Lowest Common Ancestor of a BST"),
            (102, "Binary Tree Level Order Traversal"),
            (199, "Binary Tree Right Side View"),
            (1448, "Count Good Nodes in Binary Tree"),
            (98, "Validate Binary Search Tree"),
            (230, "Kth Smallest Element in a BST"),
            (105, "Construct Binary Tree from Preorder and Inorder Traversal"),
            (124, "Binary Tree Maximum Path Sum"),
            (297, "Serialize and Deserialize Binary Tree"),
        ],
    },
    {
        "stage": 8,
        "category": "Tries",
        "start": date(2026, 8, 17),
        "end": date(2026, 8, 23),
        "problems": [
            (208, "Implement Trie (Prefix Tree)"),
            (211, "Design Add and Search Words Data Structure"),
            (212, "Word Search II"),
        ],
    },
    {
        "stage": 9,
        "category": "Heap / Priority Queue",
        "start": date(2026, 8, 24),
        "end": date(2026, 9, 6),
        "problems": [
            (703, "Kth Largest Element in a Stream"),
            (1046, "Last Stone Weight"),
            (973, "K Closest Points to Origin"),
            (215, "Kth Largest Element in an Array"),
            (621, "Task Scheduler"),
            (355, "Design Twitter"),
            (295, "Find Median from Data Stream"),
        ],
    },
    {
        "stage": 10,
        "category": "Backtracking",
        "start": date(2026, 9, 7),
        "end": date(2026, 9, 20),
        "problems": [
            (78, "Subsets"),
            (39, "Combination Sum"),
            (46, "Permutations"),
            (90, "Subsets II"),
            (40, "Combination Sum II"),
            (79, "Word Search"),
            (131, "Palindrome Partitioning"),
            (17, "Letter Combinations of a Phone Number"),
            (51, "N-Queens"),
        ],
    },
    {
        "stage": 11,
        "category": "Graphs",
        "start": date(2026, 9, 21),
        "end": date(2026, 10, 11),
        "problems": [
            (200, "Number of Islands"),
            (133, "Clone Graph"),
            (695, "Max Area of Island"),
            (417, "Pacific Atlantic Water Flow"),
            (130, "Surrounded Regions"),
            (994, "Rotting Oranges"),
            (286, "Walls and Gates"),
            (207, "Course Schedule"),
            (210, "Course Schedule II"),
            (684, "Redundant Connection"),
            (323, "Number of Connected Components in an Undirected Graph"),
            (261, "Graph Valid Tree"),
            (127, "Word Ladder"),
        ],
    },
    {
        "stage": 12,
        "category": "Advanced Graphs",
        "start": date(2026, 10, 12),
        "end": date(2026, 10, 22),
        "problems": [
            (332, "Reconstruct Itinerary"),
            (1584, "Min Cost to Connect All Points"),
            (743, "Network Delay Time"),
            (778, "Swim in Rising Water"),
            (269, "Alien Dictionary"),
            (787, "Cheapest Flights Within K Stops"),
        ],
    },
    {
        "stage": 13,
        "category": "1-D DP",
        "start": date(2026, 10, 23),
        "end": date(2026, 11, 9),
        "problems": [
            (70, "Climbing Stairs"),
            (746, "Min Cost Climbing Stairs"),
            (198, "House Robber"),
            (213, "House Robber II"),
            (5, "Longest Palindromic Substring"),
            (647, "Palindromic Substrings"),
            (91, "Decode Ways"),
            (322, "Coin Change"),
            (152, "Maximum Product Subarray"),
            (139, "Word Break"),
            (300, "Longest Increasing Subsequence"),
            (416, "Partition Equal Subset Sum"),
        ],
    },
    {
        "stage": 14,
        "category": "2-D DP",
        "start": date(2026, 11, 10),
        "end": date(2026, 11, 27),
        "problems": [
            (62, "Unique Paths"),
            (1143, "Longest Common Subsequence"),
            (309, "Best Time to Buy and Sell Stock with Cooldown"),
            (518, "Coin Change II"),
            (494, "Target Sum"),
            (97, "Interleaving String"),
            (329, "Longest Increasing Path in a Matrix"),
            (115, "Distinct Subsequences"),
            (72, "Edit Distance"),
            (312, "Burst Balloons"),
            (10, "Regular Expression Matching"),
        ],
    },
    {
        "stage": 15,
        "category": "Greedy",
        "start": date(2026, 11, 28),
        "end": date(2026, 12, 11),
        "problems": [
            (53, "Maximum Subarray"),
            (55, "Jump Game"),
            (45, "Jump Game II"),
            (134, "Gas Station"),
            (846, "Hand of Straights"),
            (1899, "Merge Triplets to Form Target Triplet"),
            (763, "Partition Labels"),
            (678, "Valid Parenthesis String"),
        ],
    },
    {
        "stage": 16,
        "category": "Intervals",
        "start": date(2026, 12, 12),
        "end": date(2026, 12, 22),
        "problems": [
            (57, "Insert Interval"),
            (56, "Merge Intervals"),
            (435, "Non-overlapping Intervals"),
            (252, "Meeting Rooms"),
            (253, "Meeting Rooms II"),
            (1851, "Minimum Interval to Include Each Query"),
        ],
    },
    {
        "stage": 17,
        "category": "Math & Geometry",
        "start": date(2026, 12, 23),
        "end": date(2027, 1, 5),
        "problems": [
            (48, "Rotate Image"),
            (54, "Spiral Matrix"),
            (73, "Set Matrix Zeroes"),
            (202, "Happy Number"),
            (66, "Plus One"),
            (50, "Pow(x, n)"),
            (43, "Multiply Strings"),
            (2013, "Detect Squares"),
        ],
    },
    {
        "stage": 18,
        "category": "Bit Manipulation",
        "start": date(2027, 1, 6),
        "end": date(2027, 1, 16),
        "problems": [
            (136, "Single Number"),
            (191, "Number of 1 Bits"),
            (338, "Counting Bits"),
            (190, "Reverse Bits"),
            (268, "Missing Number"),
            (371, "Sum of Two Integers"),
            (7, "Reverse Integer"),
        ],
    },
]


def get_solved_numbers(problems_dir: str) -> set[int]:
    """problems/ 디렉토리에서 solution.py가 존재하고 내용이 있는 문제 번호를 반환."""
    solved = set()
    for entry in glob.glob(os.path.join(problems_dir, "LC*")):
        if not os.path.isdir(entry):
            continue
        dirname = os.path.basename(entry)
        # LC0217-contains-duplicate → 217
        try:
            num = int(dirname.split("-")[0].replace("LC", ""))
        except ValueError:
            continue
        sol_path = os.path.join(entry, "solution.py")
        if not os.path.isfile(sol_path):
            continue
        with open(sol_path) as f:
            content = f.read()
        # "TODO: 풀이 작성" 또는 pass만 있으면 아직 안 푼 것
        if "TODO" in content and "pass" in content:
            continue
        solved.add(num)
    return solved


def find_current_stage(today: date) -> dict | None:
    """오늘 날짜가 속하는 Stage를 반환."""
    for s in STAGES:
        if s["start"] <= today <= s["end"]:
            return s
    return None


def find_nearest_stage(today: date) -> dict | None:
    """아직 시작 전이거나 모두 끝난 경우 가장 가까운 Stage를 반환."""
    # 시작 전이면 → 첫 번째 Stage
    if today < STAGES[0]["start"]:
        return STAGES[0]
    # 모두 끝났으면 → 마지막 Stage
    if today > STAGES[-1]["end"]:
        return STAGES[-1]
    # Stage 사이 빈 날짜 → 다음 Stage
    for s in STAGES:
        if today < s["start"]:
            return s
    return None


def main():
    today = date.today()
    problems_dir = os.path.join(os.path.dirname(__file__), "..", "problems")
    problems_dir = os.path.abspath(problems_dir)

    solved = get_solved_numbers(problems_dir)
    total_solved = sum(
        1 for s in STAGES for num, _ in s["problems"] if num in solved
    )

    # ── 헤더 ──
    print()
    print(f"  NeetCode 150 Progress — {today.strftime('%Y-%m-%d')}")
    print(f"  전체: {total_solved}/150 solved")
    print()

    # ── 현재 Stage 찾기 ──
    current = find_current_stage(today)
    if current is None:
        current = find_nearest_stage(today)
        if today < STAGES[0]["start"]:
            days_until = (STAGES[0]["start"] - today).days
            print(f"  아직 시작 전! Stage 1 시작까지 {days_until}일 남음")
            print()
        elif today > STAGES[-1]["end"]:
            print(f"  모든 Stage 완료 기간이 지났습니다!")
            print()

    # ── 현재 Stage 상세 ──
    stage = current
    stage_solved = [num for num, _ in stage["problems"] if num in solved]
    stage_unsolved = [
        (num, title)
        for num, title in stage["problems"]
        if num not in solved
    ]
    stage_total = len(stage["problems"])
    days_left = max(0, (stage["end"] - today).days)

    phase = "Phase 1 (주 3문제)" if stage["stage"] <= 6 else "Phase 2 (주 5문제)"

    print(f"  ┌─────────────────────────────────────────────────")
    print(f"  │ Stage {stage['stage']}. {stage['category']}  ({phase})")
    print(f"  │ 기간: {stage['start']} ~ {stage['end']}  (D-{days_left})")
    print(f"  │ 진행: {len(stage_solved)}/{stage_total} solved")
    print(f"  └─────────────────────────────────────────────────")
    print()

    if stage_unsolved:
        print(f"  남은 문제:")
        for num, title in stage_unsolved:
            print(f"    - LC {num:>4}  {title}")
        print()
        print(f"  빠른 시작: make new {stage_unsolved[0][0]}")
    else:
        print(f"  이 Stage 모든 문제를 풀었습니다!")
        # 다음 Stage 미리보기
        next_idx = stage["stage"]  # stage 번호는 1-based, index는 0-based
        if next_idx < len(STAGES):
            nxt = STAGES[next_idx]
            print(f"  다음: Stage {nxt['stage']}. {nxt['category']} ({nxt['start']} ~)")
    print()

    # ── 이전 Stage 밀린 문제 체크 ──
    overdue = []
    for s in STAGES:
        if s["stage"] >= stage["stage"]:
            break
        for num, title in s["problems"]:
            if num not in solved:
                overdue.append((s["stage"], s["category"], num, title))

    if overdue:
        print(f"  ⚠ 이전 Stage 밀린 문제 ({len(overdue)}개):")
        current_cat = None
        for stg, cat, num, title in overdue:
            if cat != current_cat:
                print(f"    [Stage {stg}. {cat}]")
                current_cat = cat
            print(f"      - LC {num:>4}  {title}")
        print()


if __name__ == "__main__":
    main()
