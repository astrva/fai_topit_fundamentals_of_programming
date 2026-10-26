print("A")
a = 10
b = a

print('до изменений')
print(a, b)
print(id(a), id(b))

a += 1

print('после изменений')
print(a, b)
print(id(a), id(b))

print()

print('B')

first = [10, 20]
second = first

print('до изменений')
print(first, second)
print(id(first), id(second))

second.append(30)


print(first, second)
print(id(first), id(second))

second = [10, 20, 30]

print('после изменений')
print(first == second)
print(first is second)
print(id(first), id(second))
second.append(1)
print(first, second)

print()
print('Практическая задача')
config1 = {
    "Название": "Учебный проект 1",
    "Список участников": ["Петя", "Вася"],
    "Параметры запуска": {"Время": 30, "Количество запусков": 3}
}


config_bad = config1
config_bad["Список участников"].append("Андрей")
config_bad["Параметры запуска"]["Время"] = 60

print("После изменения config_bad:")
print(f"config1: {config1}")
print(f"config_bad: {config_bad}")
print(config1['Список участников'] is config_bad['Список участников'])


import copy
config_good = copy.deepcopy(config1)
config_good["Название"] = "Учебный проект 2"
config_good["Список участников"].append("Артем")
config_good["Параметры запуска"]["Время"] = 80

print("После изменения config_good:")
print(f"config1: {config1}")
print(f"config_good: {config_good}")


assert config1["Название"] != config_good["Название"]
assert config1["Список участников"] is not config_good["Список участников"]
assert config1["Параметры запуска"] is not config_good["Параметры запуска"]
print('config1 и config_good независимы')
