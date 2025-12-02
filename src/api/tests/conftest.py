"""Root conftest.py to configure Python path and environment for tests"""
import os
import sys
from pathlib import Path

# Set DOCS_MODE to avoid database initialization during test collection
os.environ["DOCS_MODE"] = "1"

# Add the src/api directory to Python path so imports work correctly
src_api_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_api_path))
