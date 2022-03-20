# internal methods:

def init_db():
    return {}


def add_to_db(mdb:dict, token:str):
    token_added = False
    cur = mdb
    for char in token:
        if char not in cur:
            cur[char] = {}
        cur = cur[char]
    if not None in cur:
        cur[None] = None
        token_added = True
    return token_added

"""
O(n) where n is a token length
"""

# return bool
# if this token is already in the db, it doesn't get added and add_to_db() returns False
# if token is added, add_to_db() returns True

def iterable_tokens(path:str):
    with open(path, 'r') as f_tokens:
        db_tokens = []
        for line in f_tokens:
            if line.endswith('\n'):
                token = line[0:-1]
            else:
                token = line
            yield token
        return db_tokens

# return iterable[str]

"""
O(n) where n is a number of tokens
"""


def find_prefix(mdb:dict, prefix:str):
    cur = mdb
    for char in prefix:
        if char in cur:
            cur = cur[char]
        else:
            return None
    return cur

"""
O(n) where n is a number of characters in a prefix
"""
    
# return dict
# start from root mdb and returns root for end of prefix


# iterative implementation of trie traversal with a branch buffer
def iterate_suffixes(mdb:dict):
    suffixes = []
    branch_buffer = {}

    suffix = ''
    cur = mdb
    
    while cur:
        if cur == {None: None}:                                     # when we reach the word end
            yield suffix                                            # we yield the suffix
            if branch_buffer:                                       # if branch buffer is not empty
                suffix, branch_children = branch_buffer.popitem()   # we extract the last added suffix and its children from the buffer

                while branch_children and not branch_children[-1]:  # in some situations this check is required even more than once
                    yield suffix
                    branch_children.pop()
                    if branch_buffer:                               # without this condition test with 2466 tokens crashes
                        suffix, branch_children = branch_buffer.popitem()

                if branch_children:                                 # if anything left from the previous iteration
                    child = branch_children.pop()[0]                # pick one child for a current suffix: thus we branch
                else:
                    break

                if branch_children:                                 # if any children for this suffix left to branch
                    branch_buffer[suffix] = branch_children         # we put them back into the buffer with their suffix as a key
                
                cur = mdb                      # here we step through all the suffix chars
                for char in suffix:            # down or sub-trie to get to the branching node
                    cur = cur[char]

                suffix += child
                cur = cur[child]                # here we switch to the current branch

            else:
                break                          # if branch_buffer is empty and we reach the end of the word, no words left
        
        children = list(cur.keys())
        
        if children[-1]:                       # without this condition a nonsubscriptable type error occurs
            child = children.pop()[0]          # TODO: if [0] is nesseccary?
        else:
            child = {None:None}
            children.pop()            
        if children:
            branch_buffer[suffix] = children    # if cursor meets branch, it writes the suffix and the node children to the buffer
        if child == {None:None}:                # TODO: keys() are iterator, I should use this property. Store iterators in brach_buffer
            cur = child
        else:
            suffix += child                     # TODO: turn suffix into a list
            cur = cur[child]
    
    return suffixes

    # return iterable[str]


def retrive_suffixes_by_prefix(mdb:dict, prefix:str, limit:int=10):
    subtrie = find_prefix(mdb=mdb, prefix=prefix)
    if subtrie:
        itsuf = iterate_suffixes(subtrie)
        if not limit:
            suffixes = [suf for suf in itsuf]
        else:
            suffixes = []
            for suf in itsuf:
                suffixes.append(suf)
                limit -= 1
                if limit == 0:
                    return suffixes
        return suffixes
    else:
        return None

    # return list[str]

# external API methods:

def load_db(path:str=None):
    mdb = init_db()
    if path:
        itokens = iterable_tokens(path=path)
        for itoken in itokens:
            add_to_db(mdb=mdb, token=itoken)
    return mdb


def get_suggestions(mdb:dict, prefix:str, limit:int=None):
    suffixes = retrive_suffixes_by_prefix(mdb=mdb, prefix=prefix, limit=limit)
    if suffixes:
        suggestions = [prefix + suffix for suffix in suffixes]
        return suggestions
    else:
        return []