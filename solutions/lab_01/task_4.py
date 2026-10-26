student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10
print(student[0], student[3])
print(student[0:4])
print(student[5:len(student)])
print(student.upper(), student.lower())
print(f'{student[0]}.{student[5]}.')
print(course[::-1])
print(f'{student} - {course}: {completed}/{total} ({total/100*completed*100}%)')
print('%s - %s: %d/%d (%s)' % (student, course, completed, total, str(total/100*completed*100)+'%'))
print('{} - {}: {}/{} ({}%)'.format(student, course, completed, total, str(total/100*completed*100)))



symbol = "Я"
print(symbol, ord(symbol), chr(ord(symbol)), chr(ord(symbol)), symbol.encode("utf-8"))
print(len(symbol), len(symbol.encode("utf-8")))

"""symbol[0] = 'a'
print(symbol)"""





