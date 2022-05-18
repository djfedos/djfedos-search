# This app creates a web interface for lib-search_sdk
# The app is refactored from the basic tutorial to avoid from pywebio import * construction

import pywebio as pwb
from lib_search_sdk import load_db, get_suggestions, add_to_db


def main():
    my_db = load_db('tests/2466_tokens.txt')
    pwb.output.put_text('This is a web app for djfedos-search trie searching engine')
    pwb.output.put_text('It looks up words in database by prefix')
    while True:
        prefix_lim = pwb.input.input_group('Input prefix and set limit:',
            [pwb.input.input('Enter any prefix you like to try it out, use lowercase latin letters', name='prefix', placeholder='prefix'),
            pwb.input.input('Set maximum suggestion count. For 10 leave blank. Set to zero or a negative number to remove the limit', name='limit', type=pwb.input.NUMBER)])

        prefix = prefix_lim['prefix']

        if prefix_lim['limit'] == 0:
            suggs = get_suggestions(my_db, prefix, limit=None)
        elif prefix_lim['limit']:
            suggs = get_suggestions(my_db, prefix, limit=prefix_lim['limit'])
        else:
            suggs = get_suggestions(my_db, prefix)

        pwb.input.select(label='suggestions', options=suggs)

if __name__ == '__main__':
    main()