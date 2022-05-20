# This app creates a web interface for lib-search_sdk
# The app is refactored from the basic tutorial to avoid from pywebio import * construction

import pywebio as pwb
from lib_search_sdk import load_db, get_suggestions, add_to_db


def main():
    while True:
        pwb.output.put_text('This is a web app for djfedos-search trie searching engine')
        pwb.output.put_text('It looks up words in database by prefix')

        prefix = pwb.input.input('Enter any prefix you like to try it out, use lowercase latin letters', placeholder='prefix')
        limit = pwb.input.input('By default the engine outputs 10 words or less. If you want to change this limit, enter a new limit to this field', type=pwb.input.NUMBER)
        print(prefix)

        my_db = load_db('tests/2466_tokens.txt')

        if limit:
            lim = limit
        else:
            lim = 10

        suggs = get_suggestions(my_db, prefix, lim)
        tbl = [['tokens']] + [[it] for it in suggs]
        pwb.output.put_table(tbl)
        print(suggs)


if __name__ == '__main__':
    main()