import numpy as np
import sympy
import argparse
import random
import threading
import datetime


parser = argparse.ArgumentParser()

parser.add_argument(
    '--n',
    help='Размер массива',
    required=False,
    default=100000
)
parser.add_argument(
    '--use_threads',
    help='Использовать мультипоточность',
    required=False,
    default=False
)

args = parser.parse_args()

USE_THREADS = True if args.use_threads in ('true', 'True') else False

ARRAY_LENGTH = int(args.n)
ARRAY = np.array(
    [random.randint(0, 100) for _ in range(ARRAY_LENGTH)]
)


def search_primes(array: np.array) -> None:
    primes = list(filter(sympy.isprime, array))
    # print(f"Простые числа из массива: {primes}")


def main():
    start_time = datetime.datetime.now()
    print(type(USE_THREADS))
    first_part= ARRAY[:int(ARRAY_LENGTH ** 0.5)]
    second_part = ARRAY[int(ARRAY_LENGTH ** 0.5):]
    
    for array_part in [first_part, second_part]:
        thread = threading.Thread(
            target=search_primes,
            args=(array_part,)
        )
        thread.start()
        if not USE_THREADS:
            thread.join()
            
    end_time = datetime.datetime.now()
    work_time = (end_time - start_time).microseconds
    
    with open('logs/lab_2_part_1.log', 'a') as log_file:
        log_file.write(
            f"Массив случайных чисел (от 0 до 100) длиной {len(ARRAY)}"
            f" {'с использованием мультипоточности' if USE_THREADS else 'без использования мультипоточности'}."
            f" Время работы: {work_time}\n"
        )
        

if __name__ == '__main__':
    main()
