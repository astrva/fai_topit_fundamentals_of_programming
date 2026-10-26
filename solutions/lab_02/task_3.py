import sys
import weakref

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))

class Record:
    pass


record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())

registry = weakref.WeakValueDictionary()

r1 = Record()
r2 = Record()
r3 = Record()

registry[1] = r1
registry[2] = r2
registry[3] = r3

print(f"Реестр до удалений: {list(registry.keys())}")
del r3
print(f"Реестр после del r3: {list(registry.keys())}")
del r2
print(f"Реестр после del r2: {list(registry.keys())}")
print(f"r1 все еще жив: {r1}")
