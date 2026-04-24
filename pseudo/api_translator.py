from pseudo.tree_transformer import TreeTransformer
from pseudo.pseudo_tree import Node, to_node, method_call, call, local
from pseudo.errors import PseudoStandardLibraryError, PseudoDSLError
from pseudo.api_handlers import LeakingNode, NormalLeakingNode, BizarreLeakingNode
import copy

TYPES = {'List', 'Dictionary', 'Set', 'Tuple', 'Regexp', 'Array', 'String'}

def to_op(op, reversed=False):
    '''
    create a function that transforms a method to a binary op

    often we need to convert a pseudo method
    <receiver>.<message>(<z>) to a binary op
    <receiver> <op> <message>
    that's a decorator that helps for that
    '''
    def transformer(receiver, param, pseudo_type):
        pass
    return transformer


class ApiTranslator(TreeTransformer):
    '''
    A base class for the api translators

    DSL:
    you can use either 
      a lambda/function defined in <lang>_api_handlers.py which returns a Node with signature
    `(receiver, *args)` (e.g. `lambda receiver, value: Node('none'))
    or
      a <Name> class inheriting from LeakingNode 
      which can inject nodes in the closest block
    or

    shortcuts:
    '#method_name'  => calls that method of the receiver with the same args
    'function_name' => calls that function with the same args
    'namespace.function_name' => calls the function in the namespace
    '.attr_name!'   => accesses that attribute of the receiver
    '.method_name'  => calls that static method
    `to_op(op)`     => transforms `receiver.method(arg)` to a `receiver op arg` binary

    `class_name<shortcut>` =>
        transforms into the method/attr according to previous rules but of the class_name class,
        not the equivalent one

    `<shortcut>(%{0}, %{self})` =>
        transforms into the call according to previous rules but with args ordered like in the
        placeholders

        %{<number>}      => the n-th arg(starts from 0)
        %{self}          => the receiver of the method
        %{equivalent}    => the equivalent class
        %{<other-name>}  => each language translator can redefine it with
                            def <other-name>_placeholder(self, receiver, *args, equivalent) which
                            should return a Node


    Nodes: Nodes can be either the official pseudo nodes or in special cases
           with `_<special_node>` when they describe syntax typical only for
           the target language of the translator

    helpers: quite useful helpers from pseudo.pseudo_tree are
             `method_call(receiver: str/Node, message: str, args: [Node])`
                 which helps with method call nodes with normal `local` name object receivers

             `call(callee: str/Node, args: [Node])`
                 which helps with call nodes with normal `local` name callees
    '''

    def __init__(self, tree):
        self.tree = copy.deepcopy(tree)

    def api_translate(self):
        self.standard_dependencies = set()
        self.used = set()
        self.leaked_nodes = []
        transformed = self.transform(self.tree)

        for l in self.used:
            m = self.dependencies.get(l, {}).get('@all')
            if m:
                if isinstance(m, list):
                    self.standard_dependencies |= set(m)
                else:
                    self.standard_dependencies.add(m)

        transformed.dependencies = [
            Node('dependency', name=name) for name in self.standard_dependencies]

        return transformed

    def after(self, node, in_block, assignment):
        if node and not isinstance(node, Node):
            return node
        if node:
            if node.type.title() in TYPES:
                self.used.add(node.type.title())
            # elif isinstance(node, list) and node.type[0] in TYPES:
            #     self.used.add(node.type[0].title())
        if node and (node.type == 'try_statement' or node.type == 'throw_statement'):
            self.used.add('Exception')
        if node and node.type == 'assignment' and node.value:
            self.update_used(node.value.pseudo_type)

        if node and node.type == 'assignment' and node.value and node.value.type == 'binary_op':
            if node.value.right == node.target:
                node = Node('operation_assign', slot=node.value.left, op=node.value.op, value=node.value.right)
        
        if node and hasattr(node, 'params'):
            self.update_used(node.pseudo_type)

        if node and node.type == 'static_call':
            if node.receiver.type == 'local' and hasattr(self, 'js_dependencies') and node.receiver.name in self.js_dependencies:
                self.standard_dependencies.add(self.js_dependencies[node.receiver.name])                

        if in_block:
            results = [ass for ass in self.leaked_nodes]
            # input(type(self).__name__ )
            if type(self).__name__ == 'GolangTranslator':
                2# 2 input(node)
            if node and not (node.type == 'assignment' and node.value is None):
                results.append(node)
            self.leaked_nodes = []
            return results
            
        else:
            return node


    def transform_standard_method_call(self, node, in_block=False, assignment=None):
        pass

    def leaking(self, z, module, name, node, context, *data):
        '''
        an expression leaking ...

        assignment nodes into the nearest block list of nodes
        c++ guys, stay calm
        '''
        pass

    def transform_standard_call(self, node, in_block=False, assignment=None):
        pass

    def update_dependencies(self, namespace, function, arg_types):
        pass


    def _expand_api(self, api, receiver, args, pseudo_type, equivalent):
        '''
        the heart of api translation dsl

        function or <z>(<arg>, ..) can be expanded, <z> can be just a name for a global function, or #name for method, <arg> can be %{self} for self or %{n} for nth arg
        '''
        pass

    def _parse_part(self, part, receiver, args, equivalent):
        pass

    def update_used(self, t):
        if isinstance(t, list):
            for type_ in t:
                if isinstance(type_, str):
                    if type_ in TYPES:
                        self.used.add(type_)
                else:
                    self.update_used(type_)
        else:
            if t in TYPES:
                self.used.add(t)
