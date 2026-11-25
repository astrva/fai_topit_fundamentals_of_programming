def calculate_statistics(values: list[int]) -> dict[str, int | float | None]:
    """За один проход считает сумму, минимум, максимум и количество четных."""
    if not values:
        return {
            "sum": 0,
            "min": None,
            "max": None,
            "even_count": 0,
            "mean": 0.0,
            "above_mean_count": 0,
        }

    total = 0
    min_value = values[0]
    max_value = values[0]
    even_count = 0

    for value in values:
        total += value
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value
        if value % 2 == 0:
            even_count += 1

    # Среднее известно после первого прохода, поэтому нужен второй проход.
    average = total / len(values)
    above_mean_count = 0
    for value in values:
        if value > average:
            above_mean_count += 1

    return {
        "sum": total,
        "min": min_value,
        "max": max_value,
        "even_count": even_count,
        "mean": average,
        "above_mean_count": above_mean_count,
    }


def linear_search(values: list[int], target: int) -> int:
    """Возвращает индекс первого вхождения target или -1."""
    for index in range(len(values)):
        if values[index] == target:
            return index
    return -1


def linear_search_with_count(values: list[int], target: int) -> tuple[int, int]:
    """Линейный поиск с подсчетом сравнений элементов с target."""
    comparisons = 0
    for index in range(len(values)):
        comparisons += 1
        if values[index] == target:
            return index, comparisons
    return -1, comparisons


def is_prime(number: int) -> bool:
    """Проверяет простоту положительного целого числа делителями до sqrt(n)."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def selection_sort(values: list[int]) -> tuple[list[int], int]:
    """Сортировка выбором; возвращает копию списка и число сравнений."""
    result = values.copy()
    comparisons = 0
    size = len(result)

    for index in range(size - 1):
        min_index = index
        for candidate in range(index + 1, size):
            comparisons += 1
            if result[candidate] < result[min_index]:
                min_index = candidate
        result[index], result[min_index] = result[min_index], result[index]

    return result, comparisons


def binary_search(values: list[int], target: int) -> tuple[int, int, int]:
    """Бинарный поиск; возвращает индекс, число сравнений и число итераций.

    Сравнением считается каждое фактическое сравнение элемента с target
    (операции == и < считаются отдельно).
    """
    left = 0
    right = len(values) - 1
    comparisons = 0
    iterations = 0

    while left <= right:
        iterations += 1
        middle = (left + right) // 2

        comparisons += 1  # values[middle] == target
        if values[middle] == target:
            return middle, comparisons, iterations

        comparisons += 1  # values[middle] < target
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1, comparisons, iterations


def run_checks() -> None:
    measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]
    stats = calculate_statistics(measurements)
    assert stats == {
        "sum": 144,
        "min": 7,
        "max": 21,
        "even_count": 4,
        "mean": 14.4,
        "above_mean_count": 6,
    }
    assert linear_search(measurements, 18) == 3
    assert linear_search(measurements, 100) == -1
    assert is_prime(2) is True
    assert is_prime(97) is True
    assert is_prime(1) is False
    assert is_prime(100) is False
    sorted_values, sort_comparisons = selection_sort([5, 1, 4, 2, 3])
    assert sorted_values == [1, 2, 3, 4, 5]
    assert sort_comparisons == 10
    assert binary_search(sorted_values, 4)[0] == 3
    assert binary_search(sorted_values, 9)[0] == -1
    assert calculate_statistics([])["min"] is None
    print("Проверки алгоритмов: OK")


def run_comparison_experiment() -> None:
    print("\n=== Сравнение линейного и бинарного поиска ===")
    print(f"{'Размер':>8} {'Линейный поиск':>18} {'Бинарный поиск':>18} {'Итерации БП':>14} {'Сортировка':>14}")
    for size in (10, 100, 1000):
        # Один и тот же искомый элемент отсутствует в обоих наборах.
        data = list(range(size, 0, -1))
        target = size + 1
        linear_index, linear_comparisons = linear_search_with_count(data, target)
        sorted_data, sort_comparisons = selection_sort(data)
        binary_index, binary_comparisons, binary_iterations = binary_search(sorted_data, target)
        assert linear_index == binary_index == -1
        print(
            f"{size:>8} {linear_comparisons:>18} {binary_comparisons:>18} "
            f"{binary_iterations:>14} {sort_comparisons:>14}"
        )


def main() -> None:
    measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]
    print("=== Исходные данные ===")
    print(measurements)

    stats = calculate_statistics(measurements)
    print("\n=== Статистика ===")
    print(f"Сумма: {stats['sum']}")
    print(f"Минимум: {stats['min']}")
    print(f"Максимум: {stats['max']}")
    print(f"Количество четных: {stats['even_count']}")
    print(f"Среднее: {stats['mean']:.2f}")
    print(f"Значений выше среднего: {stats['above_mean_count']}")

    print("\n=== Линейный поиск ===")
    try:
        target = int(input("Введите целое число для поиска: "))
    except ValueError:
        print("Ошибка: необходимо ввести целое число.")
    else:
        print(f"Индекс первого вхождения: {linear_search(measurements, target)}")

    print("\n=== Проверка простоты ===")
    for number in (2, 3, 4, 17, 25, 97, 100, 7919):
        state = "простое" if is_prime(number) else "составное"
        print(f"{number}: {state}")

    run_checks()
    run_comparison_experiment()


if __name__ == "__main__":
    main()
