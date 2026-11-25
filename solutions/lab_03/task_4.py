from collections.abc import Callable, Sequence

course = "Python"  # Глобальная область видимости модуля.


def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое; для пустого списка — 0.0."""
    if not values:
        return 0.0
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def normalize_name(name: str) -> str:
    """Удаляет лишние пробелы и приводит каждую часть имени к формату Title."""
    if not name or not name.strip():
        return ""
    parts = name.strip().split()
    normalized_parts = [part.capitalize() for part in parts]
    return " ".join(normalized_parts)


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    """Формирует строковый отчет; precision и prefix — только именованные."""
    if precision < 0:
        return f"{prefix}: некорректная точность"
    if not results:
        return f"{prefix}: {student} — нет результатов"
    average = arithmetic_mean(results)
    return f"{prefix}: {student} — среднее {average:.{precision}f}"


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    cleaned_tags: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        if not tag or not tag.strip():
            continue
        cleaned = tag.strip()
        if lowercase:
            cleaned = cleaned.lower()
        if cleaned not in seen:
            seen.add(cleaned)
            cleaned_tags.append(cleaned)
    return tuple(cleaned_tags)


def apply_to_results(
    operation: Callable[[float], float],
    values: Sequence[float],
) -> list[float]:
    """Применяет переданную функцию к каждому значению без изменения входа."""
    return [operation(value) for value in values]


def make_threshold_checker(threshold: int) -> Callable[[int], bool]:
    """Создает проверку, сохраняющую threshold в замыкании."""
    def checker(value: int) -> bool:
        return value >= threshold

    return checker


def add_result(value: int, results: list[int] | None = None) -> list[int]:
    """Безопасно добавляет результат; новый список создается при results=None."""
    if results is None:
        results = []
    results.append(value)
    return results


def run_assertions() -> None:
    """Не менее трех assert-проверок для каждой обязательной функции."""
    assert arithmetic_mean([1, 2, 3]) == 2.0
    assert arithmetic_mean([10]) == 10.0
    assert arithmetic_mean([]) == 0.0

    assert normalize_name("  anna  pavlovna  ") == "Anna Pavlovna"
    assert normalize_name("ivan") == "Ivan"
    assert normalize_name("   ") == ""

    assert build_report("Anna", [80, 90]) == "Результат: Anna — среднее 85.00"
    assert build_report("Ivan", [100], precision=0) == "Результат: Ivan — среднее 100"
    assert build_report("Petr", [], prefix="Оценка") == "Оценка: Petr — нет результатов"

    assert collect_tags("Python", "python", "PYTHON") == ("python",)
    assert collect_tags("A", "", "B", "A") == ("a", "b")
    assert collect_tags(" Tag ", lowercase=False) == ("Tag",)

    source_values = [1, 2, 3]
    assert apply_to_results(lambda value: value * 2, source_values) == [2, 4, 6]
    assert apply_to_results(lambda value: value + 1, [0]) == [1]
    assert source_values == [1, 2, 3]

    checker_80 = make_threshold_checker(80)
    checker_90 = make_threshold_checker(90)
    assert checker_80(85) is True
    assert checker_90(85) is False
    assert checker_90(90) is True

    assert add_result(1) == [1]
    assert add_result(2) == [2]
    existing = [5]
    assert add_result(6, existing) == [5, 6]
    print("Проверки функций: OK")


def demonstrate_legb() -> None:
    """Показывает nonlocal: меняется enclosing, global остается прежним."""
    def outer_function() -> str:
        course = "Algorithms"  # Enclosing scope

        def inner_function() -> str:
            nonlocal course
            course = "Databases"
            print(f"Внутри inner_function: {course}")  # Local -> Enclosing
            return course

        print(f"До inner_function: {course}")
        inner_function()
        print(f"После inner_function: {course}")
        return course

    print(f"Global до вызова: {course}")
    enclosing_value = outer_function()
    print(f"Global после вызова: {course}")
    assert enclosing_value == "Databases"
    assert course == "Python"


def demonstrate_unpacking_and_closures() -> None:
    print("\n=== Распаковка аргументов ===")
    tags_list = [" Python ", "Algorithms", "python"]
    print("Распаковка списка через *:", collect_tags(*tags_list))

    report_options = {"precision": 1, "prefix": "Итог"}
    print("Распаковка словаря через **:", build_report("Anna", [85, 90, 95], **report_options))

    print("\n=== Функция высшего порядка ===")
    values = [1, 2, 3, 4]

    def square(value: float) -> float:
        return value ** 2

    print("Именованная функция:", apply_to_results(square, values))
    print("Lambda:", apply_to_results(lambda value: value ** 3, values))

    print("\n=== Замыкания ===")
    checker_80 = make_threshold_checker(80)
    checker_90 = make_threshold_checker(90)
    test_scores = [75, 85, 95]
    print("Порог 80:", [checker_80(score) for score in test_scores])
    print("Порог 90:", [checker_90(score) for score in test_scores])
    print("Сохраненный threshold для checker_80:", checker_80.__closure__[0].cell_contents)
    print("Сохраненный threshold для checker_90:", checker_90.__closure__[0].cell_contents)
    assert checker_80.__closure__[0].cell_contents == 80
    assert checker_90.__closure__[0].cell_contents == 90


def demonstrate_mutable_default_fix() -> None:
    """Показывает независимые списки в исправленной функции add_result."""
    print("\n=== Исправление изменяемого значения по умолчанию ===")
    print(add_result(1))
    print(add_result(2))
    print(add_result(3))
    print("Каждый вызов без списка получает новый объект.")


def main() -> None:
    run_assertions()
    demonstrate_legb()
    demonstrate_unpacking_and_closures()
    demonstrate_mutable_default_fix()


if __name__ == "__main__":
    main()
