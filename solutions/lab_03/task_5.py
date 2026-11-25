from collections.abc import Mapping, Sequence

STUDENTS = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}

CATEGORIES = (
    "отличный",
    "хороший",
    "удовлетворительный",
    "недостаточный",
    "нет данных",
)


def mean(values: Sequence[float]) -> float:
    """Возвращает среднее значение; для пустой последовательности — 0.0."""
    if not values:
        return 0.0
    total = 0.0
    count = 0
    for value in values:
        total += value
        count += 1
    return total / count


def minimum(values: Sequence[float]) -> float | None:
    """Возвращает минимум без min(); для пустой последовательности — None."""
    if not values:
        return None
    min_value = values[0]
    for index in range(1, len(values)):
        if values[index] < min_value:
            min_value = values[index]
    return min_value


def maximum(values: Sequence[float]) -> float | None:
    """Возвращает максимум без max(); для пустой последовательности — None."""
    if not values:
        return None
    max_value = values[0]
    for index in range(1, len(values)):
        if values[index] > max_value:
            max_value = values[index]
    return max_value


def classify(score: float) -> str:
    """Классифицирует средний балл по заданным границам."""
    if score >= 90:
        return "отличный"
    elif score >= 75:
        return "хороший"
    elif score >= 60:
        return "удовлетворительный"
    else:
        return "недостаточный"


def student_summary(name: str, results: Sequence[float]) -> dict[str, object]:
    """Формирует статистику студента; пустой список получает категорию «нет данных»."""
    if not results:
        return {
            "name": name,
            "mean": 0.0,
            "min": None,
            "max": None,
            "category": "нет данных",
            "count": 0,
        }

    average = mean(results)
    return {
        "name": name,
        "mean": average,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(average),
        "count": len(results),
    }


def find_top_students(students: Mapping[str, Sequence[float]]) -> list[str]:
    """Возвращает всех студентов с максимальным средним, пропуская пустые списки."""
    best_mean: float | None = None
    leaders: list[str] = []

    for name, results in students.items():
        if not results:
            continue
        current_mean = mean(results)
        if best_mean is None or current_mean > best_mean:
            best_mean = current_mean
            leaders = [name]
        elif current_mean == best_mean:
            leaders.append(name)
    return leaders


def _build_rating(summaries: list[dict[str, object]]) -> list[dict[str, object]]:
    """Строит рейтинг по убыванию среднего методом вставок без sorted()."""
    rating = [item.copy() for item in summaries if item["count"] > 0]
    for index in range(1, len(rating)):
        current = rating[index]
        position = index - 1
        while position >= 0 and float(rating[position]["mean"]) < float(current["mean"]):
            rating[position + 1] = rating[position]
            position -= 1
        rating[position + 1] = current
    return rating


def group_summary(students: Mapping[str, Sequence[float]]) -> dict[str, object]:
    """Формирует сводку группы и рейтинг, не изменяя исходный словарь.

    Общий средний балл — среднее по всем попыткам всех студентов (взвешенный
    по количеству результатов показатель). Студенты без результатов
    учитываются в количестве студентов и категории «нет данных», но не входят
    в расчет среднего балла.
    """
    summaries = [student_summary(name, results) for name, results in students.items()]
    categories = {category: 0 for category in CATEGORIES}
    total_sum = 0.0
    total_results = 0

    for summary in summaries:
        category = str(summary["category"])
        categories[category] += 1
        name = str(summary["name"])
        results = students[name]
        for value in results:
            total_sum += value
            total_results += 1

    total_mean = total_sum / total_results if total_results else 0.0
    rating = _build_rating(summaries)

    return {
        "student_count": len(students),
        "result_count": total_results,
        "total_mean": total_mean,
        "categories": categories,
        "summaries": summaries,
        "rating": rating,
        "top_students": find_top_students(students),
    }


def format_report(
    student_data: Sequence[Mapping[str, object]],
    group_data: Mapping[str, object],
) -> str:
    """Формирует итоговый отчет по списку сводок студентов и сводке группы."""
    lines = ["=" * 68, "ОТЧЕТ ПО УЧЕБНЫМ РЕЗУЛЬТАТАМ", "=" * 68]
    lines.append("\nРезультаты студентов:")

    if not student_data:
        lines.append("  Нет данных о студентах.")
    for summary in student_data:
        lines.append(f"  {summary['name']}:")
        lines.append(f"    Средний балл: {float(summary['mean']):.2f}")
        lines.append(f"    Минимум / максимум: {summary['min']} / {summary['max']}")
        lines.append(f"    Категория: {summary['category']}")
        lines.append(f"    Количество результатов: {summary['count']}")

    lines.append("\nРейтинг (по убыванию среднего балла):")
    rating = group_data["rating"]
    if not rating:
        lines.append("  Нет студентов с результатами.")
    for place, summary in enumerate(rating, start=1):
        lines.append(f"  {place}. {summary['name']} — {float(summary['mean']):.2f}")

    lines.append("\nОбщая статистика:")
    lines.append(f"  Количество студентов: {group_data['student_count']}")
    lines.append(f"  Количество результатов: {group_data['result_count']}")
    lines.append(f"  Средний балл по всем результатам: {float(group_data['total_mean']):.2f}")
    lines.append("  Распределение по категориям:")
    categories = group_data["categories"]
    for category in CATEGORIES:
        lines.append(f"    {category}: {categories[category]}")
    lines.append(f"  Лидер(ы): {', '.join(group_data['top_students']) or 'нет'}")
    return "\n".join(lines)


def run_scenarios() -> None:
    """Проверяет шесть обязательных сценариев и контракты функций."""
    # Базовые функции.
    assert mean([1, 2, 3]) == 2.0
    assert mean([]) == 0.0
    assert minimum([4, 1, 7]) == 1
    assert minimum([]) is None
    assert maximum([4, 1, 7]) == 7
    assert maximum([]) is None
    assert classify(90) == "отличный"
    assert classify(75) == "хороший"
    assert classify(60) == "удовлетворительный"
    assert classify(59) == "недостаточный"

    # 1. Обычный набор данных.
    original = {name: values.copy() for name, values in STUDENTS.items()}
    normal = group_summary(STUDENTS)
    assert normal["student_count"] == 4
    assert normal["top_students"] == ["Дарья"]
    assert STUDENTS == original

    # 2. Один студент.
    one_student = {"Анна": [85, 90, 88]}
    one_summary = group_summary(one_student)
    assert one_summary["student_count"] == 1
    assert one_summary["top_students"] == ["Анна"]

    # 3. Несколько лидеров.
    tied = {"Анна": [90, 90], "Борис": [90, 90], "Дарья": [80]}
    assert find_top_students(tied) == ["Анна", "Борис"]

    # 4. Пустая группа.
    empty_group = group_summary({})
    assert empty_group["student_count"] == 0
    assert empty_group["total_mean"] == 0.0
    assert empty_group["summaries"] == []
    assert "Нет данных" in format_report([], empty_group)

    # 5. Студент без результатов.
    no_results = student_summary("Борис", [])
    assert no_results["category"] == "нет данных"
    assert no_results["min"] is None and no_results["max"] is None
    mixed_group = group_summary({"Анна": [85, 90], "Борис": []})
    assert mixed_group["categories"]["нет данных"] == 1
    assert mixed_group["total_mean"] == 87.5

    # 6. Граничные значения категорий.
    boundary = {
        "90": student_summary("90", [90]),
        "75": student_summary("75", [75]),
        "60": student_summary("60", [60]),
        "59": student_summary("59", [59]),
    }
    assert boundary["90"]["category"] == "отличный"
    assert boundary["75"]["category"] == "хороший"
    assert boundary["60"]["category"] == "удовлетворительный"
    assert boundary["59"]["category"] == "недостаточный"

    # Проверка форматирования и построения рейтинга.
    report = format_report(normal["summaries"], normal)
    assert "ОТЧЕТ ПО УЧЕБНЫМ РЕЗУЛЬТАТАМ" in report
    assert "Рейтинг" in report
    print("Проверки анализатора и шести сценариев: OK")


def main() -> None:
    run_scenarios()
    group_data = group_summary(STUDENTS)
    report = format_report(group_data["summaries"], group_data)
    print("\n" + report)


if __name__ == "__main__":
    main()
