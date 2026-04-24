from pseudo.code_generator import CodeGenerator, switch
from pseudo.middlewares import DeclarationMiddleware, NameMiddleware, TupleMiddleware
from pseudo.pseudo_tree import Node, local

OPS = {'not': '!', 'and': '&&', 'or': '||'}

def index_switch(s):
    pass

class CSharpGenerator(CodeGenerator):
    '''CSharp code generator'''

    indent = 4
    use_spaces = True
    middlewares = [TupleMiddleware(all=False),
                   DeclarationMiddleware,
                   NameMiddleware(
                       normal_name='camel_case', 
                       method_name='pascal_case',
                       function_name='pascal_case')]

    types = {
      'Int': 'int',
      'Float': 'float',
      'Boolean': 'bool',
      'String': 'string',
      'List': 'List<{0}>',
      'Dictionary': 'Dictionary<{0}, {1}>',
      'Set': 'HashSet<{0}>',
      'Tuple': lambda x: 'Tuple<{0}>'.format(', '.join(x)),
      'Array': '{0}[]', 
      # fixed-size buffers in c# are not widely used
      # they require a struct and an unsafe annotation
      # we can a unsafe-fixed-size-buffer option to config
      'Void': 'void',
      'Regexp': 'Regex',
      'RegexpMatch': 'Match'
    }

    templates = dict(
        module     = '''
            using System;
            %<dependencies:lines>
            %<custom_exceptions:lines>
            %<tuple_definitions:lines>
            %<#class_definitions>
            public class Program
            {
                %<constants:lines>
            %<#function_definitions>
                public static void Main(string[] args)
                {
                    %<main:semi>
                }
            }''',

        function_definition   = '''
            static %<@return_type> %<name>(%<#params>)
            {
                %<block:semi>
            }''',

        method_definition =     '''
            %<.is_public> %<@return_type> %<name>(%<#params>)
            {
                %<block:semi>
            }''',

        method_definition_is_public = ('public', 'private'),

        class_definition = '''
            public class %<name>%<.base>
            {
                %<attrs:lines>
                %<.constructor>
                %<methods:line_join>
            }''',

        class_definition_base = ('%<#base>', ''),

        class_definition_constructor = ('%<constructor>', ''),

        class_attr = "%<.is_public>%<@pseudo_type> %<name:camel_case 'lower'>;",

        class_attr_is_public = ('public ', 'private '),
            
        immutable_class_attr = '''
            private readonly %<@pseudo_type> %<name>;
            public %<@pseudo_type> %<name:camel_case 'title'> { get { return %<name>; } }''',

        anonymous_function = "%<#anon_params> =>%<#anon_block>",

        constructor = '''
            public %<this>(%<#params>)
            {
                %<block:semi>
            }''',

        dependency  = 'using %<name>;',


        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_double>',
        boolean     = '%<value>',
        null        = 'null',

        simple_initializer = "new %<name>(%<args:join ', '>)",
        list        = switch(lambda l: len(l.elements) > 0,
                            true =          "new[] {%<elements:join ', '>}",
                            _otherwise =    "Enumerable.Empty<int>()"
                    ),
        dictionary  = switch(lambda d: len(d.pairs) > 0,
                            true =  "new %<@pseudo_type> { %<pairs:join ', '> }",
                            _otherwise = "new Dictionary<int, int> {}"
                    ),
        pair        = "{%<key>, %<value>}",
        attr        = "%<object>.%<attr>",

        new_instance = "new %<class_name>(%<args:join ', '>)",

        # assignment  = '%<#z>',
        assignment  = switch('first_mention',
            true       = 'var %<target> = %<value>', # in v0.3 add config/use var only for generic types
            _otherwise = '%<target> = %<value>'
        ),

        tuple       = switch(lambda e: len(e.elements) <= 2,
                        true = "Tuple.Create(%<elements:join ', '>)",
                        _otherwise = '''
                            Tuple.Create(
                                %<elements:c_lines>
                            )'''),

        array       = "new[] { %<elements:join ', '> }",

        set         = switch(lambda s: len(s.elements) > 0,
                        true        = "new %<@pseudo_type>(new[] {%<elements:join ', '>})",
                        _otherwise  = "new HashSet<int>()"
                    ),

        char        = "%<#char>",
        binary_op   = '%<#binary_left> %<#op> %<#binary_right>',
        unary_op    = '%<#op>%<value>',
        comparison  = '%<#comparison>',

        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",
        this_method_call = "this.%<message:camel_case 'title'>(%<args:join ', '>)",

        this        = 'this',

        instance_variable = 'this.%<name>',

        throw_statement = 'throw new %<exception>(%<value>)',

        if_statement    = '''
            if (%<test>)
            {
                %<block:semi>
            }
            %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            else if (%<test>)
            {
                %<block:semi>
            }
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else 
            {
                %<block:semi>
            }''',

        while_statement = '''
            while (%<test>)
            {
                %<block:semi>
            }''',

        try_statement = '''
            try
            {
                %<block:semi>
            }
            %<handlers:lines>''',

        exception_handler = '''
            catch (%<.exception> %<instance>)
            {
                %<block:semi>
            }''',

        exception_handler_exception = ('%<exception>', 'Exception'),

        for_each_statement = '''
            for %<iterator> in %<sequence>:
                %<#block>''',
    
        for_each_with_index_statement = '''
            for %<index>, %<iterator> in %<.sequence>:
                %<#block>''',

        for_each_with_index_statement_sequence = ('%<#index_sequence>', ''),

        for_each_in_zip_statement = '''
            for %<iterators:join ', '> in zip(%<sequences:join ', '>):
                %<#block>''',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        index            = switch(index_switch,
            tuple           = '%<sequence>.Item%<#tuple_index>',
            normal          = '%<sequence>[%<index>]',
            _otherwise      = '%<sequence>[%<sequence>.Length - %<#index>]'
        ),

        interpolation = "string.Format(\"%<args:join ''>\",  %<#placeholders>)",

        interpolation_placeholder = "{%<index>}",

        interpolation_literal = "%<value>",

        index_assignment = '%<sequence>[%<index>] = %<value>',

        not_null_check = '%<value> != null',

        constant = '%<constant> = %<init>',

        for_statement = switch(lambda f: f.iterators.type,
            for_iterator_with_index = '''
                for (int %<iterators.index> = 0; %<iterators.index> < %<sequences.sequence>.Length; %<iterators.index> ++)
                {
                    var %<iterators.iterator> = %<sequences.sequence>[%<iterators.index>];
                    %<block:semi>
                }''',

            for_iterator_zip = '''
                for (int _index = 0; _index < %<#first_sequence>.Length; _index ++)
                {
                    %<#zip_iterators>
                    %<block:semi>
                }''',

            for_iterator_with_items = '''
                foreach(var _item in %<sequences.sequence>)
                {
                    var %<iterators.key> = _item.key;
                    var %<iterators.value> = _item.value;
                    %<block:semi>
                }''',
            _otherwise = '''
                foreach(%<iterators> in %<sequences>)
                {
                    %<block:semi>
                }'''
        ),
        
        for_range_statement = '''
            for (int %<index> = %<.first>; %<index> != %<end>; %<index> += %<.step>)
            {
                %<block:semi>
            }''',

        for_range_statement_first = ('%<start>', '0'),

        for_range_statement_step = ('%<step>', '1'),

        for_iterator = 'var %<iterator>',

        for_iterator_zip = "var %<iterators:join ', '>",

        for_iterator_with_index = 'int %<index>, var %<iterator>',

        for_iterator_with_items = '%<key>, %<value>',

        for_sequence = '%<sequence>',

        custom_exception = '''
            public class %<name> : Exception
            {
                public %<name>(string message)
                    : base(message)
                {
                }
            }''',

        standard_iterable_call = '''
                    %<sequences>
                        .Where(%<iterators.iterator> => %<test:first>)
                        .Select(%<iterators.iterator> => %<block:first>)
                        .ToList()''',

        aug_assignment = '%<target> %<op>= %<value>',

        block = '%<block:semi>',

        regex = '@"%<value>'
    )

    def params(self, node, indent):
        pass

    def anon_params(self, node, indent):
        pass

    def anon_block(self, node, indent):
        # print(indent);input(node.params[0].y)     
        pass

    def class_definitions(self, node, depth):
        pass

    def function_definitions(self, node, depth):
        pass

    def base(self, node, depth):
        pass

    def first_sequence(self, node, depth):
        pass

    def zip_iterators(self, node, depth):
        pass

    def tuple_index(self, node, depth):
        pass

    def op(self, node, depth):
        pass

    def char(self, node, depth):
        pass

    # args starting from 0
    def comparison(self, node, depth):
        pass

    def z(self, node, depth):
        pass

    def index(self, node, depth):
        pass

    def placeholders(self, node, depth):
        pass

