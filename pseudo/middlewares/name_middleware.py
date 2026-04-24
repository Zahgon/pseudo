from pseudo.middlewares.middleware import Middleware

class NameMiddleware(Middleware):
    '''
    changes names according to language conventions

    can accept rules for normal_name, method_name and function_name
    available rules: snake_case, camel_case, pascal_case

    currently used c#, go, javascript and php
    '''

    def __init__(self, normal_name=None, method_name=None, function_name=None, attr_name=None):
        self.normal_name = normal_name
        self.method_name = method_name
        self.function_name = function_name
        self.attr_name = attr_name
        self.current_class_ = None

    def process(self, tree):
        self.tree = tree
        self.defined_functions = {q.name for q in self.tree.definitions if q.type == 'function_definition'}
        return self.transform(tree)

    def transform_normal_name(self, node, in_block=False, assignment=None):
        pass
    
    transform_local = transform_instance_variable = transform_normal_name

    def transform_f(self, node, in_block=False, assignment=None):
        pass

    transform_function_definition = transform_method_definition = transfrom_anonymous_function = transform_f

    def transform_method_call(self, node, in_block=False, assignment=None):
        pass

    def transform_this_method_call(self, node, in_block=False, assignment=None):
        pass

    def transform_attr(self, node, in_block=False, assignment=None):
        pass
    
    def transform_class_definition(self, node, in_block=False, assignment=None):
        pass

    def transform_attr_name(self, node, in_block=False, assignment=None):
        pass

    transform_class_attr = transform_instance_variable = transform_immutable_class_attr = transform_attr_name
    
    def convert_to_pascal_case(self, name):
        pass

    def convert_to_camel_case(self, name):
        pass

    def convert_to_snake_case(self, name):
        pass

    def words(self, name):
        pass
