<<<<<<< HEAD
# Coding_Interview
=======
# LeetCode Workspace

NeetCode 150 로컬 풀이 환경 (Python + pytest + Claude Code)

## 세팅

### 1. Python 설치

```bash
# Mac
brew install python

# Windows
# https://www.python.org/downloads/ 에서 다운로드
# 설치 시 "Add Python to PATH" 반드시 체크
```

### 2. 환경 세팅

```bash
cd leetcode-workspace
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> 터미널 열 때마다 `source .venv/bin/activate` 한 번 실행해야 한다.
> 프롬프트에 `(.venv)` 붙어있으면 활성화된 상태.

## 매일 워크플로우

### 1. 새 문제 스캐폴딩

```bash
python scripts/new_problem.py 1 two-sum "array,hash-map"
```

생성되는 파일:
- `problems/LC0001-two-sum/problem.md` ← 문제 복붙
- `problems/LC0001-two-sum/solution.py` ← 풀이 작성

### 2. 문제 복붙

`problem.md`를 열고 LeetCode에서 문제 설명을 복붙한다.

### 3. 풀이 작성

`solution.py`를 열고 풀이 코드를 작성한다.
IDE에서 `problem.md`와 `solution.py`를 스플릿 뷰로 열면 왼쪽 문제 / 오른쪽 코드로 쓸 수 있다.

### 4. 테스트 자동 생성 (Claude Code)

```
/generate-test problems/LC0001-two-sum
```

`problem.md`와 `solution.py`를 읽고 `test_solution.py`를 자동 생성한다.

### 5. 테스트 실행

```bash
# 특정 문제만
python -m pytest problems/LC0001-two-sum -v

# 전체
python -m pytest -v
```

## 폴더 구조

```
leetcode-workspace/
├── .claude/
│   └── commands/
│       └── generate-test.md    ← Claude Code 슬래시 커맨드
├── CLAUDE.md                    ← Claude Code 프로젝트 컨텍스트
├── STUDY_GUIDE.md               ← 학습 가이드 (Phase 1~3)
├── problems/
│   └── LC0217-contains-duplicate/  ← 예시 문제
│       ├── problem.md           ← 문제 설명 (LeetCode 복붙)
│       ├── solution.py          ← 풀이 코드
│       └── test_solution.py     ← 테스트 (Claude Code 생성)
├── templates/                   ← Obsidian 템플릿
│   ├── Daily Coding Log.md
│   └── Problem Note.md
├── scripts/
│   └── new_problem.py           ← 문제 스캐폴딩
├── pytest.ini
└── requirements.txt
```

## Obsidian 연동

`templates/` 폴더의 파일을 Obsidian vault의 Templater 템플릿 폴더에 복사한다.

- **Daily Coding Log** → 매일 풀이 결과 한 줄 기록 (30초)
- **Problem Note** → 🟡🔴 문제만 상세 기록 (3분)

## 학습 가이드

[STUDY_GUIDE.md](./STUDY_GUIDE.md) 참조
>>>>>>> f47cc10 (Initial Setting)
