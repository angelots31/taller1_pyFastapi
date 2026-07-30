import os
import sys

# Permite que los tests hagan "from models import trainee_model", etc.,
# igual que lo hace src/main.py, sin importar desde dónde se ejecute pytest.
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
