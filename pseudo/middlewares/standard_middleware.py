from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node

class StandardMiddleware(Middleware):
    '''
    changes standard_iterable_call in return to a special type

    used by go
    '''

    @classmethod
    def process(cls, tree):
        return cls().transform(tree)

    def transform_r(self, node, in_block=False, assignment=None):
        pass

    transform_explicit_return = transform_implicit_return = transform_r
