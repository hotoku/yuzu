__version__ = "4.0.0"

from .logging import (
    setup_logging as setup_logging,
    get_annotation as get_annotation
)
from .cache import (
    cache as cache,
    activate_cache as activate_cache,
    deactivate_cache as deactivate_cache,
    clear_cache as clear_cache
)
