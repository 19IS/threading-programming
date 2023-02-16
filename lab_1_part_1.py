import argparse
import datetime
import threading

import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument(
    '--N',
    help='Количество элементов массива',
    required=False,
    default=1000
)
parser.add_argument(
    '--M',
    help='Число потоков для обработки элементов массива',
    required=False,
    default=2
)

args = parser.parse_args()

N = int(args.N)
M = int(args.M)


a = np.array([number+1 for number in range(N)])
b = np.array([np.NaN for _ in range(len(a))])


def run(array: np.array):
    for i in range(len(array)):
        b[i] = a[i] ** 1.789


def main():
    print(f"Запуск функции обработки массива длиной {len(a)} с помощью {M} потоков ...")
    start_time = datetime.datetime.now()
    # Разделяем массив на несколько частей M
    arrays = np.split(a, M)
    print(f"Исходный массив разделен на {len(arrays)} частей")

    for index, array in enumerate(arrays):
        print(f"Обработка {index+1} части массива")
        thread = threading.Thread(
            target=run,
            args=(array,)
        )

        thread.start()

    end_time = datetime.datetime.now()

    work_time = (end_time - start_time).microseconds

    print(f"Время работы программы: {work_time}. \n")


if __name__ == '__main__':
    main()
