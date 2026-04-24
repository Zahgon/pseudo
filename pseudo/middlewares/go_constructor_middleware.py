from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node, assignment as assi, typename, local
from pseudo.tree_transformer import TreeTransformer

class GoConstructorMiddleware(Middleware):
    '''
    go: middleware for translation of constructors

    translate constructor calls which just initialize
    values to {} initializers
    translate constructors starting with nodes like
      newA(b int, x int) ..
        this.z = b + x
        this.z2 = b
        other
    to nodes like
      newA(b int, x int) ..
        this = A{b + x, b}
        other
    '''

    @classmethod
    def process(cls, tree):
        s = ConstructorTransformer()
        tree = s.transform(tree)
        result = cls(tree, s.classes_with_simple_initializers).transform(tree)
        return result

    def __init__(self, tree, classes_with_simple_initializers):
        self.current_class, self.current_function = None, None
        self.classes_with_simple_initializers = classes_with_simple_initializers

    def transform_new_instance(self, node, in_block=False, assignment=None):
        pass

class ConstructorTransformer(TreeTransformer):
    whitelist = {'module', 'class_definition', 'constructor'}
    
    def __init__(self):
        self.classes_with_simple_initializers = set()

    def transform_constructor(self, node, in_block=False, assignment=None):
        pass

# go is a really simple language and one of its 
# strengths is that a shitload of stuff is completely
# different than in all other mainstream languages
# but hey, at least it doesn't have erlang syntax right
# or elixir macroses, *faints when imagining so much power
# in a programming language*
