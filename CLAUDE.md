# LeetCode Workspace

NeetCode 150 풀이 환경. Python + pytest.

## 구조

- `problems/LC{번호}-{slug}/problem.md` — 문제 설명
- `problems/LC{번호}-{slug}/solution.py` — 풀이 코드
- `problems/LC{번호}-{slug}/test_solution.py` — 테스트 (AI 생성)

## 규칙

- 테스트는 항상 pytest 사용 (plain assert, no unittest)
- solution.py에서 함수를 from solution import 으로 import (상대 임포트 X)
- 테스트 함수명: test_example_1, test_edge_empty 등
- LeetCode 예시 케이스 + edge case 2~3개 포함
- 타입 힌트 사용
