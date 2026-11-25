
LEVELS = ("отличный", "хороший", "удовлетворительный", "недостаточный")
WORK_TYPES = {
    "exam": "экзаменационная работа",
    "project": "проектная работа",
    "practice": "практическая работа",
}


def classify_result(score: int, work_type: str, absences: int) -> dict[str, object]:
    """Проверяет запись и возвращает уровень, пояснение и текст результата."""
    # Проверка диапазонов выполняется до классификации.
    if score < 0 or score > 100:
        return {
            "valid": False,
            "level": None,
            "message": f"Ошибка: результат {score} вне диапазона 0-100",
        }
    elif absences < 0 or absences > 5:
        return {
            "valid": False,
            "level": None,
            "message": f"Ошибка: количество пропусков {absences} вне диапазона 0-5",
        }
    else:
        # Базовый уровень определяется сверху вниз.
        if score >= 90:
            level = LEVELS[0]
        elif score >= 75:
            level = LEVELS[1]
        elif score >= 60:
            level = LEVELS[2]
        else:
            level = LEVELS[3]

    # Более трех пропусков снижают уровень на одну ступень.
    if absences > 3:
        level_index = LEVELS.index(level)
        if level_index < len(LEVELS) - 1:
            level = LEVELS[level_index + 1]

    # Для неизвестного типа работы предусмотрена отдельная ветвь.
    match work_type:
        case "exam":
            work_description = "экзаменационная работа"
        case "project":
            work_description = "проектная работа"
        case "practice":
            work_description = "практическая работа"
        case _:
            work_description = "неизвестный тип работы"

    return {
        "valid": True,
        "level": level,
        "message": (
            f"Результат: {score}, уровень: {level}, "
            f"тип: {work_description}, пропуски: {absences}"
        ),
    }


def run_tests() -> None:
    """Проверяет границы диапазонов и дополнительные ветви."""
    test_cases = [
        (0, "exam", 0, "недостаточный"),
        (59, "project", 2, "недостаточный"),
        (60, "practice", 3, "удовлетворительный"),
        (74, "exam", 4, "недостаточный"),
        (75, "project", 1, "хороший"),
        (89, "practice", 5, "удовлетворительный"),
        (90, "exam", 0, "отличный"),
        (100, "project", 3, "отличный"),
    ]

    print("=== Тестовые сценарии ===")
    for score, work_type, absences, expected_level in test_cases:
        result = classify_result(score, work_type, absences)
        assert result["valid"] is True
        assert result["level"] == expected_level
        print(f"({score}, {work_type}, {absences}) -> {result['message']} [OK]")

    invalid_score = classify_result(-1, "exam", 0)
    invalid_absences = classify_result(80, "exam", 6)
    unknown_type = classify_result(80, "unknown", 0)
    assert invalid_score["valid"] is False
    assert invalid_absences["valid"] is False
    assert "неизвестный тип работы" in str(unknown_type["message"])
    print(f"Дополнительные проверки: {invalid_score['message']}; {invalid_absences['message']}; неизвестный тип обработан [OK]")


def run_practical_extension() -> None:
    """Обрабатывает десять записей и подсчитывает распределение уровней."""
    students_data = [
        (95, "exam", 1),
        (82, "project", 2),
        (67, "practice", 0),
        (45, "exam", 4),
        (78, "project", 4),
        (91, "practice", 3),
        (60, "exam", 5),
        (88, "project", 1),
        (73, "practice", 2),
        (100, "exam", 0),
    ]
    original_data = students_data.copy()
    level_counts = {level: 0 for level in LEVELS}

    print("\n=== Практическое расширение: 10 записей ===")
    for record in students_data:
        result = classify_result(*record)
        print(result["message"])
        if result["valid"]:
            level = str(result["level"])
            level_counts[level] += 1

    assert students_data == original_data  # исходный список не изменен
    print("\n=== Итоговая сводка ===")
    for level in LEVELS:
        print(f"{level}: {level_counts[level]}")
    assert level_counts == {
        "отличный": 3,
        "хороший": 2,
        "удовлетворительный": 3,
        "недостаточный": 2,
    }


def main() -> None:
    run_tests()
    run_practical_extension()


if __name__ == "__main__":
    main()
