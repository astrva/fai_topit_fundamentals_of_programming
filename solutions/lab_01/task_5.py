user_name = input("Имя исследователя: ")
project_name = input("Название эксперимента: ")
runs_cnt = int(input("Количество выполненных запусков: "))
run_time = float(input("Длительность одного запуска: "))
re_part = float(input("Действительная часть комплексного коэффициента: "))
im_part = float(input("Мнимая часть комплексного коэффициента: "))


all_runs_time = runs_cnt * run_time
all_runs_time_mins = all_runs_time/60
cmplx = complex(re_part, im_part)
qu_abs = re_part ** 2 + im_part ** 2
has_runs = bool(runs_cnt)


print(f"ЭКПЕРИМЕНТ: {project_name}")
print(f'Исследователь: {user_name}')
print(f'Запуски: {runs_cnt}')
print(f'Общее время: {all_runs_time:.2f} c ({all_runs_time_mins:.2f} мин)')
print(f'Коэффициент: {cmplx}')
print(f'Квадрат модуля: {qu_abs:.2f}')
print(f'Есть выполненные запуски: {has_runs}')


