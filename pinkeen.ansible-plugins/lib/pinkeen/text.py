import math
import textwrap
import re


DEFAULT_WIDTH=80

def split_lines(text):
  return text if isinstance(text, list) else text.splitlines(keepends=False)

def ruler(
  char='-', 
  padding_char=' ',
  padding_left=0,
  padding_right=0, 
  margin_top=1, 
  margin_bottom=1, 
  width=DEFAULT_WIDTH
):
  ruler_width = width - padding_left - padding_right

  return ''.join((
      '\n' * margin_top,
      padding_char * padding_left,
      char * ruler_width,
      padding_char * padding_right,
      '\n',
      '\n' * margin_bottom,
  ))


def wrapped(
  text='', 
  as_list=False, 
  indicate_breaks=False, 
  break_on_hyphens=True, 
  width=DEFAULT_WIDTH
):
    def add_break_indicator(wrapped_lines):
      if indicate_breaks and len(wrapped_lines) > 1:
        wrapped_lines[0] = wrapped_lines[0] + '↩'
        wrapped_lines[1:-1] = map(lambda wrap: '↪%s↩' % wrap, wrapped_lines[1:-1])
        wrapped_lines[-1] = '↪' + wrapped_lines[-1]

      return wrapped_lines
    
    def wrap_line(original_line):
      return add_break_indicator(textwrap.wrap(
        text=original_line, 
        width=width,
        break_on_hyphens=break_on_hyphens,
        replace_whitespace=False, 
        drop_whitespace=False
      ))

    def flatten_line_lists(lines):
      flattened = []

      for sublines in lines:
        if isinstance(sublines, str):
          flattened.append(sublines)
        else:
          flattened.extend(list(sublines))

      return flattened

    width = width - 2 if indicate_breaks else width

    text_lines = split_lines(text)
    text_lines = flatten_line_lists(map(wrap_line, text_lines))

    return list(text_lines) if as_list else '\n'.join(text_lines)


def trimmed(
  text='',
  as_list=False,
  leading=True,
  trailing=True
):
  text_lines = split_lines(text)

  content_lines = list(filter(lambda line: len(line.strip()), text_lines))

  if leading:
    leading_whitespace = min(map(lambda line: len(line) - len(line.lstrip()), content_lines))
    text_lines = list(map(lambda line: line[leading_whitespace:], text_lines))

  if trailing:
    trailing_whitespace = min(map(lambda line: len(line) - len(line.rstrip()), content_lines))
    text_lines = list(map(lambda line: line[-trailing_whitespace:], text_lines))

  return list(text_lines) if as_list else '\n'.join(text_lines)

def stripped(
  text='',
  as_list=False,
  leading=True,
  trailing=True
): pass

def aligned(
  text='', 
  align='left',
  width=None,
  width_max=None,
  as_list=False
): 
  def align_line(line):
    pad_len = width - len(line)

    if align == 'right':
      return ' ' * pad_len + line
    
    if align == 'center':
      return ' ' * math.ceil(pad_len / 2) + line

    return line

  text_lines = split_lines(text)

  if align == 'left':
    leading_whitespace = min(map(lambda line: len(line) - len(line.lstrip()), text_lines))
    text_lines = list(map(lambda line: line[leading_whitespace:], text_lines))

  if align == 'right':
    trailing_whitespace = min(map(lambda line: len(line) - len(line.rstrip()), text_lines))
    text_lines = list(map(lambda line: line[-trailing_whitespace:], text_lines))

  if width is None:
    width = max(map(len, text_lines))
  
  if width_max is not None and width > width_max:
    width = width_max

  text_lines = map(align_line, text_lines)

  return list(text_lines) if as_list else '\n'.join(text_lines)

def justified(
  text, 
  separator_char=' ',
  separator_pattern=None, 
  as_list=False,
  width=DEFAULT_WIDTH
):
  def justify_line(line):
    if not re_separator.search(line):
      return line

    elements = re_separator.split(line)
    elements_width = sum(map(len, elements))
    separator_count = len(elements) - 1
    separator_width = math.ceil((width - elements_width) / separator_count)
    separator_width_fix = width - (elements_width + separator_width * separator_count)
    separator_width_odd = separator_width + separator_width_fix

    return str.join(
      separator_char * separator_width_odd,
      [
        elements[0],
        str.join(separator_char * separator_width, elements[1:])
      ]
    );
  
  if separator_pattern is None:
    separator_pattern = '%s+' % re.escape(separator_char)

  re_separator = re.compile(separator_pattern)

  text_lines = split_lines(text)
  text_lines = map(justify_line, text_lines)

  return list(text_lines) if as_list else '\n'.join(text_lines)


def banner(
  text='', 
  padding_top=1,
  padding_bottom=1,
  padding_left=2, 
  padding_right=2,
  padding_char=' ',
  frame_char='#', 
  frame_left=True, 
  frame_right=True, 
  frame_top=True, 
  frame_bottom=True, 
  expander_char='.',
  ruler_char='-',
  align='left',
  trim_leading=False, 
  trim_trailing=True,
  width=None,
  width_max=DEFAULT_WIDTH
):
  def render_content(content_lines):
    for line in content_lines:
      if ruler_char is not None and re_ruler.match(line):
        yield ''
        yield ruler_char * content_width
        yield ''
        continue

      if expander_char:
        line = justified(
          text=line, 
          separator_char=expander_char, 
          separator_pattern='%s{4,}' % re.escape(expander_char),
          width=content_width
        )

      yield line


  def frame_line(line=''):
    return str.join('', (
      frame_char if frame_left else '',
      ' ' * padding_left,
      line + ' ' * (content_width - len(line)),
      ' ' * padding_right,
      frame_char if frame_right else '',
    ))


  def frame_bar():
    return frame_char * width

  if ruler_char is not None:
    re_ruler = re.compile(''
      + '^\s*'
      + '(' + re.escape(ruler_char) + '){4,}'
      + '\s*$'
    )

  text_lines = trimmed(
    text=text,
    as_list=True,
    leading=trim_leading,
    trailing=trim_trailing
  )

  decorators_width = (
    + padding_left 
    + padding_right 
    + (1 if frame_left else 0)
    + (1 if frame_right else 0)
  )

  if width is None:
    width = max(map(len, text_lines))
    width_max -= decorators_width

  if width > width_max:
    width = width_max

  content_width = width - decorators_width
  
  text_lines = wrapped(
    text=text_lines,
    as_list=True,
    width=content_width
  )

  text_lines = list(render_content(text_lines))

  text_lines = aligned(
    text=text_lines,
    align=align,
    width=content_width,
    as_list=True
  )

  banner_lines = []
  banner_lines += [frame_bar()] if frame_top else []
  banner_lines += [frame_line('')] * padding_top
  banner_lines += list(map(frame_line, text_lines))
  banner_lines += [frame_line('')] * padding_top
  banner_lines += [frame_bar()] if frame_bottom else []

  return str.join('\n', banner_lines)




a = """
    elo....ziomalu co tam elo
    def flatten_line_lists(lines):
      flattened = []

      for sublines in lines:
        if isinstance(sublines, str):
          flattened.append(sublines)
        else:
          flattened.extend(list(sublines))

      return flattened
"""

# print(banner(a, width=40))
print(trimmed(a))