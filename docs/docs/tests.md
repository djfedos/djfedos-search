---
hide:
  - toc
---

This library comes with two sets of tests. Use pytest to run them.

1. `test_lib_search_sdk.py` contains unit tests. This is the main set of tests.
It ensures that the crucial functions work as expected.
2. `test_lib_search_sdk_custom_set.py` contains additional tests for bugs that
were discovered manually.

Lists of tokens for tests are in the `tests` folder.

There is also a test for FastAPI server in `test_fapi_server.py`.

Those three tests run automatically on every commit push to the
[GitHub repository](https://github.com/djfedos/djfedos-search).

There is an additional tool called `test_lib_search_sdk_manual.py` that allows convenient
manual testing.
