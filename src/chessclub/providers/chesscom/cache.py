"""Compatibility module for Chess.com response cache.

Re-exports SQLiteCache and CachedResponse from chessclub.providers.cache.
"""

from chessclub.providers.cache import CachedResponse, SQLiteCache

__all__ = ["CachedResponse", "SQLiteCache"]
