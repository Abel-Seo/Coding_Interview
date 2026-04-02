"""
새 문제 스캐폴딩 스크립트 (LeetCode API 자동 연동)

사용법:
    python scripts/new_problem.py <번호>
    python scripts/new_problem.py <번호> [유형태그]   ← 태그 직접 지정 시

예시:
    python scripts/new_problem.py 1
    python scripts/new_problem.py 217 "array"
"""

import sys
import os
import json
import re
import urllib.request
import html


def fetch_slug_from_number(num: int) -> dict | None:
    """LeetCode REST API로 번호 → slug 조회."""
    url = "https://leetcode.com/api/problems/all/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    for q in data.get("stat_status_pairs", []):
        if q["stat"]["frontend_question_id"] == num:
            return {
                "slug": q["stat"]["question__title_slug"],
                "title": q["stat"]["question__title"],
                "difficulty_level": q["difficulty"]["level"],
                "paid_only": q.get("paid_only", False),
            }
    return None


def fetch_problem_detail(slug: str) -> dict | None:
    """LeetCode GraphQL API로 문제 상세 정보 조회."""
    query = json.dumps({
        "query": """query {
            question(titleSlug: "%s") {
                questionFrontendId title titleSlug difficulty
                content topicTags { name }
                exampleTestcaseList
            }
        }""" % slug
    }).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=query,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return data.get("data", {}).get("question")


def html_to_markdown(html_str: str) -> str:
    """LeetCode 문제 HTML → 간단한 마크다운 변환."""
    text = html_str
    # 줄바꿈 정리
    text = text.replace("\r\n", "\n")
    # code 태그
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
    # strong / b
    text = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", text)
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)
    # em / i
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text)
    # example-io spans
    text = re.sub(r'<span class="example-io">(.*?)</span>', r"\1", text)
    # li → bullet
    text = re.sub(r"<li>\s*", "- ", text)
    text = re.sub(r"</li>", "", text)
    # ul / ol 태그 제거
    text = re.sub(r"</?[uo]l[^>]*>", "", text)
    # p / div → 줄바꿈
    text = re.sub(r"<p[^>]*>", "\n", text)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<div[^>]*>", "\n", text)
    text = re.sub(r"</div>", "\n", text)
    # br
    text = re.sub(r"<br\s*/?>", "\n", text)
    # pre 태그 → 코드블록
    text = re.sub(r"<pre>(.*?)</pre>", r"\n```\n\1\n```\n", text, flags=re.DOTALL)
    # img → alt text
    text = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*/?>',r"[\1]", text)
    # sup 태그 (거듭제곱)
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", text)
    # 나머지 HTML 태그 제거
    text = re.sub(r"<[^>]+>", "", text)
    # HTML 엔티티 디코딩
    text = html.unescape(text)
    # &nbsp; 정리
    text = text.replace("\u00a0", " ")
    # 연속 빈줄 정리
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_examples(content_md: str) -> str:
    """마크다운에서 Example 블록 추출."""
    lines = content_md.split("\n")
    examples = []
    in_example = False
    for line in lines:
        if re.match(r"\*\*Example \d+", line):
            in_example = True
            examples.append("")
            continue
        if in_example:
            if line.startswith("**Constraints") or line.startswith("**Note"):
                in_example = False
                continue
            examples.append(line)
    return "\n".join(examples).strip()


def extract_constraints(content_md: str) -> str:
    """마크다운에서 Constraints 블록 추출."""
    lines = content_md.split("\n")
    constraints = []
    in_constraints = False
    for line in lines:
        if "**Constraints" in line:
            in_constraints = True
            continue
        if in_constraints:
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("`"):
                constraints.append(stripped)
            elif stripped == "":
                if constraints:
                    break
            else:
                if constraints:
                    break
    return "\n".join(constraints)


def build_method_name(slug: str) -> str:
    """slug → camelCase 메서드명 (LeetCode 기본 스타일)."""
    parts = slug.split("-")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def main():
    if len(sys.argv) < 2:
        print("사용법: python scripts/new_problem.py <번호> [태그]")
        print("예시:   python scripts/new_problem.py 1")
        print('        python scripts/new_problem.py 217 "array"')
        sys.exit(1)

    try:
        problem_num = int(sys.argv[1])
    except ValueError:
        print(f"❌ 번호가 아닙니다: {sys.argv[1]}")
        sys.exit(1)

    custom_tags = sys.argv[2] if len(sys.argv) > 2 else None

    # ── 1. 번호 → slug 조회 ──
    print(f"🔍 LeetCode #{problem_num} 조회 중...")
    info = fetch_slug_from_number(problem_num)
    if info is None:
        print(f"❌ LeetCode #{problem_num} 문제를 찾을 수 없습니다.")
        sys.exit(1)

    if info["paid_only"]:
        print(f"🔒 #{problem_num} ({info['title']})은 Premium 전용 문제입니다.")
        sys.exit(1)

    slug = info["slug"]
    title = info["title"]
    difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    difficulty = difficulty_map.get(info["difficulty_level"], "Unknown")

    print(f"   → {title} ({difficulty})")

    # ── 2. 문제 상세 조회 ──
    print(f"📄 문제 내용 가져오는 중...")
    detail = fetch_problem_detail(slug)
    if detail is None or detail.get("content") is None:
        print(f"❌ 문제 상세 정보를 가져올 수 없습니다.")
        sys.exit(1)

    tags_list = [t["name"] for t in detail.get("topicTags", [])]
    tags = custom_tags if custom_tags else ", ".join(tags_list)

    content_md = html_to_markdown(detail["content"])
    examples_text = extract_examples(content_md)
    constraints_text = extract_constraints(content_md)

    # ── 3. 디렉토리 생성 ──
    num_str = str(problem_num).zfill(4)
    dir_name = f"LC{num_str}-{slug}"
    dir_path = os.path.join("problems", dir_name)

    if os.path.exists(dir_path):
        print(f"⚠️  이미 존재함: {dir_path}")
        sys.exit(1)

    os.makedirs(dir_path)

    # ── 4. problem.md 생성 ──
    problem_md = f"""# LC{num_str} — {title}

- **LeetCode**: https://leetcode.com/problems/{slug}/
- **난이도**: {difficulty}
- **유형**: {tags}

## 문제

{content_md}

## 제약 조건

{constraints_text if constraints_text else "- (위 문제 설명 참조)"}
"""

    # ── 5. solution.py 생성 ──
    func_name = slug.replace("-", "_")
    method_name = build_method_name(slug)

    solution_py = f'''"""
LC{num_str} — {title}
https://leetcode.com/problems/{slug}/

유형: {tags}
난이도: {difficulty}

접근법:
    -

시간복잡도: O()
공간복잡도: O()
"""


# ── LeetCode 제출용 ─────────────────────────────────────────
class Solution:
    def {method_name}(self):
        # TODO: 풀이 작성
        pass


# ── 로컬 테스트용 래퍼 ────────────────────────────────────────
def {func_name}():
    return Solution().{method_name}()
'''

    # ── 6. 파일 쓰기 ──
    with open(os.path.join(dir_path, "problem.md"), "w") as f:
        f.write(problem_md)

    with open(os.path.join(dir_path, "solution.py"), "w") as f:
        f.write(solution_py)

    print()
    print(f"✅ 생성 완료: {dir_path}/")
    print(f"   - problem.md       ← 문제 설명 (자동 생성됨)")
    print(f"   - solution.py      ← 여기에 풀이 작성")
    print()
    print(f"📝 다음 단계:")
    print(f"   1. solution.py에 풀이 작성")
    print(f'   2. Claude Code에서: /generate-test {dir_path}')
    print(f"   3. python -m pytest {dir_path} -v")


if __name__ == "__main__":
    main()
