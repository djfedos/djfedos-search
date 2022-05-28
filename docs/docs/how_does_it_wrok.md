---
hide:
  - toc
---

First it takes a list of words as an input. It turns this list into a trie aka a prefix tree.
Then it takes a prefix (any given string of characters) as an input and returns the words
(aka tokens) from the trie that start with this prefix.

### More details
The library itself is in [`lib_search_sdk.py`](https://github.com/djfedos/djfedos-search/blob/main/lib_search_sdk.py)
file. It's self-contained, it doesn't need any 
other files from the repository in order to work. It also doesn't import any python modules.
All the additional files are there for testing, benchmarking, documentation and demonstration
purposes.

The input format for words (aka tokens) is a text file, one word per line.

The input format for prefix is string. Given an empty string as a prefix the library will
output all the words stored in its prefix tree, though only if `limit` is set to `None`.

`limit` is an optional parameter, by default it's set to 10. It defines the maximum amount
of words that the library will return for a given prefix. Limit can be an integer number or
`None`. When limit is set to `None`, the library outputs all the words that start with a
given prefix.

For even more details you're always welcome [to read the source code](https://github.com/djfedos/djfedos-search)
and ask me any questions.
