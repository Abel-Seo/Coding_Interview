# ── LeetCode Workspace ──────────────────────────────────────
# make new 217          → 문제 스캐폴딩 (problem.md + solution.py + test_solution.py)
# make new 217 "array"  → 태그 직접 지정
# make test n=217       → 특정 문제 테스트
# make test             → 전체 테스트
# make status           → 오늘 진행 상황 확인

status:
	@python scripts/status.py

new:
	@python scripts/new_problem.py $(filter-out $@,$(MAKECMDGOALS))

test:
ifdef n
	@python -m pytest problems/LC$(shell printf '%04d' $(n))-* -v
else
	@python -m pytest -v
endif

# make new 217 에서 217을 타겟으로 인식하지 않게 처리
%:
	@:
