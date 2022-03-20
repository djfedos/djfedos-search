"""
This is the set of custom tests that reproduce conditions for the bugs that were found manually.
If any of those tests breaks it means that something goes wrong
"""

import lib_search_sdk
from pathlib import Path

_me_parent = Path(__file__).absolute().parent

def test_iterate_suffixes_manually_found_bug():
    #arrange
    token_path = f'{_me_parent}/tests/1200_tokens.txt'
    mdb = lib_search_sdk.load_db(token_path)
    prefix = 'mi'
    expected_suffixes = {'litary','ddle','ce','sty','st','screant','nd','nor','nt','ne'}
    #act
    isuffixes = lib_search_sdk.retrive_suffixes_by_prefix(mdb, prefix)
    if isuffixes:
        actual_suffixes = {suf for suf in isuffixes}
    else:
        actual_suffixes = None

    assert actual_suffixes == expected_suffixes
    # lines 63 to 72 of the lib_search_sdk.py fix this issue


def test_add_to_db_manually_found_bug():
    #arrange
    mdb = {}
    token_path = f'{_me_parent}/tests/2466_tokens.txt'
    itokens = lib_search_sdk.iterable_tokens(path=token_path)
    #act
    for itoken in itokens:
        assert lib_search_sdk.add_to_db(mdb=mdb, token=itoken)
    # add_to_db() function fixed


def test_get_suggestions_manually_found_bug():
    #arrange
    full_tokens = ['tested', 'friendly', 'planes', 'windy', 'seat', 'secretary', 'highfalutin', 'skirt', 'handsome', 'flowery', 'scared',
    'cows', 'damaged', 'fearful', 'handy', 'nutritious', 'skin', 'rightful', 'needle', 'town', 'tired', 'caption', 'tickle',
    'earthquake', 'bite', 'earth', 'rainy', 'start', 'capricious', 'early', 'paste', 'skip', 'handsomely', 'hands', 'bite-sized',
    'needless', 'plane', 'damage', 'damaging', 'skinny', 'earthy']
    token_path = f'{_me_parent}/tests/2466_tokens.txt'
    mdb = lib_search_sdk.load_db(token_path)
    #act
    for full_token in full_tokens:
        assert lib_search_sdk.get_suggestions(mdb, full_token)[0].startswith(full_token)
    # add condition "if branch_children" to the line 64 of the lib_search_sdk.py to fix an issue
