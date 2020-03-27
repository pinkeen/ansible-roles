def decode_ini(
  data,

  sections_skip = False,

  param_path_separator='.',
  param_definition_separator='=',

  value_true='true', 
  value_false='false',
  value_none='',
): 
  while raw_line = next(iter(data.splitlines()), None) is not None:
    pass
    

def encode_ini(
  data, 

  section_main_name=None,
  section_main_only=False,
  section_spacing_lines=1,

  param_path_separator='.',
  param_definition_separator='=', 
  param_definition_separator_spacing=1, 

  list_separate_indices=False,
  list_index_from_one=False,
  list_brace_all=False,
  
  string_quote_char='"',
  string_newline_soft_escape=False,

  value_true='true', 
  value_false='false',
  value_none='',

  comment_prefix='#', 
  comment_prefix_spacing=1,
):
  def emit_section(section_name=None, section_data={}, section_comment_out=False):
    def render_line(line, comment_out=False):
      if comment_out:
        return '%(delimiter)s%(spacing)s%(comment)s' % {
          'delimiter': comment_prefix,
          'comment': line,
          'spacing': ' ' * comment_prefix_spacing
        }

      return line


    def emit_param(param_name, param_value, param_path=[], param_comment_out=False):
      def escape_param_string(value_string):
        if escape_param_string.trans is None:
          chars = ['\\', '\n'];

          if string_quote_char is not None:
            chars += [string_quote_char]
          else:
            chars += ['[', ']']

          mapping = {c: '\\' + c for c in chars}

          if not string_newline_soft_escape:
            mapping['\n'] = r'\n'

          escape_param_string.trans = str.maketrans(mapping)

        return value_string.translate(escape_param_string.trans)

      escape_param_string.trans = None


      def render_scalar(value, nesting_level=0):
        if value is None:
          return value_none;

        if type(value) in [str]:
          value = escape_param_string(value)

          if string_quote_char is not None:
            value = '%(quote)s%(text)s%(quote)s' % {
              'text': value,
              'quote': string_quote_char
            }

          return value

        if type(value) in [int, float]:
          return str(value)
        
        if isinstance(value, bytes):
          return bytes.decode('utf-8')

        if isinstance(value, bool):
          return value_true if value else value_false

        if type(value) in [tuple, list]:
          contents = ', '.join(map(lambda v: render_scalar(v, nesting_level + 1), value))

          if list_brace_all or nesting_level > 0:
            return '[%s]' % contents

          return contents

        raise ValueError('Invalid ini parameter value type: %s' % type(value))


      def render_key(name):
        if isinstance(name, str):
          return name

        if type(name) in [tuple, list]:
          return param_path_separator.join(name)

        raise ValueError('Invalid ini parameter name type: %s' % type(name))


      param_name = render_key(param_name)

      if len(param_name) > 1 and param_name[0] == comment_prefix:
        param_comment_out = True
        param_name = param_name[1:]

      param_key = render_key(param_path + [param_name])

      if isinstance(param_value, dict):
        for subparam_name, subparam_value in param_value.items():
          yield from emit_param(subparam_name, subparam_value, param_path=[param_key], param_comment_out=param_comment_out) 
          
      elif list_separate_indices and type(param_value) in [tuple, list]:
        for i in range(len(param_value)):
          subparam_name = str(i + 1 if list_index_from_one else i)
          yield from emit_param(subparam_name, param_value[i], param_path=[param_key], param_comment_out=param_comment_out)

      elif param_name == '#':
        yield render_line(param_value, comment_out=True)

      elif param_name == '' and param_value == '':
        yield ''

      else:
        param_value = render_scalar(param_value)

        yield render_line(
          '%(name)s%(spacing)s=%(spacing)s%(value)s' % {
            'name': param_key,
            'value': param_value,
            'spacing': ' ' * param_definition_separator_spacing
          },
          comment_out=param_comment_out
        );

        

    if section_name is not None:
      section_name = section_name.strip()

      if not isinstance(section_name, str):
        raise ValueError('Ini section name must be a string')
    
      if len(section_name) == 0:
        raise ValueError('Ini section name must not be empty')

      if section_name[0] == comment_prefix:
        section_comment_out = True
        section_name = section_name[1:]

      yield render_line('[%s]' % section_name, comment_out=section_comment_out)



    if not isinstance(section_data, dict):
      raise ValueError('Ini section data must be a dict')

    for param_name, param_value in section_data.items():
      yield from emit_param(param_name, param_value, param_comment_out=section_comment_out)

    yield from [''] * section_spacing_lines


  def emit_lines(data):
    if not isinstance(data, dict):
      raise ValueError('Ini data must be dict')

    if section_main_only:
      yield from emit_section(section_main_name, data) 
      return

    section_keys = [key for key in data.keys() if isinstance(data[key], dict)]
    bare_params = {k: v for (k, v) in data.items() if k not in section_keys}
    
    yield from emit_section(section_main_name, bare_params)

    for section_key in section_keys:
      yield from emit_section(section_key, data[section_key]) 

  parts = map(lambda l: l + '\n', emit_lines(data))

  return ''.join(parts)


class FilterModule(object):
    def filters(self):
        return {
            'from_ini': decode_ini,
            'to_ini': encode_ini
        }

print(encode_ini({
      'somevar': 'aaa',
      '#': 'someint is nice and all',
      '#someint': 34,
      'somelist': ['a', 'b', 'dupa', 42, 'elo'],
      'nestedlist': ['one', 'two', ['es[c]ape', ['meee', 'ccc[c]har']]],
      'multiline': 'First line\n2nd one\n      ... and the third one!',
      'section_a': {
        'in_section': 'val',
        'nested': {
          'sub_key_1': [1, 2, 3],
          'sub_key_2': {
            'magic': 'number?',
            '#deep': {
              'deepes_shit': 'really deep',
              'all': 'or not all'
            },
            '#': 'And the last nested one comes next...',
            'after': 'works?'
          }
        },
        'moar': 3434
      },
      'truish': True,
      'list_of_lists': [
        ["oneone", "onetwo"],
        ["twoone", "twotwo"]
      ],
      'NULL': None,
      '#section_b': {
        'falsish': False,
        'bools': (True, False, False, True)
      },
      'escape_my_quotes':  r'This is some "thing", and it works, "nested \"escapes\"" shall work' 
}))