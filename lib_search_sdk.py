# these methods are to be implemented

# internal methods:

def init_db():
    return {}


def add_to_db(mdb:dict, token:str):
    token_added = False
    cur = mdb
    for char in token:
        if char not in cur:
            cur[char] = {}
            token_added = True
        cur = cur[char]
    cur[None] = None
    return token_added

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


def find_prefix(mdb:dict, prefix:str):
    cur = mdb
    for char in prefix:
        if char in cur:
            cur = cur[char]
        else:
            return None
    return cur
    
# return dict
# start from root mdb and returns root for end of prefix


# iterative implementation of tree traversal with a branch buffer
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
                child = branch_children.pop()[0]                    # pick one child for a current suffix: thus we branch
                if branch_children:                                 # if any children for this suffix left to branch
                    branch_buffer[suffix] = branch_children         # we put them back into the buffer with their suffix as a key
                
                cur = mdb                      # here we step through all the suffix chars
                for char in suffix:            # down or sub-trie to get to the branching node
                    cur = cur[char]
                
                else:
                    suffix += child                
                    cur = cur[child]           # here we switch to the current branch
            else:
                break                          # if branch_buffer is empty and we reach the end of the word, no words left
        
        children = list(cur.keys())
        
        if children[-1]:                       # without this condition a nonsubscriptable type error occurs
            child = children.pop()[0]
        else:
            child = {None:None}
            children.pop()            
        if children:
            branch_buffer[suffix] = children    # if cursor meets branch, it writes the suffix and the node children to the buffer
        if child == {None:None}:
            cur = child
        else:
            suffix += child
            cur = cur[child]
    
    return suffixes

    # return iterable[str]


def retrive_suffixes_by_prefix(mdb:dict, prefix:str, limit:int=None):
    subtrie = find_prefix(mdb=mdb, prefix=prefix)
    if subtrie:
        itsuf = iterate_suffixes(subtrie)
        if not limit:
            suffixes = [suf for suf in itsuf]
        else:
            suffixes = [next(itsuf) for i in range(limit)]
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
    suggestions = [prefix + suffix for suffix in suffixes]
    return suggestions