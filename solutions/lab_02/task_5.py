import sys
import tracemalloc

# Часть 1
empty_list = []
list_10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tuple_10 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
str_10 = "1234567890"
int_obj = 42
none_obj = None

print("Пустой список:", sys.getsizeof(empty_list))
print("Список из 10 int:", sys.getsizeof(list_10))
print("Кортеж из 10 int:", sys.getsizeof(tuple_10))
print("Строка из 10 символов:", sys.getsizeof(str_10))
print("Целое число:", sys.getsizeof(int_obj))
print("None:", sys.getsizeof(none_obj))

# Часть 2
lst = []
prev_size = sys.getsizeof(lst)
print(f"Длина: {len(lst)}, Размер: {prev_size}")

for i in range(100):
    lst.append(i)
    current_size = sys.getsizeof(lst)
    if current_size != prev_size:
        print(f"Длина: {len(lst)}, Размер: {current_size}")
        prev_size = current_size

# Часть 3
tracemalloc.start()
numbers_list = list(range(100_000))
current1, peak1 = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
numbers_range = range(100_000)
current2, peak2 = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"list(range(100_000)): текущий={current1/1024:.2f} KB, пиковый={peak1/1024:.2f} KB")
print(f"range(100_000): текущий={current2/1024:.2f} KB, пиковый={peak2/1024:.2f} KB")
