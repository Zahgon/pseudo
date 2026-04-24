import re
from code_generator_dsl import Placeholder, Newline, Offset, INTERNAL_WHITESPACE, Action, Function, SubTemplate
import yaml

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

s = '''
        def %<name>(%<args:join ','>):
            %<#body>
    '''
# print(yaml.dump(_parse_template(2, s, 'module')))