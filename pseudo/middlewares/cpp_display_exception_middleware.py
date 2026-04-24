from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node, method_call

class CppDisplayExceptionMiddleware(Middleware):
    '''
    converts `cout << e` to a `cout << e.what()` node
    '''

    @classmethod
    def process(cls, tree):
        return cls(tree).transform(tree)

    def __init__(self, tree):
        self.tree = tree

    def transform__cpp_cout(self, node, in_block=False, assignment=None):
        pass
