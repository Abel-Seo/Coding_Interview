개인 맥북 세팅 순서
1. Python 설치 (한 번만)
bashbrew install python@3.14
brew 자체가 없으면 먼저:
bash/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. 레포 클론
bashcd ~/Documents/Study/DS_AL  # 원하는 경로로
git clone https://github.com/오빠아이디/leetcode-workspace.git
cd leetcode-workspace
3. 가상환경 만들고 패키지 설치 (한 번만)
bashpython3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
4. 확인
bashpython3 -m pytest problems/LC0217-contains-duplicate -v
초록색 PASSED 6개 뜨면 끝!
5. 이후 매일 루틴
bashcd leetcode-workspace
source .venv/bin/activate    # 터미널 열 때마다 한 번
# 문제 풀기 시작
핵심은 .venv/ 폴더는 GitHub에 안 올라가니까 (.gitignore에 포함), 새 컴퓨터에서는 3번 과정을 한 번 해줘야 한다는 거야. Node로 치면 git clone 후에 npm install 해주는 거랑 똑같아.
