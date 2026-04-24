from pseudo.middlewares.middleware import Middleware

class DeclarationMiddleware(Middleware):
    '''
    finds and marks first initializations of locals

    adds a boolean first_mention field to assignments for first mentions of locals as targets of
    assignments
    adds a local_declarations array with local not-arg names to function/methods
    rebuilds tree TreeTransformer in place!!
    '''

    @classmethod
    def process(cls, tree):
        return cls(tree).transform(tree)

    def __init__(self, tree):
        self.envs = [set()]
    
    def transform_module(self, node, in_block=False, assignment=None):
        pass

    def transform_f(self, node, in_block=False, assignment=None):
        pass

    transform_function = transform_methods = transfrom_anonymous_function = transform_f

    def transform_assignment(self, node, in_block=False, assignment=None):
        pass

    def transform__go_multi_assignment(self, node, in_block=False, assignment=False):
        pass

