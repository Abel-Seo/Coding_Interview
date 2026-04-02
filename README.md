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

### 3. (선택) .zshrc 자동 활성화 설정

터미널 열 때마다 수동으로 activate 하기 귀찮으면, `~/.zshrc` 끝에 아래를 추가한다:

```bash
# Auto activate venv
auto_activate_venv() {
  if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
  fi
}
# cd 할 때마다 자동 체크
chpwd_functions=(${chpwd_functions[@]} auto_activate_venv)
# 터미널 열 때도 현재 디렉토리 체크
auto_activate_venv
```

이렇게 하면:
- `.venv/` 폴더가 있는 디렉토리에 `cd` 하면 자동으로 가상환경 활성화
- 해당 디렉토리에서 터미널을 열어도 자동 활성화
- `.venv/`가 없는 디렉토리로 이동하면 아무 일도 안 함

## 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `make status` | 오늘 기준 Stage, 남은 문제 확인 |
| `make new 217` | LeetCode 번호로 문제 자동 생성 |
| `make test n=217` | 특정 문제 테스트 실행 |
| `make test` | 전체 테스트 실행 |
| `/generate-test problems/LC0217-...` | Claude Code 테스트 자동 생성 |

## 매일 워크플로우

### 1. 오늘 할 문제 확인

```bash
make status
```

오늘 날짜 기준으로 현재 Stage, 남은 기간(D-day), 안 푼 문제 목록을 보여준다.
이전 Stage에 밀린 문제가 있으면 경고도 표시된다.

### 2. 새 문제 스캐폴딩

```bash
make new 217
```

LeetCode 번호만 입력하면 API에서 문제 정보를 자동으로 가져와서 파일을 생성한다.

- `problems/LC0217-contains-duplicate/problem.md` ← 문제 설명 (자동 생성)
- `problems/LC0217-contains-duplicate/solution.py` ← 풀이 작성

태그를 직접 지정하고 싶으면: `make new 217 "array"`

### 3. 풀이 작성

`solution.py`를 열고 풀이 코드를 작성한다.
IDE에서 `problem.md`와 `solution.py`를 스플릿 뷰로 열면 왼쪽 문제 / 오른쪽 코드로 쓸 수 있다.

### 4. 테스트 자동 생성 (Claude Code)

```
/generate-test problems/LC0217-contains-duplicate
```

`problem.md`와 `solution.py`를 읽고 `test_solution.py`를 자동 생성한다.

### 5. 테스트 실행

```bash
# 특정 문제만
make test n=217

# 전체
make test
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
├── Makefile                     ← make 명령어 (new, test, status)
├── scripts/
│   ├── new_problem.py           ← 문제 스캐폴딩 (LeetCode API 자동 연동)
│   └── status.py                ← 진행 상황 확인
├── pytest.ini
└── requirements.txt
```

## Obsidian 연동

`templates/` 폴더의 파일을 Obsidian vault의 Templater 템플릿 폴더에 복사한다.

- **Daily Coding Log** → 매일 풀이 결과 한 줄 기록 (30초)
- **Problem Note** → 🟡🔴 문제만 상세 기록 (3분)

## 학습 가이드

[STUDY_GUIDE.md](./STUDY_GUIDE.md) 참조
