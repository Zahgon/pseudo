# base generator with common functionality
import re
from pseudo.pseudo_tree import Node
from pseudo.code_generator_dsl import Placeholder, Newline, Action, Function, SubTemplate, SubElement, PseudoType, Whitespace, Offset, INTERNAL_WHITESPACE, NEWLINE
from pseudo.middlewares import AugAssignmentMiddleware
LINE_FIRS = re.compile(r'^( +)')
TOO_MANY_ENDLINES = re.compile(r'(\n\n\n+)')
CLOSING_CURLY_ENDLINES = re.compile(r'}\n(\n+)([ \t]*)}')
JS_BRACKET = re.compile(r'}\n *([,\)])')

# for all!
DEFAULT_MIDDLEWARES = [AugAssignmentMiddleware]

class CodeGenerator:
    '''
    options:
      indent: the size of indent, example: python - 4, ruby - 2
      spaces: use spaces if true, tabs if false
    '''

    def __init__(self, indent=None, use_spaces=None):
        if indent: self.indent = indent
        if use_spaces: self.use_spaces = use_spaces
        # always init them in classes
        self._symbol = ' ' if self.use_spaces else '\t'
        self._single_indent = self._symbol * (self.indent)
        self._parsed_templates = {k: self._parse_template(v, k) for k, v in self.templates.items()}
        self.a = [] # additional code, lambdas etc
        # print('[]')
        # for z in self._parsed_templates['function_definition']:
        #     if hasattr(z, 'y'):
        #         print(z.y)
        #     else:
        #         print(z)
        # input()

    def generate(self, tree):
        '''
        generates code based on templates and gen functions
        defined in the <x> lang generator
        '''
        for middleware in DEFAULT_MIDDLEWARES + self.middlewares:
            tree = middleware.process(tree) # changed in place!!
        original = self._generate_node(tree)
        # first n lines n dependencies
        # after that additional code

        if self.a and tree.type == 'module':
            p = original.split('\n')
            r = '\n'.join(p[:len(tree.dependencies)] + (['\n'] if tree.dependencies else []) + self.a + ['\n'] + p[len(tree.dependencies):]) + '\n'
        else:
            r = original
        r = re.sub(CLOSING_CURLY_ENDLINES, r'}\n\2}', r)
        r = re.sub(JS_BRACKET, r'}\1', r)
        return re.sub(TOO_MANY_ENDLINES, r'\n\n', r)

    def action_line_join_pass(self, expanded, _):
        pass

    def action_join(self, expanded, separator, depth):
        pass

    def action_join_depth_aware(self, expanded, separator, depth):
        # a big hack, fix in v0.3..dsl omits depth for non-newline join, but not for join_depth_aware
        pass

    def action_join_lws(self, expanded, separator, depth):
        pass

    def action_each_rpad(self, expanded, value, depth):
        pass

    def action_each_lpad(self, expanded, value, depth):
        pass

    def action_last(self, expanded, depth):
        pass

    def action_first(self, expanded, depth):
        pass

    def action_join_rest(self, expanded, separator, depth):
        pass

    def action_lines(self, expanded, depth):
        pass

    def action_semi_lines(self, expanded, depth):
        pass

    def action_semi(self, expanded, depth):
        # input(expanded)
        
        pass

    def action_c_lines(self, expanded, depth):
        pass

    def action_line_join(self, expanded, depth):
        pass

    def action_camel_case(self, expanded, case, depth):
        pass

    def action_lines_before(self, expanded, depth):
        pass

    def _generate_node(self, node, depth=0):
        # if isinstance(node, list):
        #     return self._generate_node(Node('block', block=node), depth)
        if not isinstance(node, Node):
            return node
        elif node.type in self._parsed_templates:
            return self._generate_from_template(self._parsed_templates[node.type], node, depth)
        elif hasattr(self, 'generate_%s' % node.type):
            return getattr(self, 'generate_%s' % node.type)(node, depth)
        else:
            raise NotImplementedError("no action for %s" % node.type)

    def _generate_from_template(self, template, node, depth):
        if isinstance(template, dict): # and type(self).__name__ == 'JsGenerator':
            if isinstance(template['_key'], str):
                t = template.get(str(getattr(node, template['_key'])).lower())
            else:
                t = template.get(str(template['_key'](node)).lower())

            if t is None:
                t = template['_otherwise']
            template = t

        expanded = []
        # print('T',depth, template)
        # input()
        normal_depth = depth
        after_newline = False
        
        for i, element in enumerate(template):
            if isinstance(element, str):
                if after_newline:
                    if depth:
                        expanded.append(self.offset(depth))
                    after_newline = False
                expanded.append(element)
            elif isinstance(element, Whitespace):
                if element.is_offset:
                    depth += element.count
                    if depth:
                        expanded.append(self.offset(depth))
                    after_newline = False
                else:
                    expanded.append(' ')
            elif isinstance(element, Newline):
                # print(' ',template[i-2] if i >= 2 else '', expanded[-3:])
                if expanded == ['', '\n'] or expanded == ['']:
                    expanded = []
                elif len(expanded) >= 2 and not expanded[-1] and (i >= 2 and isinstance(template[i - 2], Whitespace) and template[i - 2].is_offset) and (not expanded[-2] or expanded[-2][0] == '\n' or expanded[-2][0] == self._symbol):
                    # unrealised fragment, we should swallow that line
                    # sorry sov
                    expanded.pop()
                    if not expanded[-1] or expanded[-1][0] == self._symbol:
                        expanded.pop()
                elif expanded:
                    expanded.append('\n')
                after_newline = True
                depth = normal_depth

            elif hasattr(element, 'expand'):
                expanded.append(element.expand(self, node, depth))
            elif callable(element):
                expanded.append(element(self, node, depth))
            # print(depth,node.type, expanded)
        return ''.join(expanded)

    def _parse_template(self, code, label):
        '''
        Pare smart indented templates

        Takes a template a returns a list of sub-templates, taking in account
        the indentation of the original code based on the first line indentation(0)
        Special treatment of whitespace: returns special Offset and INTERNAL_WHITESPACE, so the generation can be configurable
        It auto detects the indentation width used, as the indent of the first indented line
        >>> indented("""
          def %<code>
            e =
            %<code2>
          """)
        ['def', INTERNAL_WHITESPACE, Placeholder('code', 0), NEWLINE,
          Offset(1),'e', INTERNAL_WHITESPACE, '=', NEWLINE,
          Placeholder('code2', 1), NEWLINE]
        '''
        pass


    def safe_single_except_nl(self, node, indent):
        pass

    def safe_single(self, node, indent):
            pass

    def safe_double(self, node, indent):
        pass

    def binary_left(self, node, indent):
        pass

    def binary_right(self, node, indent):
        pass

    def binary_side(self, field, op):
        pass

    priorities = {
        '**':   11,
        '%':    11,
        '/':    10,
        '*':    10,
        '+':    9,
        '-':    9,
        '>':    8,
        '<':    8,
        '>=':   8,
        '<=':   8,
        '==':   8,
        'and':  7,
        'or':   6,
    }
    def render_type(self, type):
        pass

    def offset(self, depth):
        return self._single_indent * depth

def switch(key, **cases):
    return dict(_key= key, **cases)

