from lab_1_part_2 import generate_matrix, transpose_matrix
import argparse
import datetime
import numpy as np
import threading
from signal import SIGINT, signal
import sys



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

# Перехват сигнала
def handle_sigint(signalnum, frame):
    # terminate
    print('Сообщение перехвачено!')
    sys.exit()


def main():
    """
    Индивидуальное задание к ЛР-1-2-3
    Используя критическую секцию (lock), решить следующую задачу:
    Транспонировать матрицу размером 120x120
    Run command: python -m lab_3_1.lab_3_1_part_2
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
    signal(SIGINT, handle_sigint)
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


if __name__ == '__main__':
    main()
