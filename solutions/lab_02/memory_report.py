import sys
import tracemalloc

n = 100_000


tracemalloc.start()
numbers_list = list(range(n))
current1, peak1 = tracemalloc.get_traced_memory()
size1 = sys.getsizeof(numbers_list)
tracemalloc.stop()


tracemalloc.start()
numbers_range = range(n)
current2, peak2 = tracemalloc.get_traced_memory()
size2 = sys.getsizeof(numbers_range)
tracemalloc.stop()



results = [
    {
        "scenario": "list(range(N))",
        "elements": n,
        "outer_size": size1,
        "current_kb": current1 / 1024,
        "peak_kb": peak1 / 1024
    },
    {
        "scenario": "range(N)",
        "elements": n,
        "outer_size": size2,
        "current_kb": current2 / 1024,
        "peak_kb": peak2 / 1024
    }
]


for r in results:
    print(f"Сценарий: {r['scenario']}")
    print(f"  Число элементов: {r['elements']}")
    print(f"  Размер внешнего объекта: {r['outer_size']} байт")
    print(f"  Текущая память: {r['current_kb']:.2f} KB")
    print(f"  Пиковая память: {r['peak_kb']:.2f} KB")

ratio = results[0]['peak_kb'] / results[1]['peak_kb'] if results[1]['peak_kb'] > 0 else 0
print(f"Отношение пикового объема: {ratio:.0f} к 1")
