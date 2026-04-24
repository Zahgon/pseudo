from pseudo.pseudo_tree import Node, call, method_call, local, assignment, to_node

def display(*values):
    if all(isinstance(v.pseudo_type, str) for v in values[:-1]):
        name = 'puts'
    else:
        name = 'p'

    return call(name, values[:-1], 'Void')


def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if pseudo_type: #to
            return Node('_rb_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            pseudo_type = to
            return Node('_rb_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        return Node('_rb_slice', sequence=receiver, from_=to_node(0), to=to, pseudo_type=pseudo_type)
    else:
        return None

def to_method_rb_block(name):
    def l(receiver, *args):
        pass
    return l


