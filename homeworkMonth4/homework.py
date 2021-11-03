from random import randint
import datetime
import time

name = input("Введите свое имя:")
attempts = int(input("Введите количество попыток:"))
copyattempts = attempts
start = datetime.datetime.now()
rnd = 0
while True:
    a = randint(1, 9)
    b = randint(1, 9)
    answer = a * b
    print(f"Сколько будет {a} x {b} = ?", end=' ')
    result = int(input())
    print(answer)
    attempts -= 1

    with open('results.txt', 'a') as file:
        if result == answer:
            file.write(f"{a} x {b} = {result} ({answer}) правильно\n")
        elif result != answer:
            file.write(f"{a} x {b} = {result} ({answer}) неправильно\n")

    if attempts == 0:
        end = datetime.datetime.now()
        end - start
        with open('results.txt', 'a') as file:
            file.write(
                f"Потрачено попытки: {copyattempts}, Потраченное время: {end-start} секунд, Имя: {name}\n")
        print("Количество попыток закончилось")
        print(f"Потраченное время: {end - start} секунд")
        break