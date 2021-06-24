try:
    from ._local import *
except ImportError:
    from .prod import *
