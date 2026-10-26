import copy

original = [
    ["Python", 5],
    ["Algorithms", 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

def print_ids(structures):
    print("Идентификаторы:")
    for name, obj in structures.items():
        print(f"{name}: outer={id(obj)}, inner0={id(obj[0])}, grade0={id(obj[0][1])}")

print("Исходное состояние")
print(f"original: {original}")
print(f"alias: {alias}")
print(f"shallow: {shallow}")
print(f"deep: {deep}")
print_ids({"original": original, "alias": alias, "shallow": shallow, "deep": deep})
print()
print("После original.append(['Databases', 5])")
original.append(["Databases", 5])
print(f"original: {original}")
print(f"alias: {alias}")
print(f"shallow: {shallow}")
print(f"deep: {deep}")
print()
print("После original[0][1] = 3")
original[0][1] = 3
print(f"original: {original}")
print(f"alias: {alias}")
print(f"shallow: {shallow}")
print(f"deep: {deep}")
print_ids({"original": original, "alias": alias, "shallow": shallow, "deep": deep})
print()
print("Исследование матриц")
wrong_matrix = [[0] * 3] * 3
print(f"wrong_matrix до: {wrong_matrix}")
print(f"id строк wrong_matrix: {[id(row) for row in wrong_matrix]}")
wrong_matrix[0][0] = 1
print(f"wrong_matrix после wrong_matrix[0][0] = 1: {wrong_matrix}")
print()
correct_matrix = [[0] * 3 for _ in range(3)]
print(f"correct_matrix до: {correct_matrix}")
print(f"id строк correct_matrix: {[id(row) for row in correct_matrix]}")
correct_matrix[0][0] = 1
print(f"correct_matrix после correct_matrix[0][0] = 1: {correct_matrix}")
