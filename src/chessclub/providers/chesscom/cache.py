"""Re-exports from the shared cache module.

Kept for backward compatibility — prefer importing from
:mod:`chessclub.providers.cache` instead.
"""

from chessclub.providers.cache import CachedResponse, SQLiteCache

__all__ = ["CachedResponse", "SQLiteCache"]
