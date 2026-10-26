import gc

first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)

print("GC включен:", gc.isenabled())
print("Пороги поколений:", gc.get_threshold())
print("Статистика поколений:", gc.get_stats())

id_first = id(first)
id_second = id(second)
print(f"id(first) = {id_first}")
print(f"id(second) = {id_second}")

del first
del second
collected = gc.collect()
print(f"gc.collect() вернул: {collected}")


gc.disable()

cycle1 = []
cycle2 = []
cycle1.append(cycle2)
cycle2.append(cycle1)
cycle3 = []
cycle4 = []
cycle3.append(cycle4)
cycle4.append(cycle3)

del cycle1
del cycle2
del cycle3
del cycle4

collected_manual = gc.collect()
print(f"Ручной gc.collect() собрал: {collected_manual}")

gc.enable()


node1 = {"id": 1}
node2 = {"id": 2}
node3 = {"id": 3}
node4 = {"id": 4}

node1["next"] = node2
node2["next"] = node3
node3["next"] = node1

print(f"node1 -> node2: {node1['next']['id']}")
print(f"node2 -> node3: {node2['next']['id']}")
print(f"node3 -> node1: {node3['next']['id']}")
print(f"node4 независим: {node4['id']}")

before = gc.get_count()
del node1
del node2
del node3
collected_graph = gc.collect()
after = gc.get_count()

print(f"До сборки: {before}")
print(f"Собрано объектов: {collected_graph}")
print(f"После сборки: {after}")
print(f"node4 доступен: {node4['id']}")
