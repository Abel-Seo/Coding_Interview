# Python Coding Test Cheatsheet (for JS developers)

## 1. 배열 / 리스트

```python
# ── 생성 ──
nums = [1, 2, 3]
zeros = [0] * 5                    # [0, 0, 0, 0, 0]
grid = [[0] * 3 for _ in range(4)] # 4x3 2D 배열 (⚠ [[0]*3]*4 는 참조 복사 버그)
```
```javascript
// JS 대응
const nums = [1, 2, 3];
const zeros = new Array(5).fill(0);
const grid = Array.from({length: 4}, () => new Array(3).fill(0));
```

```python
# ── 슬라이싱 (JS에 없는 핵심 문법) ──
nums[1:3]      # [2, 3]        인덱스 1~2
nums[::-1]     # [3, 2, 1]     역순 복사
nums[::2]      # [1, 3]        짝수 인덱스만
nums[-1]       # 3             마지막 원소 (JS: nums.at(-1))
nums[-2:]      # [2, 3]        뒤에서 2개
```

```python
# ── 자주 쓰는 메서드 ──
nums.append(4)          # push          → [1,2,3,4]
nums.pop()              # pop           → 4 반환, [1,2,3]
nums.pop(0)             # shift         → 1 반환 (O(n) 주의!)
nums.insert(0, 0)       # unshift       → [0,2,3] (O(n) 주의!)
nums.sort()             # 제자리 정렬 (원본 변경!)
sorted(nums)            # 새 리스트 반환 (원본 유지)
nums.sort(key=lambda x: -x)  # 내림차순
nums.reverse()          # 제자리 역순
len(nums)               # nums.length
```

```python
# ── List Comprehension (JS: map/filter 대체) ──
squares = [x**2 for x in range(5)]           # [0,1,4,9,16]   JS: [...Array(5)].map((_,i) => i**2)
evens = [x for x in nums if x % 2 == 0]     # filter          JS: nums.filter(x => x%2===0)
flat = [x for row in grid for x in row]      # flat            JS: grid.flat()
```

---

## 2. 문자열

```python
s = "hello"
s[1:3]            # "el"
s[::-1]           # "olleh"           JS: s.split('').reverse().join('')
s.upper()         # "HELLO"
s.lower()         # "hello"
s.isalpha()       # True              JS: /^[a-zA-Z]+$/.test(s)
s.isdigit()       # False             JS: /^\d+$/.test(s)
s.isalnum()       # True              JS: /^[a-zA-Z0-9]+$/.test(s)
"lo" in s         # True              JS: s.includes("lo")
s.startswith("he")# True              JS: s.startsWith("he")
s.split(",")      # split             JS: s.split(",")
",".join(["a","b"])# "a,b"            JS: ["a","b"].join(",")
s.replace("l","r")# "herro"          (첫 번째만 아니라 전부 교체!)
s.strip()         # trim              JS: s.trim()
ord("a")          # 97                JS: "a".charCodeAt(0)
chr(97)           # "a"               JS: String.fromCharCode(97)
```

```python
# ⚠ Python 문자열은 불변! 수정하려면 리스트로 변환
chars = list(s)       # ['h','e','l','l','o']
chars[0] = 'H'
s = "".join(chars)    # "Hello"
```

---

## 3. HashMap / HashSet

```python
# ── dict (= JS Object / Map) ──
d = {}
d["key"] = 1                       # JS: d["key"] = 1  또는  d.set("key", 1)
d.get("key", 0)                    # 없으면 기본값 0 반환 (JS: d.get("key") ?? 0)
"key" in d                         # JS: "key" in d  또는  d.has("key")
del d["key"]                       # JS: delete d["key"]  또는  d.delete("key")
d.keys()                           # JS: Object.keys(d)
d.values()                         # JS: Object.values(d)
d.items()                          # JS: Object.entries(d)

for k, v in d.items():             # JS: for (const [k, v] of Object.entries(d))
    print(k, v)
```

```python
# ── defaultdict (키 없을 때 자동 초기화) ──
from collections import defaultdict
graph = defaultdict(list)          # graph["a"] 접근만 해도 [] 자동 생성
count = defaultdict(int)           # count["x"] += 1  → KeyError 없이 동작
```

```python
# ── Counter (빈도수 세기) ──
from collections import Counter
cnt = Counter("aabbc")            # {'a':2, 'b':2, 'c':1}   JS: 직접 루프 돌려야 함
cnt.most_common(2)                # [('a',2), ('b',2)]      상위 N개
cnt["a"]                          # 2
cnt["z"]                          # 0 (KeyError 안 남!)
```

```python
# ── set (= JS Set) ──
s = set()
s.add(1)                          # JS: s.add(1)
s.remove(1)                       # 없으면 KeyError (JS: s.delete(1))
s.discard(1)                      # 없어도 에러 안 남
1 in s                            # JS: s.has(1)
a & b                             # 교집합    JS: 직접 구현
a | b                             # 합집합
a - b                             # 차집합
```

---

## 4. 스택 / 큐 / 덱

```python
# ── 스택 (list로 충분) ──
stack = []
stack.append(1)       # push
stack.pop()           # pop
stack[-1]             # peek (top)

# ── 큐 (deque 필수! list.pop(0)은 O(n)) ──
from collections import deque
q = deque()
q.append(1)           # enqueue (오른쪽)    JS: queue.push(1)
q.popleft()           # dequeue (왼쪽)      JS: queue.shift()
q.appendleft(0)       # 왼쪽 추가
q[0]                  # front peek
```

---

## 5. 힙 (Priority Queue)

```python
import heapq

# ⚠ Python heapq는 최소힙만 지원! 최대힙은 -1 곱해서 사용
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)              # 제자리 힙 변환 O(n)
heapq.heappush(nums, 2)          # 삽입 O(log n)
smallest = heapq.heappop(nums)   # 최솟값 꺼내기 O(log n)
nums[0]                          # peek (최솟값 확인만)

# 최대힙 트릭
max_heap = []
heapq.heappush(max_heap, -val)   # 넣을 때 부호 반전
largest = -heapq.heappop(max_heap) # 꺼낼 때 다시 반전

# 상위 k개
heapq.nlargest(3, nums)          # 큰 순 3개
heapq.nsmallest(3, nums)         # 작은 순 3개
```
```javascript
// JS에는 내장 힙이 없음 → 직접 구현하거나 라이브러리 사용
```

---

## 6. 정렬

```python
# ── 기본 ──
sorted([3,1,2])                       # [1,2,3] 새 리스트
sorted([3,1,2], reverse=True)         # [3,2,1]

# ── 커스텀 키 ──
words = ["banana", "pie", "apple"]
sorted(words, key=len)                # ['pie', 'apple', 'banana']
sorted(words, key=lambda w: w[-1])    # 마지막 글자 기준

# ── 다중 기준 (JS보다 훨씬 깔끔) ──
# 점수 내림차순 → 이름 오름차순
students = [("Alice", 90), ("Bob", 90), ("Charlie", 80)]
sorted(students, key=lambda x: (-x[1], x[0]))
# [('Alice', 90), ('Bob', 90), ('Charlie', 80)]
```
```javascript
// JS 대응 (다중 기준)
students.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
```

---

## 7. 이진 탐색

```python
from bisect import bisect_left, bisect_right, insort

nums = [1, 3, 3, 5, 7]
bisect_left(nums, 3)      # 2  → 3이 들어갈 가장 왼쪽 인덱스
bisect_right(nums, 3)     # 4  → 3이 들어갈 가장 오른쪽 인덱스
insort(nums, 4)           # [1, 3, 3, 4, 5, 7]  정렬 유지하며 삽입
```

```python
# ── 직접 구현 (면접용) ──
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

---

## 8. 그래프 순회

```python
# ── BFS ──
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# ── DFS (재귀) ──
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# ── DFS (스택, 재귀 깊이 제한 우회) ──
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            stack.append(neighbor)
```

```python
# ⚠ Python 재귀 제한 (기본 1000)
import sys
sys.setrecursionlimit(10000)    # 필요시 늘리기
```

---

## 9. 유용한 내장 함수

```python
# ── 수학 ──
abs(-5)                    # 5
max(1, 2, 3)               # 3
min(nums)                  # 리스트 최솟값
sum(nums)                  # 합계
float('inf')               # Infinity          JS: Infinity
float('-inf')              # -Infinity         JS: -Infinity
divmod(10, 3)              # (3, 1)  → 몫과 나머지 동시에
10 // 3                    # 3  정수 나눗셈     JS: Math.floor(10/3)
10 % 3                     # 1  나머지
2 ** 10                    # 1024  거듭제곱     JS: 2**10 또는 Math.pow(2,10)

# ⚠ Python 음수 나머지는 JS와 다름!
-7 % 3                    # 2   (Python: 항상 양수)
                           # JS: -7 % 3 === -1
```

```python
# ── 반복 도구 ──
enumerate(nums)             # [(0,'a'), (1,'b'), ...]   JS: nums.map((v,i) => [i,v])
zip([1,2], [3,4])           # [(1,3), (2,4)]            JS: 없음, 직접 구현
zip(*matrix)                # 행렬 전치!                  [[1,2],[3,4]] → [(1,3),(2,4)]
range(5)                    # 0,1,2,3,4                  JS: [...Array(5).keys()]
range(2, 10, 3)             # 2,5,8                      시작, 끝, 스텝

any(x > 3 for x in nums)   # 하나라도 만족?              JS: nums.some(x => x>3)
all(x > 0 for x in nums)   # 모두 만족?                  JS: nums.every(x => x>0)
```

```python
# ── itertools (코테 단골) ──
from itertools import combinations, permutations, product, accumulate

list(combinations([1,2,3], 2))   # [(1,2),(1,3),(2,3)]     조합 nC2
list(permutations([1,2,3], 2))   # [(1,2),(1,3),(2,1),...] 순열 nP2
list(product("ab", repeat=2))    # [('a','a'),('a','b'),('b','a'),('b','b')]  중복순열
list(accumulate([1,2,3,4]))      # [1,3,6,10]             누적합 (prefix sum)
```

---

## 10. 트리 노드

```python
# ── LeetCode 표준 TreeNode ──
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ── 순회 ──
def inorder(node):          # 중위: 왼 → 루트 → 오른 (BST → 정렬된 순서)
    if not node: return []
    return inorder(node.left) + [node.val] + inorder(node.right)

def preorder(node):         # 전위: 루트 → 왼 → 오른
    if not node: return []
    return [node.val] + preorder(node.left) + preorder(node.right)

def level_order(root):      # 레벨 순회 (BFS)
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

---

## 11. 연결 리스트

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# ── 더미 헤드 패턴 (삽입/삭제 시 edge case 제거) ──
dummy = ListNode(0)
dummy.next = head
# ... 작업 후
return dummy.next

# ── 투 포인터 (fast & slow) ──
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow → 중간 노드
```

---

## 12. Python 특이 문법 (JS와 차이점)

```python
# ── 다중 할당 / 스왑 ──
a, b = 1, 2                 # JS: let [a,b] = [1,2]  (구조 분해)
a, b = b, a                 # 스왑 (임시 변수 불필요!)

# ── 비교 체이닝 ──
if 0 <= x < n:              # JS: if (0 <= x && x < n)
    pass

# ── Truthy / Falsy ──
# Python Falsy: None, 0, 0.0, "", [], {}, set(), False
# JS Falsy:     null, undefined, 0, NaN, "", false
# ⚠ JS에서 [] 와 {}는 truthy, Python에서는 falsy!

if not nums:                # 빈 리스트 체크    JS: if (!nums.length)
    pass

# ── 삼항 연산자 ──
x = "yes" if condition else "no"    # JS: x = condition ? "yes" : "no"

# ── Walrus 연산자 (:=) — 할당과 동시에 사용 ──
if (n := len(nums)) > 10:
    print(f"길이가 {n}")

# ── 언패킹 ──
first, *rest = [1, 2, 3, 4]       # first=1, rest=[2,3,4]
*init, last = [1, 2, 3, 4]        # init=[1,2,3], last=4

# ── for-else (break 없이 끝나면 else 실행) ──
for x in nums:
    if x == target:
        break
else:
    print("target을 찾지 못함")     # JS에는 없는 문법
```

---

## 13. 시간복잡도 빠른 참조

| 연산 | Python | 복잡도 |
|------|--------|--------|
| `list.append()` | `arr.push()` | O(1) |
| `list.pop()` | `arr.pop()` | O(1) |
| `list.pop(0)` | `arr.shift()` | **O(n)** → deque 사용 |
| `list[i]` | `arr[i]` | O(1) |
| `x in list` | `arr.includes(x)` | **O(n)** |
| `x in set` | `set.has(x)` | O(1) |
| `x in dict` | `key in obj` | O(1) |
| `dict[key]` | `obj[key]` | O(1) |
| `sorted()` | `arr.sort()` | O(n log n) |
| `heappush/pop` | — | O(log n) |
| `deque.popleft()` | `arr.shift()` | O(1) vs **O(n)** |
