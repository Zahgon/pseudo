from pseudo.pseudo_tree import Node, call, method_call, local, assignment, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

class Read(BizarreLeakingNode):
    '''
    transforms `io:read`

    `a = io:read()`
    `cin << a`
    '''

    def temp_name(self, target):
        pass

    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass

class Slice(BizarreLeakingNode):
    '''
    transforms `List:slice..`
    '''

    def temp_name(self, target):
        pass

    def as_expression(self):
        # pseudo_type=self.args[0].pseudo_type
        pass

    def as_assignment(self, target):
        pass

class ReadFile(BizarreLeakingNode):
    '''
    transforms `io:read_file`
    '''

    def temp_name(self, target):
        pass

    def as_expression(self):
        pass

    def as_assignment(self, target):
        pass
