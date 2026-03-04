"""
새 문제 스캐폴딩 스크립트

사용법:
    python scripts/new_problem.py <번호> <slug> [유형태그]

예시:
    python scripts/new_problem.py 1 two-sum "array,hash-map"
    python scripts/new_problem.py 217 contains-duplicate "array"
"""

import sys
import os

def main():
    if len(sys.argv) < 3:
        print("사용법: python scripts/new_problem.py <번호> <slug> [태그]")
        print('예시:   python scripts/new_problem.py 1 two-sum "array,hash-map"')
        sys.exit(1)

    num = sys.argv[1].zfill(4)
    slug = sys.argv[2]
    tags = sys.argv[3] if len(sys.argv) > 3 else ""

    dir_name = f"LC{num}-{slug}"
    dir_path = os.path.join("problems", dir_name)

    if os.path.exists(dir_path):
        print(f"⚠️  이미 존재함: {dir_path}")
        sys.exit(1)

    os.makedirs(dir_path)

    # --- problem.md ---
    problem_md = f"""# LC{num} — {slug}

- **LeetCode**: https://leetcode.com/problems/{slug}/
- **난이도**: Easy / Medium / Hard
- **유형**: {tags}

## 문제

> 여기에 LeetCode 문제 설명 복붙

## 예시

```
Input:
Output:
```

## 제약 조건

-
"""

    # --- solution.py ---
    solution_py = f'''"""
LC{num} — {slug}
https://leetcode.com/problems/{slug}/

유형: {tags}
난이도: Easy / Medium / Hard

접근법:
    -

시간복잡도: O()
공간복잡도: O()
"""


def solution():
    # TODO: 풀이 작성
    pass
'''

    with open(os.path.join(dir_path, "problem.md"), "w") as f:
        f.write(problem_md)

    with open(os.path.join(dir_path, "solution.py"), "w") as f:
        f.write(solution_py)

    print(f"✅ 생성 완료: {dir_path}/")
    print(f"   - problem.md    ← 여기에 문제 복붙")
    print(f"   - solution.py   ← 여기에 풀이 작성")
    print()
    print(f"📝 워크플로우:")
    print(f"   1. problem.md에 LeetCode 문제 복붙")
    print(f"   2. solution.py에 풀이 작성")
    print(f'   3. Claude Code에서: /generate-test {dir_path}')
    print(f"   4. python -m pytest {dir_path} -v")


if __name__ == "__main__":
    main()
