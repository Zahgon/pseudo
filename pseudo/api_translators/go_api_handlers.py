from pseudo.pseudo_tree import Node, call, method_call, local, assignment, attr, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode
from pseudo.tree_transformer import TreeTransformer

def expand_push(receiver, element):
        pass

def expand_insert(receiver, index, element):
    return call('append', [])

def empty(s, _):
    return Node('binary_op',
                op='==',
                left=call('len', [s], 'Int'),
                right=to_node(0),
                pseudo_type='Boolean')

def present(s, _):
    return Node('binary_op',
                op='>',
                left=call('len', [s], 'Int'),
                right=to_node(0),
                pseudo_type='Boolean')    

class ExpandMap(BizarreLeakingNode):
    def temp_name(self, target):
        pass

    default = '_results'

    def as_expression(self, target=None):
        pass

    def as_assignment(self, target):
        pass

expand_map = ExpandMap

class ExpandFilter(ExpandMap):
    def as_expression(self, target=None):
        pass

expand_filter = ExpandFilter

class ExpandReduce(ExpandMap):
    default = 'accumulator'
    def as_expression(self, target=None):
        pass


expand_reduce = ExpandReduce

def extract_name(s, default=None):
    pass

class Find(ExpandMap):
    default = '_found'
    def as_expression(self, target=None):
        pass
                

def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if pseudo_type: #to
            if from_.type == 'int' and from_.value == 0:
                return Node('_go_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
            else:
                if from_.type == 'int' and from_.value < 0:
                    from_ = Node('binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(-from_.value), pseudo_type='Int')
                if to.type == 'int' and to.value < 0:
                    to = Node('binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(-to.value), pseudo_type='Int')

                return Node('_go_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            pseudo_type = to
            return Node('_go_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        if to.type == 'int' and to.value < 0:
            to = Node('binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(-to.value), pseudo_type='Int')
        return Node('_go_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
    else:
        return None

class ListContains(ExpandMap):
    default = '_contains'

    def as_expression(self, target=None):
        pass
        

class Contains(BizarreLeakingNode):
    '''
    transform `sequenc:contains?`
    '''
    def temp_name(self, target):
        pass

    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass
class Int(BizarreLeakingNode):
    count = 0

    def temp_name(self, _, i=True):
        pass

    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass

            

class ReduceRewriter(TreeTransformer):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def transform_local(self, node, *x):
        pass

class DictItems(BizarreLeakingNode):
    def temp_name(self, _):
        pass

    def singular_name(self):
        pass

    def index(self):
        pass

    def as_expression(self):
        pass


class DictKeys(DictItems):
    field = 'keys'

class DictValues(DictItems):
    field = 'values'

class ReadFile(BizarreLeakingNode):
    '''transforms io:read_file'''
    def temp_name(self, target):
        pass

    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass

class Read(BizarreLeakingNode):
    '''
    transform `io:read`
    '''

    def temp_name(self, target):
        pass

    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass

