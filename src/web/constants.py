import os
from typing import Final

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR: Final = os.path.join(APP_ROOT, "static")
TEMPLATE_DIR: Final = os.path.join(APP_ROOT, "templates")
