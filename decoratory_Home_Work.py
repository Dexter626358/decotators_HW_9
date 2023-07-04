"""
Напишите следующие функции:
○Нахождение корней квадратного уравнения
○Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк.
○Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
○Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.
"""
import random
import csv
import os
import json
from typing import Callable


def roots_csv(func):
    def wrapper(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                a, b, c = map(int, row)
                result = func(a, b, c)
                #print(f"Корни уравнения {a}x^2 {b}x {c}: {result}")

    return wrapper


def save_to_json(file_path):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            a, b, c = args
            data = {
                "Параметры": f"{a}, {b}, {c}",
                "Результат": result
            }
            if os.path.exists(file_path):
                with open(file_path, 'a', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            return result

        return wrapper

    return decorator


@roots_csv
@save_to_json("root_json.json")
def square_equalities(a, b, c):
    disriminant = b ** 2 - 4 * a * c
    if disriminant > 0:
        x1 = round((-b + disriminant ** 0.5) / (2 * a), 2)
        x2 = round((-b - disriminant ** 0.5) / (2 * a), 2)
        return x1, x2
    elif disriminant == 0:
        x1 = round(-b / (2 * a), 2)
        return x1
    else:
        return f"Квадратное уравнение не имеет корней в области действительных чисел"


def gen_csv():
    with open("randNumbers.csv", 'w', encoding='utf-8') as file:
        for i in range(0, 500):
            num1 = random.randint(-100, 100)
            if num1 == 0:
                num1 += 1
            num2 = random.randint(-100, 100)
            if num2 == 0:
                num2 += 1
            num3 = random.randint(-100, 100)
            if num3 == 0:
                num3 += 1

            file.write(f"{num1},{num2},{num3}" + "\n")


gen_csv()
square_equalities("randNumbers.csv")
