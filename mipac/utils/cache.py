from __future__ import annotations

from functools import lru_cache, wraps
from typing import Any

DEFAULT_CACHE: dict[str, "LRUCache"] = {}


class Node:
    """キャッシュのノード

    Attributes
    ----------
    key : str
        キャッシュのキー
    value : Any
        キャッシュの値
    next : ListNode
        次のノード
    prev : ListNode
        前のノード
    """

    def __init__(self, key: str, value: Any) -> None:
        self.key: str = key
        self.value: Any = value
        self.next: Node | None = None
        self.prev: Node | None = None


class LRUCache:
    def __init__(self, capacity: int = 100) -> None:
        self.items: dict[str, Node] = {}
        # headとtailはダミーノード、この間にノードを追加していく
        self.head_node = Node("", 0)
        self.tail_node = Node("", 0)
        self.head_node.next = self.tail_node  # 先頭 => 末尾
        self.tail_node.prev = self.head_node  # 先頭 <= 末尾
        self.capacity = capacity

    def _remove_node(self, node: Node):
        if node.prev:  # 削除対象の前にいるnodeのnextを削除対象の次のnodeに変更
            node.prev.next = node.next

        if node.next:  # 削除対象の次のnodeのprevを削除対象の前のnodeに変更
            node.next.prev = node.prev

        del self.items[node.key]

    def _add(self, node: Node):
        prev_node = self.tail_node.prev
        next_node = self.tail_node

        if prev_node:
            prev_node.next = node
            node.prev = prev_node

        if next_node:
            next_node.prev = node
            node.next = next_node

        self.items[node.key] = node

    def get(self, key: str) -> Any:
        if key not in self.items:
            raise KeyError

        node = self.items[key]

        # 一度削除して追加しなおすことで最新のノードとして更新する
        self._remove_node(node)
        self._add(node)

        return node.value

    def put(self, key: str, value: Any):
        if key in self.items:  # 既に同一のキーが存在する場合は再登録するために一度消す
            self._remove_node(self.items[key])

        node = Node(key, value)
        self._add(node)

        if len(self.items) > self.capacity:
            if self.head_node.next:  # 基本存在するはずだけど型的に一応やっとく
                self._remove_node(self.head_node.next)


def cache(group: str = "default", override: bool = False):
    """キャッシュを行います"""

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            key = cache_key_builder(func, self, *args, **kwargs)
            target_cache = DEFAULT_CACHE.get(group)

            if target_cache is None:
                target_cache = LRUCache()
                DEFAULT_CACHE[group] = target_cache

            try:
                hit_item = target_cache.get(key)
                if hit_item and override is False and kwargs.get("cache_override") is None:
                    return hit_item
            except KeyError:
                res = await func(self, *args, **kwargs)
                target_cache.put(key, res)
                return res

        return wrapper

    return decorator


@lru_cache
def cache_key_builder(func, cls, *args, **kwargs):
    """キャッシュのキーを作成します"""
    ordered_kwargs = sorted(kwargs.items())
    key = (func.__module__ or "") + ".{0}" + f"{cls}" + str(args) + str(ordered_kwargs)
    return key
