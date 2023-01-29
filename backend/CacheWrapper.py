import random
from collections import OrderedDict


class CacheWrapper:

    def __init__(self, capacity: int):
        self.memcache = OrderedDict()
        self.capacity = capacity
        self.accessCount = 0
        self.hit = 0
        self.entryNum = 0
        self.cacheInvalidations = 0

    def get(self, key):
        self.accessCount += 1
        if key not in self.memcache:
            return -1
        else:
            self.hit += 1
            self.memcache.move_to_end(key, last=False)
            return self.memcache[key]

    def put(self, key, value):
        # self.memcache.__setitem__(key, value)
        # self.memcache.update({key, value})
        self.memcache[key] = value
        self.memcache.move_to_end(key)
        self.entryNum += 1
        self.LRUReplacement()

    def LRUReplacement(self) -> None:
        if len(self.memcache) > self.capacity:
            self.memcache.popitem(last=False)
            self.entryNum -= 1

    def RNDReplacement(self) -> None:
        if len(self.memcache) > self.capacity:
            replace = random.randint(0, self.capacity)
            index = 0
            keyInd = self.memcache.__iter__()
            while index != replace:
                keyInd = next(keyInd)
                index += 1
            self.memcache.popitem(keyInd)
            self.entryNum -= 1

    def clear(self) -> None:
        self.entryNum = 0
        return self.memcache.clear()

    def invalidateKey(self, key):
        self.memcache.popitem(key)
        self.cacheInvalidations += 1

    def refreshConfigurations(self, capacity: int):
        self.capacity = capacity

    def displayStats(self):
        if(self.accessCount != 0):
            return {'capacity': self.capacity,
                    'accessCount': self.accessCount,
                    'hit': self.hit,
                    'entryNum': self.entryNum,
                    'hitRatio': self.hit / self.accessCount,
                    'cacheInvalidations' : self.cacheInvalidations
                    }
        else:
            return {'capacity': self.capacity,
                    'accessCount': self.accessCount,
                    'hit': self.hit,
                    'entryNum': self.entryNum,
                    'cacheInvalidations' : self.cacheInvalidations
                    }

