"""
새 문제 스캐폴딩 스크립트 (LeetCode API 자동 연동)

사용법:
    python scripts/new_problem.py <번호>
    python scripts/new_problem.py <번호> [유형태그]   ← 태그 직접 지정 시

예시:
    python scripts/new_problem.py 1
    python scripts/new_problem.py 217 "array"

생성 파일:
    - problem.md       ← 문제 설명
    - solution.py      ← 풀이 템플릿 (정확한 메서드 시그니처)
    - test_solution.py ← 테스트 (예제 케이스 자동 생성)
"""

import sys
import os
import json
import re
import urllib.request
import html
import textwrap


# ── LeetCode API ───────────────────────────────────────────────


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
    """LeetCode GraphQL API로 문제 상세 정보 조회 (코드 스니펫 포함)."""
    query = json.dumps({
        "query": """query {
            question(titleSlug: "%s") {
                questionFrontendId title titleSlug difficulty
                content topicTags { name }
                exampleTestcaseList
                codeSnippets { lang langSlug code }
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


# ── HTML → Markdown 변환 ──────────────────────────────────────


def html_to_markdown(html_str: str) -> str:
    """LeetCode 문제 HTML → 간단한 마크다운 변환."""
    text = html_str
    text = text.replace("\r\n", "\n")
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
    text = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", text)
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text)
    text = re.sub(r'<span class="example-io">(.*?)</span>', r"\1", text)
    text = re.sub(r"<li>\s*", "- ", text)
    text = re.sub(r"</li>", "", text)
    text = re.sub(r"</?[uo]l[^>]*>", "", text)
    text = re.sub(r"<p[^>]*>", "\n", text)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<div[^>]*>", "\n", text)
    text = re.sub(r"</div>", "\n", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<pre>(.*?)</pre>", r"\n```\n\1\n```\n", text, flags=re.DOTALL)
    text = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*/?>',r"[\1]", text)
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


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


# ── Python 코드 스니펫 파싱 ───────────────────────────────────


def parse_python_snippet(snippets: list[dict]) -> dict | None:
    """LeetCode Python3 코드 스니펫에서 메서드 정보 추출.

    Returns:
        {
            "method_name": "twoSum",
            "params": "self, nums: List[int], target: int",
            "param_names": ["nums", "target"],
            "return_type": "List[int]",
            "raw_code": "class Solution:\n    def ...",
        }
    """
    snippet = None
    for s in (snippets or []):
        if s["langSlug"] == "python3":
            snippet = s
            break
    if snippet is None:
        return None

    code = snippet["code"]
    # def methodName(self, param1: Type1, ...) -> ReturnType:
    m = re.search(
        r"def\s+(\w+)\s*\((self(?:,\s*.+?)?)\)\s*(?:->\s*(.+?))?\s*:",
        code,
    )
    if m is None:
        return None

    method_name = m.group(1)
    full_params = m.group(2).strip()
    return_type = (m.group(3) or "").strip()

    # self 제거하고 파라미터 이름만 추출
    param_names = []
    params_no_self = re.sub(r"^self\s*,?\s*", "", full_params).strip()
    if params_no_self:
        for p in params_no_self.split(","):
            p = p.strip()
            name = p.split(":")[0].strip().split("=")[0].strip()
            if name:
                param_names.append(name)

    return {
        "method_name": method_name,
        "params": full_params,
        "param_names": param_names,
        "return_type": return_type,
        "raw_code": code,
    }


# ── 테스트케이스 파싱 ─────────────────────────────────────────


def parse_example_testcases(
    testcase_list: list[str],
    content_md: str,
    param_names: list[str],
) -> list[dict]:
    """LeetCode 예제 테스트케이스 → 구조화된 테스트 목록 변환.

    Returns: [{"inputs": {"nums": "[1,2,3]", "target": "9"}, "expected": "..."}]
    """
    tests = []

    # exampleTestcaseList: 각 항목이 "\n"으로 파라미터 구분된 하나의 예제
    # 예: "[2,7,11,15]\n9" → nums=[2,7,11,15], target=9
    for tc in testcase_list:
        param_values = tc.strip().split("\n")
        inputs = {}
        for j, val in enumerate(param_values):
            key = param_names[j] if j < len(param_names) else f"arg{j}"
            inputs[key] = val.strip()
        tests.append({"inputs": inputs, "expected": None})

    # problem.md에서 Output 값 추출
    output_pattern = re.compile(r"\*\*Output:\*\*\s*(.+)")
    outputs = output_pattern.findall(content_md)
    for i, test in enumerate(tests):
        if i < len(outputs):
            test["expected"] = outputs[i].strip()

    return tests


def python_literal(raw_val: str) -> str:
    """LeetCode 원시 값 → Python 리터럴 문자열 변환.

    "true" → "True", "false" → "False", "null" → "None" 등
    """
    mapping = {"true": "True", "false": "False", "null": "None"}
    return mapping.get(raw_val.strip(), raw_val.strip())


def _format_assert(call: str, expected: str) -> str:
    """assert 문 생성. bool 값은 == True/False 대신 assert/assert not 사용."""
    if expected == "True":
        return f"assert {call}"
    elif expected == "False":
        return f"assert not {call}"
    else:
        return f"assert {call} == {expected}"


def _infer_edge_cases(
    param_names: list[str],
    method_params: str,
    constraints_text: str,
) -> list[dict]:
    """Constraints와 파라미터 타입을 기반으로 edge case 추론.

    Returns: [{"name": "test_edge_empty", "args": {"nums": "[]"}, "comment": "빈 배열"}]
    """
    edges = []

    # 파라미터별 타입 추출 (self 제외)
    param_types = {}
    params_no_self = re.sub(r"^self\s*,?\s*", "", method_params).strip()
    if params_no_self:
        for p in params_no_self.split(","):
            p = p.strip()
            parts = p.split(":")
            name = parts[0].strip()
            ptype = parts[1].strip() if len(parts) > 1 else ""
            param_types[name] = ptype

    # 제약 조건에서 최소 길이가 1인지 0인지 확인
    allows_empty = True
    for line in constraints_text.split("\n"):
        # "1 <= nums.length", "1 <= n", "s.length >= 1" 등
        if re.search(r"1\s*<=\s*\w+\.?(?:length|size|len)", line, re.IGNORECASE):
            allows_empty = False
        if re.search(r"\w+\.?(?:length|size|len)\s*>=\s*1", line, re.IGNORECASE):
            allows_empty = False

    # 타입별 기본값 (edge case에서 미지정 파라미터 채울 때 사용)
    type_defaults = {}
    for name in param_names:
        ptype = param_types.get(name, "")
        if "List" in ptype:
            type_defaults[name] = "[1, 2]"
        elif ptype == "str":
            type_defaults[name] = '"test"'
        elif ptype == "int":
            type_defaults[name] = "1"
        else:
            type_defaults[name] = "None"

    def _make_args(overrides: dict) -> dict:
        """모든 파라미터에 값을 채운 dict 반환."""
        result = {}
        for n in param_names:
            result[n] = overrides.get(n, type_defaults.get(n, "None"))
        return result

    matched = False
    for name in param_names:
        ptype = param_types.get(name, "")

        # List 타입 edge case
        if "List" in ptype:
            if allows_empty:
                edges.append({
                    "name": "test_edge_empty_list",
                    "args": _make_args({name: "[]"}),
                    "comment": "빈 리스트",
                })
            edges.append({
                "name": "test_edge_single_element",
                "args": _make_args({name: "[1]"}),
                "comment": "원소 1개",
            })
            matched = True
            break

        # 문자열 타입 edge case
        if ptype == "str":
            # 같은 타입 파라미터는 모두 같은 edge 값으로 채우기
            str_params = [n for n in param_names if param_types.get(n, "") == "str"]
            if allows_empty:
                edges.append({
                    "name": "test_edge_empty_string",
                    "args": _make_args({n: '""' for n in str_params}),
                    "comment": "빈 문자열",
                })
            edges.append({
                "name": "test_edge_single_char",
                "args": _make_args({n: '"a"' for n in str_params}),
                "comment": "한 글자",
            })
            matched = True
            break

        # int 타입 edge case
        if ptype == "int":
            edges.append({
                "name": "test_edge_zero",
                "args": _make_args({name: "0"}),
                "comment": "0 입력",
            })
            matched = True
            break

    # edge case가 없으면 기본 뼈대 1개
    if not matched:
        edges.append({
            "name": "test_edge_case_1",
            "args": {},
            "comment": "TODO: edge case 작성",
        })

    return edges


def generate_test_file(
    num_str: str,
    title: str,
    slug: str,
    method_info: dict,
    example_tests: list[dict],
    constraints_text: str = "",
) -> str:
    """test_solution.py 내용 생성."""
    func_name = slug.replace("-", "_")
    param_names = method_info["param_names"]
    method_params = method_info.get("params", "self")

    lines = []
    lines.append(f'"""Tests for LC{num_str} — {title}"""')

    use_parametrize = len(example_tests) >= 2 and all(
        t["expected"] is not None for t in example_tests
    )

    if use_parametrize:
        lines.append("import pytest")
    lines.append(f"from solution import {func_name}")
    lines.append("")
    lines.append("")

    # ── 예제 케이스 ──
    if use_parametrize:
        # parametrize로 묶기
        all_keys = list(param_names) + ["expected"]
        lines.append(f'@pytest.mark.parametrize("{", ".join(all_keys)}", [')

        for test in example_tests:
            args = []
            for name in param_names:
                raw = test["inputs"].get(name, "")
                args.append(python_literal(raw))
            expected = python_literal(test["expected"])
            tuple_str = f"    ({', '.join(args)}, {expected}),"
            lines.append(tuple_str)

        lines.append("])")
        call_args = ", ".join(param_names)
        call = f"{func_name}({call_args})"
        lines.append(f"def test_examples({', '.join(all_keys)}):")
        lines.append(f"    {_format_assert(call, 'expected')}")
        lines.append("")
        lines.append("")
    else:
        # 1개이거나 expected가 없는 경우 개별 함수로
        for i, test in enumerate(example_tests, 1):
            lines.append(f"def test_example_{i}():")

            args = []
            for name in param_names:
                raw = test["inputs"].get(name, "")
                args.append(python_literal(raw))

            call = f"{func_name}({', '.join(args)})"

            if test["expected"] is not None:
                expected = python_literal(test["expected"])
                lines.append(f"    {_format_assert(call, expected)}")
            else:
                lines.append(f"    result = {call}")
                lines.append(f"    assert result is not None  # TODO: expected 값 채우기")

            lines.append("")
            lines.append("")

    # ── Edge Cases (자동 추론) ──
    lines.append("# ── Edge Cases ─────────────────────────────────────────────")
    lines.append("")
    lines.append("")

    edge_cases = _infer_edge_cases(param_names, method_params, constraints_text)
    for edge in edge_cases:
        lines.append(f"def {edge['name']}():")
        lines.append(f"    # {edge['comment']}")
        if edge["args"]:
            # 제공된 인자 + 나머지는 placeholder
            args = []
            for name in param_names:
                if name in edge["args"]:
                    args.append(edge["args"][name])
                else:
                    args.append("None  # TODO")
            call = f"{func_name}({', '.join(args)})"
            lines.append(f"    result = {call}")
            lines.append(f"    assert result is not None  # TODO: expected 값 채우기")
        else:
            lines.append("    pass")
        lines.append("")
        lines.append("")

    return "\n".join(lines)


# ── solution.py 생성 ──────────────────────────────────────────


def generate_solution_file(
    num_str: str,
    title: str,
    slug: str,
    tags: str,
    difficulty: str,
    method_info: dict | None,
) -> str:
    """solution.py 내용 생성."""
    func_name = slug.replace("-", "_")

    if method_info:
        method_name = method_info["method_name"]
        method_params = method_info["params"]
        return_type = method_info["return_type"]
        param_names = method_info["param_names"]

        return_annotation = f" -> {return_type}" if return_type else ""
        wrapper_args = ", ".join(param_names)
        call_args = ", ".join(param_names)

        # raw_code에서 import 문 추출 (List, Optional 등)
        raw = method_info.get("raw_code", "")
        imports = []
        # typing 임포트가 필요한 타입들 감지
        typing_types = re.findall(r'\b(List|Optional|Dict|Set|Tuple)\b', raw + method_params + (return_type or ""))
        if typing_types:
            unique_types = sorted(set(typing_types))
            imports.append(f"from typing import {', '.join(unique_types)}")

        import_block = "\n".join(imports) + "\n\n" if imports else ""
    else:
        method_name = slug.replace("-", "_")
        method_params = "self"
        return_annotation = ""
        wrapper_args = ""
        call_args = ""
        import_block = ""

    return f'''{import_block}"""
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
    def {method_name}({method_params}){return_annotation}:
        # TODO: 풀이 작성
        pass


# ── 로컬 테스트용 래퍼 ────────────────────────────────────────
def {func_name}({wrapper_args}):
    return Solution().{method_name}({call_args})
'''


# ── 메인 ──────────────────────────────────────────────────────


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
    constraints_text = extract_constraints(content_md)

    # ── 3. 코드 스니펫 파싱 ──
    method_info = parse_python_snippet(detail.get("codeSnippets", []))
    if method_info:
        print(f"   → 메서드: {method_info['method_name']}({', '.join(method_info['param_names'])})")

    # ── 4. 예제 테스트케이스 파싱 ──
    example_testcases = detail.get("exampleTestcaseList", [])
    param_names = method_info["param_names"] if method_info else []
    example_tests = parse_example_testcases(example_testcases, content_md, param_names)

    # ── 5. 디렉토리 생성 ──
    num_str = str(problem_num).zfill(4)
    dir_name = f"LC{num_str}-{slug}"
    dir_path = os.path.join("problems", dir_name)

    if os.path.exists(dir_path):
        print(f"⚠️  이미 존재함: {dir_path}")
        sys.exit(1)

    os.makedirs(dir_path)

    # ── 6. problem.md ──
    problem_md = f"""# LC{num_str} — {title}

- **LeetCode**: https://leetcode.com/problems/{slug}/
- **난이도**: {difficulty}
- **유형**: {tags}

## 문제

{content_md}

## 제약 조건

{constraints_text if constraints_text else "- (위 문제 설명 참조)"}
"""

    # ── 7. solution.py ──
    solution_py = generate_solution_file(
        num_str, title, slug, tags, difficulty, method_info,
    )

    # ── 8. test_solution.py ──
    test_py = generate_test_file(
        num_str, title, slug, method_info or {
            "method_name": slug.replace("-", "_"),
            "param_names": [],
        },
        example_tests,
        constraints_text=constraints_text,
    )

    # ── 9. 파일 쓰기 ──
    with open(os.path.join(dir_path, "problem.md"), "w") as f:
        f.write(problem_md)

    with open(os.path.join(dir_path, "solution.py"), "w") as f:
        f.write(solution_py)

    with open(os.path.join(dir_path, "test_solution.py"), "w") as f:
        f.write(test_py)

    print()
    print(f"✅ 생성 완료: {dir_path}/")
    print(f"   📝 problem.md       ← 문제 설명")
    print(f"   💻 solution.py      ← 풀이 템플릿 ({method_info['method_name'] if method_info else 'TODO'})")
    print(f"   🧪 test_solution.py ← 테스트 ({len(example_tests)}개 예제 + edge case 뼈대)")
    print()
    print(f"📌 다음 단계:")
    print(f"   1. solution.py에 풀이 작성")
    print(f"   2. make test n={problem_num}")


if __name__ == "__main__":
    main()
