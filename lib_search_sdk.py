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
# TODO: keys() are iterator, so I should use this property to store iterators and not lists in the brach_buffer
def iterate_suffixes(mdb:dict):
    suffixes = []
    branch_buffer = {}

    suffix = []
    cur = mdb
    
    while cur:
        # when we reach the word end
        if cur == {None: None}:
            # we turn the suffix into a string then yield it
            yield ''.join(suffix)
            # if branch buffer is not empty
            # we extract the last added path to the branch and the branching node's children from the buffer
            if branch_buffer:
                branch_path, branch_children = branch_buffer.popitem()
                # in some situations this check is required even more than once
                while branch_children and not branch_children[-1]:
                    yield branch_path
                    branch_children.pop()
                    # without this condition test with 2466 tokens crashes
                    if branch_buffer:
                        branch_path, branch_children = branch_buffer.popitem()

                # if anything is left to process from the previous step
                if branch_children:
                    # pick one child for a current branch
                    child = branch_children.pop()
                else:
                    break

                # if any children still left unattended for this branch
                # we put them back into the buffer with the path to the branch as a key
                if branch_children:
                    branch_buffer[branch_path] = branch_children

                # here we step through all the branch path chars
                # down the sub-trie to get to the branching node
                # also we convert the branch_path to the beginning of the suffix
                # suffix is a list to speed up appending characters to it
                cur = mdb
                suffix = []
                for char in branch_path:
                    cur = cur[char]
                    suffix.append(char)

                # and here we switch to the current branch
                suffix.append(child)
                cur = cur[child]

            # if branch_buffer is empty, and we reach the end of the word, no words left
            else:
                break
        
        children = list(cur.keys())

        # without this condition a nonsubscriptable type error occurs
        if children[-1]:
            child = children.pop()
        else:
            child = {None:None}
            children.pop()
        # if cursor meets branch, it writes the suffix and the node children to the buffer
        if children:
            branch_path = ''.join(suffix)
            branch_buffer[branch_path] = children
        if child == {None:None}:
            cur = child
        else:
            suffix.append(child)
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
            try:
                suffixes = [next(itsuf) for i in range(limit)]
            except StopIteration:
                itsuf = iterate_suffixes(subtrie)
                suffixes = [suf for suf in itsuf]
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