SUBMISSIONS = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]


def build_structures(submissions: list[tuple[str, str, int]]) -> dict[str, object]:
    """Создает множества и словари по исходному списку попыток."""
    students_set: set[str] = set()
    labs_set: set[str] = set()
    student_attempts: dict[str, list[tuple[str, int]]] = {}
    best_results: dict[tuple[str, str], int] = {}
    attempts_count: dict[tuple[str, str], int] = {}
    lab_students: dict[str, set[str]] = {}

    for student, lab, score in submissions:
        add_submission_to_structures(
            (student, lab, score),
            students_set,
            labs_set,
            student_attempts,
            best_results,
            attempts_count,
            lab_students,
        )

    return {
        "students_set": students_set,
        "labs_set": labs_set,
        "student_attempts": student_attempts,
        "best_results": best_results,
        "attempts_count": attempts_count,
        "lab_students": lab_students,
    }


def add_submission_to_structures(
    submission: tuple[str, str, int],
    students_set: set[str],
    labs_set: set[str],
    student_attempts: dict[str, list[tuple[str, int]]],
    best_results: dict[tuple[str, str], int],
    attempts_count: dict[tuple[str, str], int],
    lab_students: dict[str, set[str]],
) -> None:
    """Добавляет одну попытку в существующие структуры без их перестроения."""
    student, lab, score = submission
    students_set.add(student)
    labs_set.add(lab)

    if student not in student_attempts:
        student_attempts[student] = []
    student_attempts[student].append((lab, score))

    key = (student, lab)
    if key not in best_results or score > best_results[key]:
        best_results[key] = score
    attempts_count[key] = attempts_count.get(key, 0) + 1

    if lab not in lab_students:
        lab_students[lab] = set()
    lab_students[lab].add(student)


def students_with_both_labs(lab_students: dict[str, set[str]]) -> set[str]:
    """Возвращает студентов, сдававших и lab_01, и lab_02."""
    lab_01_students = lab_students.get("lab_01", set())
    lab_02_students = lab_students.get("lab_02", set())
    return lab_01_students & lab_02_students


def process_query(query: str, structures: dict[str, object]) -> str:
    """Обрабатывает команды student, best, attempts и completed."""
    parts = query.strip().split()
    if not parts:
        return "Пустой запрос"

    command = parts[0]
    student_attempts = structures["student_attempts"]
    best_results = structures["best_results"]
    attempts_count = structures["attempts_count"]
    lab_students = structures["lab_students"]

    match command:
        case "student":
            if len(parts) != 2:
                return "Ошибка: формат команды — student <имя>"
            name = parts[1]
            if name not in student_attempts:
                return f"Студент {name} не найден"
            return f"Попытки {name}: {student_attempts[name]}"

        case "best":
            if len(parts) != 3:
                return "Ошибка: формат команды — best <имя> <лабораторная>"
            key = (parts[1], parts[2])
            if key not in best_results:
                return f"Лучший результат для {key} не найден"
            return f"Лучший результат {key[0]} на {key[1]}: {best_results[key]}"

        case "attempts":
            if len(parts) != 3:
                return "Ошибка: формат команды — attempts <имя> <лабораторная>"
            key = (parts[1], parts[2])
            if key not in attempts_count:
                return f"Попытки для {key} не найдены"
            return f"Количество попыток {key[0]} на {key[1]}: {attempts_count[key]}"

        case "completed":
            if len(parts) != 2:
                return "Ошибка: формат команды — completed <лабораторная>"
            lab = parts[1]
            if lab not in lab_students:
                return f"Для {lab} пока нет сдач"
            return f"Студенты, сдававшие {lab}: {sorted(lab_students[lab])}"

        case _:
            return f"Неизвестная команда: {command}"


def run_checks(structures: dict[str, object]) -> None:
    """Проверяет построение структур, инкрементальное обновление и запросы."""
    assert structures["students_set"] == {"anna", "boris", "daria"}
    assert structures["labs_set"] == {"lab_01", "lab_02"}
    assert structures["best_results"][("anna", "lab_01")] == 5
    assert structures["attempts_count"][("anna", "lab_01")] == 2
    assert students_with_both_labs(structures["lab_students"]) == {"anna", "boris"}

    add_submission_to_structures(
        ("daria", "lab_02", 4),
        structures["students_set"],
        structures["labs_set"],
        structures["student_attempts"],
        structures["best_results"],
        structures["attempts_count"],
        structures["lab_students"],
    )
    assert students_with_both_labs(structures["lab_students"]) == {"anna", "boris", "daria"}
    assert "daria" in process_query("completed lab_02", structures)
    assert "не найден" in process_query("best unknown lab_01", structures)
    assert "Неизвестная команда" in process_query("invalid", structures)
    assert "формат команды" in process_query("student", structures)
    print("Проверки коллекций и запросов: OK")


def main() -> None:
    structures = build_structures(SUBMISSIONS)
    print("=== Множество студентов ===")
    print(structures["students_set"])
    print("\n=== Множество лабораторных работ ===")
    print(structures["labs_set"])
    print("\n=== Попытки студентов ===")
    for student, attempts in structures["student_attempts"].items():
        print(f"{student}: {attempts}")
    print("\n=== Лучшие результаты ===")
    for key, score in structures["best_results"].items():
        print(f"{key}: {score}")
    print("\n=== Количество попыток ===")
    for key, count in structures["attempts_count"].items():
        print(f"{key}: {count}")

    print("\nСтуденты, сдававшие обе работы:", students_with_both_labs(structures["lab_students"]))

    new_submission = ("daria", "lab_02", 4)
    add_submission_to_structures(
        new_submission,
        structures["students_set"],
        structures["labs_set"],
        structures["student_attempts"],
        structures["best_results"],
        structures["attempts_count"],
        structures["lab_students"],
    )
    print(f"\nДобавлена запись: {new_submission}")
    print("После обновления обе работы сдавали:", students_with_both_labs(structures["lab_students"]))

    print("\n=== Текстовые запросы ===")
    for query in (
        "student anna",
        "best anna lab_01",
        "attempts boris lab_02",
        "completed lab_02",
        "student unknown",
        "best daria lab_02",
        "invalid_command",
        "student",
    ):
        print(f"{query!r} -> {process_query(query, structures)}")

    run_checks(build_structures(SUBMISSIONS))


if __name__ == "__main__":
    main()
