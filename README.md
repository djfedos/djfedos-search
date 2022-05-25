# djfedos-search

## What is it?
djfedos-search is a python library that implements a quick search of a token by its prefix.

## How does it work?

First it takes a list of words as an input. It turns this list into a trie aka a prefix tree.
Then it takes a prefix (any given string of characters) as an input and returns the words
(aka tokens) from the trie that start with this prefix.

## What is it for?

First of all, it can be used as an engine behind the user input suggestion, like in searching
engines.

## How to try it out quickly?

Here is a live web UI of the demo: http://yairdar.info:8000 
You also can run it< and that's how:
1. There is a FastAPI-based web API in `fapi_server.py`. While running it will reply to queries.
2. Run it, load a list of tokens and you can open `js_web_ui/index.html` in a browser and try out
a demo suggestion web app.
Also to try out the library with a decent example base of tokens in a convenient web interface
you can launch `neat_pywebio_app.py`.

## How to use it?

The library itself is if `lib_search_sdk.py` file. In order to use it import it as a module.

The external API of `lib_search_sdk` has two main methods:

### 1. load_db(path:str=None)

To load a list of words, pass a path to the .txt file containing one word per line. This function
returns a dict, that is a database to search through.

Example:

`test_token_db = load_db('tests/1200_tokens.txt')`

### 2. get_suggestions(mdb:dict, prefix:str, limit:int=10)

To get suggestions, pass a token db returned by `load_db()` as a first argument,  a prefix as a
second argument and optionally the limit, which is the maximum amount of suggestions you want to
get from this function. By default the limit is set to 10. If you want to get all the suggestions,
pass `None` as a limit.

Examples:

`suggestions = get_suggestions(test_token_db, 'flo')`

`suggestions = get_suggestions(test_token_db, 'ma', None)`

`suggestions = get_suggestions(test_token_db, 'do', 3)`

There is also an additional method:

### 3. add_to_db(mdb:dict, token:str)

To add a token to the existing db, pass the db as a first argument and a token as a second.

Example:

`add_to_db(test_token_db, 'acidity')`

if this token is already in the db, this function will return `False`, else it will add a token
and return `True`.

## Tests
This library comes with two sets of tests.
1. `test_lib_search_sdk.py` contains unit tests. This is the main set of tests.
It ensures that the crucial functions work as expected.
2. `test_lib_search_sdk_custom_set.py` contains additional tests for bugs that
were discovered manually.

Lists of tokens for tests are in the `tests` folder.

There is also a file called `test_lib_search_sdk_manual.py` that allows a pretty convenient
manual testing.

## Benchmarks
To benchmark the performance of the library in different scenarios, use `test_benchmarks.py`
with `pytest` module. There are several functions for benchmarking that support semi-automated
workflow.

## Authors
This library is written by Fedor Ivashchenko
