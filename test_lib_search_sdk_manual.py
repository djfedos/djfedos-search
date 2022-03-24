import lib_search_sdk
from pathlib import Path

_me_parent = Path(__file__).absolute().parent

def _get_suggestions(prefix, limit=None):
    #arrange
    token_path = f'{_me_parent}/tests/1200_tokens.txt'
    mdb = lib_search_sdk.load_db(token_path)
    #act
    suggestions = lib_search_sdk.get_suggestions(mdb, prefix, limit)
    return suggestions

if __name__== '__main__':
    import fire
    fire.Fire(_get_suggestions)

# print(_get_suggestions('aci'))