import lib_search_sdk
from pathlib import Path

_me_parent = Path(__file__).absolute().parent


def test_init_db():
    #arrange
    expected_db = {}
    #act
    actual_db = lib_search_sdk.init_db()

    assert expected_db == actual_db


def test_add_to_db():
    #arrange
    empty_db = {}
    not_empty_db = {'m': {'a': {'y': {'a': {None: None}, None: None}, 'n': {None: None}}}}
    expected_empty_db = {'m':{'a':{'n':{None:None}}}}
    token = 'man'
    #act
    added_to_empty_db = lib_search_sdk.add_to_db(empty_db, token)
    added_to_not_empty_db = lib_search_sdk.add_to_db(not_empty_db, token)

    assert empty_db == expected_empty_db
    assert added_to_empty_db
    assert not added_to_not_empty_db


def test_iterable_tokens():
    #arrange
    token_path = f'{_me_parent}/tests/tokens.txt'
    expected_tokens = {'marsaba', 'maramba', 'man', 'may', 'bar', 'baron', 'banya', 'raba', 'rab'}
    #act
    tokens = lib_search_sdk.iterable_tokens(token_path)
    actual_tokens = {token for token in tokens}
    assert actual_tokens == expected_tokens


def test_find_prefix():
    #arrange
    expected_not_found = None
    expected_subtrie = {'b':{'a':{None:None}, None:None}}
    prefix = 'ra'
    prefix_not_in_mdb = 'ly'
    token_path = f'{_me_parent}/tests/tokens.txt'
    mdb = lib_search_sdk.load_db(token_path)
    #act
    actual_subtrie = lib_search_sdk.find_prefix(mdb, prefix)
    actual_not_found = lib_search_sdk.find_prefix(mdb, prefix_not_in_mdb)

    assert actual_subtrie == expected_subtrie
    assert actual_not_found == expected_not_found


def test_iterate_suffixes_short():
    #arrange
    expected_suffixes = {'b', 'ba'}
    mdb = {'b': {'a': {None: None}, None: None}}
    #act
    suffixes = lib_search_sdk.iterate_suffixes(mdb)
    actual_suffixes = {suffix for suffix in suffixes}

    assert actual_suffixes == expected_suffixes


def test_iterate_suffixes_mid():
    #arrange
    expected_suffixes = {'may', 'maya', 'man'}
    mdb = {'m': {'a': {'y': {'a': {None: None}, None: None}, 'n': {None: None}}}}
    #act
    suffixes = lib_search_sdk.iterate_suffixes(mdb)
    actual_suffixes = {suffix for suffix in suffixes}

    assert actual_suffixes == expected_suffixes


def test_retrive_suffixes_by_prefix():
    #arrange
    token_path = f'{_me_parent}/tests/tokens.txt'
    mdb = lib_search_sdk.load_db(token_path)
    prefix = 'ra'
    prefix_not_in_mdb = 'ly'
    expected_suffixes_unlim = {'b', 'ba'}
    expected_suffixes_lim = {'b'}
    limit = 1
    #act
    actual_suffixes_unlim = set(lib_search_sdk.retrive_suffixes_by_prefix(mdb, prefix))
    actual_suffixes_lim = set(lib_search_sdk.retrive_suffixes_by_prefix(mdb, prefix, limit))
    actual_suffixes_not_found = lib_search_sdk.retrive_suffixes_by_prefix(mdb,prefix_not_in_mdb)

    assert actual_suffixes_lim == expected_suffixes_lim
    assert actual_suffixes_unlim == expected_suffixes_unlim
    assert not actual_suffixes_not_found



def test_load_db():
    #arrange
    expected_db = {'m':{'a': {'r': {'s': {'a': {'b': {'a': {None: None}}}}, 'a': {'m': {'b': {'a': {None: None}}}}},
                    'n': {None: None}, 'y': {None: None}}}, 'b': {'a': {'r': {None: None, 'o': {'n': {None: None}}},
                    'n': {'y': {'a': {None: None}}}}}, 'r': {'a': {'b': {'a': {None: None}, None: None}}}}
    token_path = f'{_me_parent}/tests/tokens.txt'
    #act
    actual_db = lib_search_sdk.load_db(token_path)

    assert actual_db == expected_db


def test_get_suggestions():
    #arrange
    token_path = f'{_me_parent}/tests/tokens.txt'
    mdb = lib_search_sdk.load_db(token_path)
    prefix = 'ma'
    prefix_not_found = 'ly'
    limit = 2
    expected_suggestions_unlim = {'marsaba', 'maramba', 'man', 'may'}
    expected_suggestions_not_found = []
    #act
    actual_suggestions_unlim = set(lib_search_sdk.get_suggestions(mdb, prefix))
    actual_suggestions_lim = lib_search_sdk.get_suggestions(mdb, prefix, limit)
    actual_suggestions_not_found = lib_search_sdk.get_suggestions(mdb, prefix_not_found)

    assert actual_suggestions_unlim == expected_suggestions_unlim
    assert len(actual_suggestions_lim) == 2
    assert actual_suggestions_lim[0] in expected_suggestions_unlim
    assert actual_suggestions_lim[1] in expected_suggestions_unlim
    assert actual_suggestions_not_found == expected_suggestions_not_found


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
