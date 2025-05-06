
import threading
def count_words(filename):
    """
    Считает количество слов в файле и выводит результат.
    """
    try:
        with open(filename, "r") as file:
            text = file.read()
        word_count = len(text.split())
        print(f"{filename}: {word_count} слов")
    except FileNotFoundError:
        print(f"{filename}: файл не найден")

def test_old():
    print("\ntest_old():")
    # Создаем два потока для работы с разными файлами
    thread1 = threading.Thread(target=count_words, args=("file1.txt",))
    thread2 = threading.Thread(target=count_words, args=("file2.txt",))
    # Запускаем потоки
    thread1.start()
    thread2.start()
    # Ожидаем завершения
    thread1.join()
    thread2.join()
    print("Обработка файлов завершена.")

###############
from concurrent.futures import ThreadPoolExecutor

def process_file(file_name):
    print(f"Processing file: {file_name}")
    count_words(file_name)

def test_pool():
    print("\ntest_pool():")
    # Создаем пул из 3 threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]
        executor.map(process_file, files)

##############

class ThreadSafeCounter:
  def __init__(self):
    self.val__ = 0
    self.lock__ = threading.Lock()

  def change(self):
    with self.lock__:
      self.val__ += 1

  def getCounter(self):
    return self.val__


def work(counter, operationsCount):
    for _ in range(operationsCount):
        counter.change()


def run_threads(counter, threadsCount, operationsPerThreadCount):
    threads = []

    for _ in range(threadsCount):
        t = threading.Thread(target=work, args=(counter, operationsPerThreadCount))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def test_lock():
    print("\ntest_lock():")
    threadsCount = 10
    operationsPerThreadCount = 1_000_000
    expectedCounterValue = threadsCount * operationsPerThreadCount
    counters = [ThreadSafeCounter()]

    for counter in counters:
      run_threads(counter, threadsCount, operationsPerThreadCount)
      print(f"{counter.__class__.__name__} : expected val: {expectedCounterValue:,d}, actual val: {counter.getCounter():,d}")

import asyncio
import time
import aiohttp

async def завантажити_сторінку_асинхронно(url):
    print(f"Початок завантаження: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Завантажено: {url}, статус: {response.status}, розмір: {len(await response.read())}")

async def async_test():
    urls = [
        "https://www.google.com",
        "https://www.facebook.com",
        "https://www.youtube.com",
        "https://www.python.org"
    ]
    tasks = [завантажити_сторінку_асинхронно(url) for url in urls]
    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Загальний час виконання: {end_time - start_time:.2f} секунд")

import multiprocessing
import time

def обчислити_суму_квадратів(числа):
    сума = sum(x**2 for x in числа)
    ідентифікатор_процесу = multiprocessing.current_process().name
    print(f"Процес {ідентифікатор_процесу}: Сума квадратів для {числа[:5]}... дорівнює {сума}")
    return сума

def multiproc_test():
    числа = [i for i in range(1, 100001)]
    розмір_частини = 25000
    частини_чисел = [числа[i:i + розмір_частини] for i in range(0, len(числа), розмір_частини)]

    процеси = []
    start_time = time.time()

    for i, частина in enumerate(частини_чисел):
        процес = multiprocessing.Process(target=обчислити_суму_квадратів, args=(частина,), name=f"Процес-{i+1}")
        процеси.append(процес)
        процес.start()

    результати = []
    for процес in процеси:
        процес.join()

    end_time = time.time()
    print(f"Загальний час виконання: {end_time - start_time:.2f} секунд")

if __name__ == "__main__" :
    #test_old()
    #test_pool()
    #test_lock()
    #asyncio.run(async_test())
    multiproc_test()