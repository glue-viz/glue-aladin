from .qt import setup as qt_setup

try:
    qt_setup()
except ImportError:
    pass
