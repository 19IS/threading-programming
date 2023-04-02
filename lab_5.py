from lab_1_part_2 import generate_matrix, transpose_matrix

import multiprocessing as mp

import argparse
import datetime
import numpy as np
import threading


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
    default=4
)

args = parser.parse_args()

X_AXIS = int(args.x_axis)
Y_AXIS = int(args.y_axis)

TREADS_COUNT = int(args.threads_count)

def main():
    """
    Индивидуальное задание к ЛР-1-2-3
    Используя критическую секцию (lock), решить следующую задачу:
    Транспонировать матрицу размером 120x120
    Run command: python -m lab_3_1.lab_3_1_part_1
    """
    matrix = generate_matrix(
        x_size=X_AXIS,
        y_size=Y_AXIS
    )

    print(
        f"Сгенерирована матрица {matrix.shape[0]} x {matrix.shape[1]} с числами от 0 до 99:")
    # print(matrix)

    start_time = datetime.datetime.now()
    # Разделение матрицы на TREADS_COUNT частей
    sub_matrixes = np.split(matrix, TREADS_COUNT)

    print(
        f"Разделенная матрица на {TREADS_COUNT} частей"
    )
    pool = mp.Pool(TREADS_COUNT)
    # Цикл вывода частей матрицы и запуска потоков для и обработки
    for index, sub_matrix in enumerate(pool.imap_unordered(transpose_matrix, sub_matrixes, chunksize=1)):
        print(f"Выполняется транспонирование матрицы ({index})")
        print(sub_matrix)
        if index == 2:
            print('Прекращение')
            pool.terminate()
            break

    end_time = datetime.datetime.now()
    work_time = (end_time-start_time).microseconds
    print(f"Время работы: {work_time}")


if __name__ == '__main__':
    main()
