---
hide:
  - toc
---

To benchmark performance of the library in different scenarios, use test_benchmarks.py with pytest module. There are several functions for benchmarking that support semi-automated workflow.

## test_benchmark_load_db()
measures the performance of loading tokens to the database from the text file. It has the following parameters:

* `num_lines:int`: number of lines (tokens) in a text file that's generated on every benchmark cycle.
* `max_length:int`: length of a single token in characters. all the generated tokens have the same length, that is also a maximum length, in order to reproduce the worst case scenario.
* `cycles:int`: number of benchmark cycles to average out any fluctuations of its results.
* `result_path:str`: path to the file with benchmark results. It's recommended to save results in .csv file.


## test_benchmark_get_suggestions_limits()
measures the performance of getting tokens from the database with a given limit on maximum amount of output tokens. The prefix is set to an empty string to maximize possible token output. It has the following parameters:

* `limit:int`: the main parameter of the test, it sets a maximum amount of tokens that the engine will output.
* `num_lines:int`: number of lines (tokens) in a text file that's generated on every benchmark cycle.
* `max_length:int`: length of a single token in characters. all the generated tokens have the same length, that is also a maximum length, in order to reproduce the worst case scenario.
* `cycles:int`: number of benchmark cycles to average out any fluctuations of its results.
* `result_path:str`: path to the file with benchmark results. It's recommended to save results in .csv file.
* `prefix_length=0` in this case is used only to output the results into a .csv file. The prefix length in this test is hardcoded to be zero anyway, so it's recommended not to edit this parameter and leave it as it is.

## test_benchmark_get_suggestions_prefix()
this benchmark emulates a pretty unrealistic worst case scenario. It generates a token base with strings of a single character 'a'. Then it measures the time that it takes to fetch all the suitable tokens with prefixes consisting of the same character 'a'. It cycles through prefix length values from zero to (prefix_length - 1).

* `prefix_length:int`: maximum prefix length.
* `num_lines:int`: number of lines (tokens) in a text file that's generated on every benchmark cycle.
* `limit:int`: maximum amount of tokens that the engine will output.
* `cycles:int`: number of benchmark cycles to average out any fluctuations of its results.
* `result_path:str`: path to the file with benchmark results. It's recommended to save results in .csv file.


## test_plot_benchmarks()
This method allows plotting benchmark results as a graph from the .csv file. It's useful when you make several benchmark runs with different parameters.

* result_path:str: path to the .csv file with benchmark results
* columns:List(str): columns with data to plot in ['x','y'] form, where 'x' is the name of horizontal axis data and 'y' is the name of vertical axis data.