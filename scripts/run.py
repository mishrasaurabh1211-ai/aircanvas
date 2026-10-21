import sys
from pathlib import Path

# Ensures the aircanvas package is importable when run directly as a script
sys.path.insert(0, str(Path(__file__).parent.parent))

from aircanvas.app.main import run

if __name__ == "__main__":
    print("Starting AirCanvas... (Press 'q' to quit)")
    run()