from pseudo.middlewares.middleware import Middleware
from pseudo.pseudo_tree import Node, assignment, local, attr, typename
from pseudo.tree_transformer import TreeTransformer
from pseudo.helpers import safe_serialize_type, general_type, camel_case

class TupleMiddleware(Middleware):
    '''
    middleware for expressing tuples with structs

    currently used with go(to translate all tuples, because no generics)
    and with c#/c++
    (in the future we can also generate NamedTuples for python,
     but for now arrays/lists are capable enough in dynamic languages)
    if Tuple[A, B] is used, create a class/struct with immutable
    fields with those types, convert the tuple to a struct/class initialize

    It works by:
      
      detecting meaningful names corresponding to a tuple
      in function/method params and call args,

      detecting meaningful names for its fields if it sees a 
      call(..t[0], t[1]..t[-1]) kind of use and convert index accesses
      and tuples for that tuple type to the class equivalents 

    If it can't find a good name, it uses tuples for C#/C++ and
    it uses
    an auto-generated ugly name for Go
    '''

    def process(self, tree):
        self.tree = tree
        self.tuple_definitions = {}
        return self.transform_and_create()

    def __init__(self, all=True):
        self.all = all

    def after(self, n, *z):
        if hasattr(n, 'pseudo_type') and isinstance(n.pseudo_type, list):
            n.pseudo_type = self.clean_tuple_class_type(n.pseudo_type)
        if hasattr(n, 'return_type') and isinstance(n.return_type, list):
            n.return_type = self.clean_tuple_class_type(n.return_type)
        if hasattr(n, 'decl_type') and isinstance(n.decl_type, list):
            n.decl_type = self.clean_tuple_class_type(n.decl_type)
        return n

    def clean_tuple_class_type(self, t):
        if isinstance(t, list):
            if t[0] == 'Tuple':
                a = self.tuple_definitions.get(safe_serialize_type(t))
                if a:
                    return camel_case(a[0])
            t[1:] = [self.clean_tuple_class_type(child) for child in t[1:]]
        return t


    def transform_and_create(self):
        self.tuple_definitions = {}
        self.function_index = {'functions': {}}
        self.params = []
        # detect param class
        self.tree = self.function_walk(self.tree)
        # detect arg fields
        self.tree = ArgWalker(self).transform(self.tree)
        # replace
        self.tree = self.transform(self.tree)
        self.tree.tuple_definitions = [self.with_constructor(t) for t in self.tuple_definitions.values()]
        return self.tree

    def with_constructor(self, t):
        t = t[1]
        t.name = camel_case(t.name)
        if self.all == False:
            t.constructor = Node('constructor',
                params=[local(field.name, field.pseudo_type) for field in t.attrs],
                this=typename(t.name),
                pseudo_type = ['Function'] + [field.pseudo_type for field in t.attrs] + [t.name],
                return_type=t.name,
                block=[
                    assignment(
                        Node('instance_variable', name=field.name, pseudo_type=field.pseudo_type),
                        local(field.name, field.pseudo_type),
                        first_mention=False)
                    for field
                    in t.attrs])
        return t

    def transform_tuple(self, node, in_block=False, assignment=None):
        pass

    def transform_index(self, n, in_block=False, assignment=None):
        pass

    def transform_special_f(self, n, in_block=False, assignment=None):
        for a in n.params:
            if general_type(a.pseudo_type) == 'Tuple':
                s = safe_serialize_type(a.pseudo_type)
                if s not in self.tuple_definitions:
                    self.tuple_definitions[s] = a, Node('class_definition',
                        name=a.name,
                        base=None,
                        attrs=[Node('immutable_class_attr', name='item%d' % j, is_public=True, pseudo_type=q) for j, q in enumerate(a.pseudo_type[1:])],
                        constructor=None,
                        methods=[])
        if n.type == 'constructor':
            if self.current_class.name not in self.function_index:
                self.function_index[self.current_class.name] = {}
            self.function_index[self.current_class.name]['__init__'] = n
        elif n.type == 'method_definition':
            if self.current_class.name not in self.function_index:
                self.function_index[self.current_class.name] = {}
            self.function_index[self.current_class.name][n.name] = n
        else:
            self.function_index['functions'][n.name] = n

        return n

class BlockRewriter(TreeTransformer):
    def __init__(self, old_params, l):
        self.old_params = old_params
        self.l = l

    def transform_local(self, node, in_block=False, assignment=None):
        pass

class ArgWalker(TreeTransformer):
    def __init__(self, tuple_definition):
        self.tuple_definition = tuple_definition

    def transform_general_call(self, n, in_block=False, assignment=None):
        pass

    transform_call = transform_method_call = transform_new_instance = transform_general_call


    def tuple_index(self, n):
        '''s[<int>] where s is a Tuple[T1..]'''
        pass


    def successive(self, sequence, j, a):
        # import pdb;pdb.set_trace()
        pass
