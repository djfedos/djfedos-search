## How to use the library in my project?

The library itself is in the `lib_search_sdk.py` file. In order to use it, import it:

`import lib_search_sdk`

The external API of `lib_search_sdk` has two main methods:

### 1. load_db(path:str=None)

To load a list of words, pass a path to the .txt file containing one word per line. This function
returns a dict, that is the database to search through.

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

**There is also an additional method:**

### 3. add_to_db(mdb:dict, token:str)

To add a token to the existing db, pass the db as a first argument and a token as a second.

Example:

`add_to_db(test_token_db, 'acidity')`

if this token is already in the db, this function will return `False`, else it will add a token
and return `True`.