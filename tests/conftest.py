import sys
from pathlib import Path


def pytest_configure():
    """Ensure project root is on sys.path so tests can import `src` package."""
    root = Path(__file__).resolve().parents[1]
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
