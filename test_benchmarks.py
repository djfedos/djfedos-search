from random import randint
from uuid import uuid4
import lib_search_sdk
import time
import csv
from pathlib import Path
from matplotlib import pyplot as plt
from pandas import read_csv


class TokensFileCreator:

    def __init__(self, workdir:str):
        self.workdir = workdir

    def create_token_file(self, num_lines:int=100, max_length:int=10):
        token_file_uuid = uuid4()
        path = self.workdir
        path += f'/tokens_{token_file_uuid}.txt'
        with open(path, 'a') as token_file:
            for _ in range(num_lines):
                line = ''.join([chr(randint(97, 97 + 26 - 1)) for _ in range(max_length)])
                token_file.write(line)
                token_file.write('\n')
        return path

    def create_one_char_token_file(self, num_lines:int=100):
        token_file_uuid = uuid4()
        path = self.workdir
        path += f'/tokens_{token_file_uuid}.txt'
        line = ''
        with open(path, 'a') as token_file:
            for _ in range(num_lines):
                line += 'a'
                token_file.write(line)
                token_file.write('\n')
        return path


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:

    def __init__(self, logger=None, text="Elapsed time: {:0.4f} seconds"):
        self._start_time = None
        self.logger = logger
        self.text = text

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running, use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))

        return elapsed_time


def test_benchmark_load_db(tmpdir, num_lines=100, max_length=10, cycles=1000, result_path='benchmark_results.csv'):
    tfk = TokensFileCreator(tmpdir)
    bench_file = tfk.create_token_file(num_lines, max_length)
    timer = Timer()
    total_time = 0
    min_time = float('inf')
    max_time = 0
    for _ in range(cycles):
        timer.start()
        bench_db = lib_search_sdk.load_db(bench_file)
        cycle_time = timer.stop()
        total_time += cycle_time
        if cycle_time < min_time:
            min_time = cycle_time
        if cycle_time > max_time:
            max_time = cycle_time
        bench_db = None
    average_time = total_time/cycles

    header = ['num_of_runs', 'num_lines', 'max_length', 'average_sec', 'max_secs', 'min_secs']
    benchmark_results = [cycles, num_lines, max_length, '{:4f}'.format(average_time), '{:6f}'.format(max_time), '{:6f}'.format(min_time)]

    if not Path(result_path).exists():
        header_needed = True
    else:
        header_needed = False

    with open(result_path, 'a', newline='') as benchmark_results_file:
        writer = csv.writer(benchmark_results_file)
        if header_needed:
            writer.writerow(header)
        writer.writerow(benchmark_results)


def test_benchmark_get_suggestions_limits(tmpdir, num_lines=100, max_length=10,  prefix_length=0, limit=100, cycles=1000, result_path='get_suggestions_benchmark_limit.csv'):
    tfk = TokensFileCreator(tmpdir)
    bench_file = tfk.create_token_file(num_lines, max_length)
    bench_db = lib_search_sdk.load_db(bench_file)
    timer = Timer()
    total_time = 0
    min_time = float('inf')
    max_time = 0
    for _ in range(cycles):
        prefix = ''.join([chr(randint(97, 97 + 26 - 1)) for _ in range(prefix_length)])
        timer.start()
        suggestions = lib_search_sdk.get_suggestions(bench_db, prefix, limit)
        cycle_time = timer.stop()
        total_time += cycle_time
        if cycle_time < min_time:
            min_time = cycle_time
        if cycle_time > max_time:
            max_time = cycle_time
        print(suggestions)
        suggestions = None

    average_time = total_time / cycles

    header = ['num_of_runs', 'prefix_length', 'limit', 'average_sec', 'max_secs', 'min_secs']
    benchmark_results = [cycles, prefix_length, limit, '{:4f}'.format(average_time), '{:6f}'.format(max_time), '{:6f}'.format(min_time)]

    if not Path(result_path).exists():
        header_needed = True
    else:
        header_needed = False

    with open(result_path, 'a', newline='') as benchmark_results_file:
        writer = csv.writer(benchmark_results_file)
        if header_needed:
            writer.writerow(header)
        writer.writerow(benchmark_results)


def test_benchmark_get_suggestions_prefix(tmpdir, num_lines=100, prefix_length=50, limit=100, cycles=1000, result_path='get_suggestions_benchmark_prefix.csv'):
    tfk = TokensFileCreator(tmpdir)
    bench_file = tfk.create_one_char_token_file(num_lines)
    bench_db = lib_search_sdk.load_db(bench_file)
    timer = Timer()
    total_time = 0
    min_time = float('inf')
    max_time = 0
    for _ in range(cycles):
        prefix = ''.join(['a' for _ in range(prefix_length)])
        timer.start()
        suggestions = lib_search_sdk.get_suggestions(bench_db, prefix, limit)
        cycle_time = timer.stop()
        total_time += cycle_time
        if cycle_time < min_time:
            min_time = cycle_time
        if cycle_time > max_time:
            max_time = cycle_time
        suggestions = None

    average_time = total_time / cycles

    header = ['num_of_runs', 'prefix_length', 'limit', 'average_sec', 'max_secs', 'min_secs']
    benchmark_results = [cycles, prefix_length, limit, '{:4f}'.format(average_time), '{:6f}'.format(max_time), '{:6f}'.format(min_time)]

    if not Path(result_path).exists():
        header_needed = True
    else:
        header_needed = False

    with open(result_path, 'a', newline='') as benchmark_results_file:
        writer = csv.writer(benchmark_results_file)
        if header_needed:
            writer.writerow(header)
        writer.writerow(benchmark_results)


def test_plot_benchmarks(result_path='get_suggestions_benchmark_prefix.csv', columns = ['prefix_length', 'average_sec']):
    if not Path(result_path).exists():
        raise FileExistsError("File does not exist, please check the file name")
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    df = read_csv(result_path, usecols=columns)
    print()
    print("Contents in csv file:\n", df)
    plt.plot(df.iloc[:,0], df.iloc[:,1])
    plt.show()


"""
Two following helpers do not work with tmpdir fixture
"""
# def test_benchmark_hepler_num_lines(parameter_min=10, parameter_max=300, parameter_step=10):
#     for parameter in range(parameter_min, parameter_max + parameter_step, parameter_step):
#         test_create_file(tmpdir, num_lines=parameter, max_length=10, cycles=1000, result_path=f'benchmark_results_num_lines.csv')
#         test_plot_benchmarks(result_path='benchmark_results_num_lines.csv', columns=['num_lines', 'average_sec'])
#
#
# def test_benchmark_hepler_max_length(parameter_min=5, parameter_max=40, parameter_step=5):
#     for parameter in range(parameter_min, parameter_max + parameter_step, parameter_step):
#         test_create_file(num_lines=100, max_length=parameter, cycles=1000, result_path=f'benchmark_results_max_length.csv')
#         test_plot_benchmarks(result_path='benchmark_results_max_length.csv', columns=['max_length', 'average_sec'])









