import sys


def pytest_collect_file(parent, file_path):
    if file_path.name.startswith("test_") and file_path.suffix == ".py":
        test_dir = str(file_path.parent)
        # Clear stale module cache from previous problem directories
        for mod in ["solution", "test_solution"]:
            sys.modules.pop(mod, None)
        # Ensure this test's directory is first in sys.path
        sys.path = [p for p in sys.path if p != test_dir]
        sys.path.insert(0, test_dir)
