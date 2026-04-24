from pseudo.pseudo_tree import Node, call, method_call, local, assignment, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

def contains(receiver, element, pseudo_type):
    return Node('_py_in', value=element, sequence=receiver, pseudo_type='Boolean')

def to_py_generatorcomp(method):
    def x(receiver, test, pseudo_type):
        pass
    return x

def expand_set_slice(receiver, from_=None, to=None, value=None, pseudo_type=None):
    s = expand_slice(receiver, from_, to, pseudo_type)
    return assignment(s, value)

def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if pseudo_type: #to
            if from_.type == 'int' and from_.value == 0:
                return Node('_py_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
            else:
                return Node('_py_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            pseudo_type = to
            return Node('_py_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        return Node('_py_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
    else:
        return None

class ReadFile(BizarreLeakingNode):
    '''
    transforms `io:read_file`

    `io:read_file(name)`
    to 
    `with open(name, 'r') as _f:
        <target>/_file_contents = f.read()`
    '''

    def temp_name(self, target):
        pass

    # assign : as_assignment 
    # block-level: as_expression
    # inside: as_assignment with temp_name as target
    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass


class WriteFile(NormalLeakingNode):
    '''
    transforms `io:write_file`

    `io:write_file(name, stuff)`
    `with open(name, 'w') as _f:
        _f.write(stuff)`
    '''

    def as_expression(self):
        pass

