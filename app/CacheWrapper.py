import random
from collections import OrderedDict


class CacheWrapper:

    def __init__(self, capacity: int):
        self.memcache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.memcache:
            return -1
        else:
            self.memcache.move_to_end(key)
            return self.memcache[key]

    def put(self, key, value):
        self.memcache[key] = value
        self.memcache.move_to_end(key)

    def LRUReplacement(self) -> None:
        if len(self.memcache) > self.capacity:
            self.memcache.popitem(last=False)

    def RNDReplacement(self) -> None:
        if len(self.memcache) > self.capacity:
            replace = random.randint(0, self.capacity)
            index = 0
            keyInd = self.memcache.__iter__()
            while index != replace:
                keyInd = next(keyInd)
                index += 1
            self.memcache.pop(keyInd)

    def clear(self) -> None:
        return self.memcache.clear()

    def invalidateKey(self, key):
        self.memcache.pop(key)

    def refreshConfigurations(self, capacity: int):
        self.capacity = capacity
