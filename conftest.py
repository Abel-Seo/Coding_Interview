import sys
import os

def pytest_collect_file(parent, file_path):
    """각 테스트 파일의 디렉토리를 sys.path에 추가"""
    if file_path.name.startswith("test_") and file_path.suffix == ".py":
        dir_path = str(file_path.parent)
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)
