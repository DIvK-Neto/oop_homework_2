# from functools import total_ordering


# Подсчёт баллов
def get_score(arg: dict):
    total = float(0)
    if arg:
        for value in arg.values():
            total += sum(value)
        total = total/len(arg)
    return total


# Создаём класс сравнений
class Comparison():
    def __lt__(self, other):
        return get_score(self.grades) < get_score(other.grades)

    def __le__(self, other):
        return get_score(self.grades) <= get_score(other.grades)

    def __gt__(self, other):
        return get_score(self.grades) > get_score(other.grades)

    def __ge__(self, other):
        return get_score(self.grades) >= get_score(other.grades)

    def __eq__(self, other):
        return get_score(self.grades) == get_score(other.grades)

    def __ne__(self, other):
        return get_score(self.grades) != get_score(other.grades)


class Student(Comparison):
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.get_score = get_score

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and list(set(lecturer.courses_attached) & set(self.courses_in_progress)) and course in self.courses_in_progress:
            if lecturer.grades.get(course, None):
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            print('у преподователя нет оценок')

    def __str__(self):
        total = get_score(self.grades)
        return f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за домашние задания: {round(total, 1)} \nКурсы в процессе изучения:{", ".join(self.courses_in_progress)} \nЗавершенные курсы:{", ".join(self.finished_courses)}'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor, Comparison):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        total = get_score(self.grades)
        return f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {round(total, 1)}'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return print('Ошибка', student.name, course)


# Расчёт средней оценки
def average_rating(param: list, course: str):
    rating, count = 0, 0
    for el in param:
        if el.grades.get(course, None):
            rating += sum(el.grades[course])
            count += 1
    return rating/count if count != 0 else 'нет данных'


# Информация о студентах
some_student_1 = Student('Ruoy', 'Eman', 'm')
some_student_1.finished_courses = ['Основы Git']
some_student_1.courses_in_progress = ['Python', 'Java']
print(some_student_1)

some_student_2 = Student('Some', 'Bady', 'w')
some_student_2.finished_courses = ['Введение в программирование']
some_student_2.courses_in_progress = ['Python', 'Git']
print(some_student_2)


# Информация о лекторах
lecturer_1 = Lecturer('Vasy', 'Petrov')
lecturer_1.courses_attached = ['Python']
print(lecturer_1)

lecturer_2 = Lecturer('Vany', 'Ivanov')
lecturer_2.courses_attached = ['Git']
print(lecturer_2)


# Информация о проверяющих
reviewer_1 = Reviewer('Mega', 'Guru')
reviewer_1.courses_attached = ['Python']
print(reviewer_1)

reviewer_2 = Reviewer('Shara', 'Puh')
reviewer_2.courses_attached = ['Git']
print(reviewer_2)


# Проверка методов
some_student_1.rate_lecturer(lecturer_1, 'Git', 10)
some_student_1.rate_lecturer(lecturer_1, 'Python', 6)
some_student_2.rate_lecturer(lecturer_1, 'Python', 9)
some_student_2.rate_lecturer(lecturer_2, 'Git', 5)
print('Оценки 1-го преподавателя', lecturer_1.grades)

reviewer_1.rate_hw(some_student_1, 'Python', 5)
reviewer_1.rate_hw(some_student_1, 'Git', 7)
print(f'Оценки 1-го студента {some_student_1.grades}')

reviewer_2.rate_hw(some_student_2, 'Git', 8)
reviewer_1.rate_hw(some_student_2, 'Python', 7)
print(f'Оценки 2-го студента {some_student_2.grades}')


# сравнение студентов
print(get_score(some_student_1.grades), get_score(some_student_2.grades))
print(some_student_1 > some_student_2)
print(some_student_1 == some_student_2)
print(some_student_1 < some_student_2)


# Сравнение лекторов
print(get_score(lecturer_1.grades), get_score(lecturer_2.grades))
print(lecturer_1 > lecturer_2)
print(lecturer_1 == lecturer_2)
print(lecturer_1 < lecturer_2)


# Сравнение средней оценки
print(average_rating([some_student_1, some_student_2], 'Python'))
print(average_rating([some_student_1, some_student_2], 'Git'))
print(average_rating([some_student_1, some_student_2], 'Java'))
print()
print(average_rating([lecturer_1, lecturer_2], 'Python'))
print(average_rating([lecturer_1, lecturer_2], 'Git'))
print(average_rating([lecturer_1, lecturer_2], 'Java'))
