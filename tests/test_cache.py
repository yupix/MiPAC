import pytest

from mipac.utils.cache import LRUCache


def test_lru_cache_holds_up_to_capacity():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_lru_cache_evicts_least_recently_used_past_capacity():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # a becomes most recently used
    cache.put("c", 3)
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    with pytest.raises(KeyError):
        cache.get("b")


def test_lru_cache_put_existing_key_updates_value_without_growing():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("a", 2)
    assert cache.get("a") == 2
    assert len(cache.items) == 1
