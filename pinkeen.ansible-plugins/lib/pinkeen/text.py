import math
import textwrap
import re

DEFAULT_WIDTH=80

def flatten_line_lists(lines):
  flattened = []

  for sublines in lines:
    if isinstance(sublines, str):
      flattened.append(sublines)
    else:
      flattened.extend(list(sublines))

  return flattened

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

    width = width - 2 if indicate_breaks else width

    text_lines = text if isinstance(text, list) else text.splitlines(keepends=False)
    text_lines = flatten_line_lists(map(wrap_line, text_lines))
    return list(text_lines) if as_list else '\n'.join(text_lines)


def wrap_markup(
    text='', 
    as_list=False, 
    width=DEFAULT_WIDTH
):
    return wrapped(
      text=text, 
      as_list=as_list, 
      indicate_breaks=True,
      break_on_hyphens=False, 
      width=width
    )


def trimmed(
  text='',
  as_list=False,
  leading=True,
  trailing=True
):
  def strip_line(line):
    if leading: line = line.lstrip()
    if trailing: line = line.rstrip()
    return line

  text_lines = text if isinstance(text, list) else text.splitlines(keepends=False)
  text_lines = map(strip_line, text_lines)

  return list(text_lines) if as_list else '\n'.join(text_lines)


def aligned(
  text='', 
  align='center',
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
    

  text_lines = text if isinstance(text, list) else text.splitlines(keepends=False)

  if width is None:
    width = max(map(len, text_lines))
  
  if width_max is not None and width > width_max:
    width = width_max

  text_lines = map(align_line, text_lines)

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
  align='center',
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

      if expander_char is not None and re_expander.search(line):
        elements = re_expander.split(line)
        elements_width = sum(map(len, elements))
        expander_count = len(elements) - 1
        expander_width = math.ceil((content_width - elements_width) / expander_count)
        expander_width_fix = content_width - (elements_width + expander_width * expander_count)
        expander_width_odd = expander_width + expander_width_fix

        line = str.join(
          expander_char * expander_width_odd,
          [
            elements[0],
            str.join(expander_char * expander_width, elements[1:])
          ]
        );

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


  if expander_char is not None:
    re_expander = re.compile('\.{4,}')

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

print(banner(width=45, align='center', text="ERROR!!!"))
print(banner(width=45, align='right', frame_top=False, text='To jest tytuł\n\nA to jest bardzo, ale to bardzo długa \n -----   \n linia dłuzsza nawet niz 80 znaków i tak dalej\n a to jest juz krotsza linia'))

print(banner(width=45, align='right', frame_top=False, text=' Cośtam .... 45'))
print(banner(width=45, align='right', frame_top=False, text=' Cośtam .... 45 .... dłuszy .... elo'))
print(banner(width=45, align='right', frame_top=False, text=' Cośtam .... 1 .... 2 .... 3 .... 42'))
print(banner(width=45, align='right', frame_top=False, text=' .... 3 .... 42'))
print(banner(width=45, align='right', frame_top=False, text='....42'))
print(banner(width=45, align='right', frame_top=False, text='5.... '))


