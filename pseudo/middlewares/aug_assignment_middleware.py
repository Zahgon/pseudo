from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node

class AugAssignmentMiddleware(Middleware):
    '''
    changes `%<x> = %<x> op %<value>`  to `%<x> += %<value>` nodes
    `
    '''

    @classmethod
    def process(cls, tree):
        return cls().transform(tree)

    def transform_assignment(self, node, in_block=False, assignment=None):
        pass

