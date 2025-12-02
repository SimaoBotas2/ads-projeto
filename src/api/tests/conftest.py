"""Root conftest.py to configure Python path for tests"""
import sys
from pathlib import Path

# Add the src/api directory to Python path so imports work correctly
src_api_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_api_path))
