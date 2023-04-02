import random
import argparse
import datetime
import threading

import numpy as np
from _thread import interrupt_main
parser = argparse.ArgumentParser()

parser.add_argument(
    '--x_axis',
    help='Количество столбцов матрицы',
    required=False,
    default=120
)
parser.add_argument(
    '--y_axis',
    help='Количство строк матрицы',
    required=False,
    default=120
)
parser.add_argument(
    '--threads_count',
    help='Количество потоков для транспонирования матрицы',
    required=False,
    default=1
)

args = parser.parse_args()

X_AXIS = int(args.x_axis)
Y_AXIS = int(args.y_axis)

TREADS_COUNT = int(args.threads_count)


def transpose_matrix(sub_matrix: np.array, semaphore: None):
    # Транспонирование матрицы
    if semaphore:
        with semaphore:
            sub_matrix = sub_matrix.transpose()
    else:
        sub_matrix = sub_matrix.transpose()
    # interrupt_main()
    # print(
    #     f"Транспонированная часть матрицы: {sub_matrix}"
    # )


def generate_matrix(x_size: int = 120, y_size: int = 120) -> np.array:
    matrix = []
    
    for _ in range(y_size):
        matrix.append([
            random.randint(0, 100) for _ in range(x_size)
        ])
        
    return np.array(matrix)


def main():
    """
    Индивидуальное задание к ЛР-2
    Используя не менне 4-х потоков, решить следующую задачу:
    Транспонировать матрицу размером 120x120
    """
    matrix = generate_matrix(
        x_size=X_AXIS,
        y_size=Y_AXIS
    )
    
    print(f"Сгенерирована матрица {matrix.shape[0]} x {matrix.shape[1]} с числами от 0 до 99:")
    # print(matrix)
    
    
    start_time = datetime.datetime.now()
    # Разделение матрицы на TREADS_COUNT частей
    sub_matrixes = np.split(matrix, TREADS_COUNT)
    
    print(
        f"Разделенная матрица на {TREADS_COUNT} частей"
    )
    
    # Цикл вывода частей матрицы и запуска потоков для и обработки
    for index, sub_matrix in enumerate(sub_matrixes):
        print(
            f"Часть {index}: {sub_matrix}"
        )
        
        thread = threading.Thread(
            target=transpose_matrix,
            args=(sub_matrix,)
        )

        thread.start()

    end_time = datetime.datetime.now()
    work_time = (end_time-start_time).microseconds
    print(f"Время работы: {work_time}")
    
    with open(f"logs.txt", "a") as file:
        file.write(
            f"Матрица {matrix.shape[0]} x {matrix.shape[1]}, Потоки {TREADS_COUNT}, время работы: {work_time}\n"
        )
        
    
    
if __name__ == '__main__':
    main()


# python -m lab_2 --x_axis 120 --y_axis 120 --threads_count 1 && python -m lab_2 --x_axis 120 --y_axis 120 --threads_count 4 && python -m lab_2 --x_axis 120 --y_axis 120 --threads_count 6 && python -m lab_2 --x_axis 120 --y_axis 120 --threads_count 10 && python -m lab_2 --x_axis 120 --y_axis 120 --threads_count 12 && python -m lab_2 --x_axis 120 --y_axis 120 --threads_count 24