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
  param_value_sep_char='.',
  ruler_char='-',
  align='center',
  trim_leading=False, 
  trim_trailing=True,
  width=None,
  width_max=DEFAULT_WIDTH
):
  def line_extra_len():
    return (0
      + padding_left 
      + padding_right 
      + (1 if frame_left else 0)
      + (1 if frame_right else 0)
    )

  text_lines = trimmed(
    text=text,
    as_list=True,
    leading=trim_leading,
    trailing=trim_trailing
  )

  if width is None:
    width = max(map(len, text_lines))
    width_max -= line_extra_len()

  if width > width_max:
    width = width_max

  content_width = width - line_extra_len()
  
  text_lines = wrapped(
    text=text_lines,
    as_list=True,
    width=content_width
  )

  text_lines = aligned(
    text=text_lines,
    align=align,
    width=content_width,
    as_list=True
  )

  if param_value_sep_char is not None:
    # The first attempt:
    #   (?P<name>([^.]+\.{0,2})+) 
    #   \s\.{3,}\s
    #   (?P<value>([^.]+\.{0,2})+)
    # ...caused catasthropic backtracking 😅,
    # so had to resort to lookaheads 🤷‍♂️.
    re_param_value = re.compile(''
      + '^(?P<name>[^.]+|[^\s].+)+\s+\.{3,}\s+(?P<value>.*)'
    )

    print(re_param_value.pattern)

  if ruler_char is not None:
    re_ruler = re.compile(''
      + '^\s*'
      + '(' + re.escape(ruler_char) + '){3,}'
      + '\s*$'
    )

  def process_line(line=''):
    if ruler_char is not None and re_ruler.match(line):
      return ([]
        + frame_line()
        + frame_line(ruler_char * content_width)
        + frame_line()
      )

    if param_value_sep_char is not None:
      print("before match", line)
      param_value_match = re_param_value.match(line)

      if param_value_match:
        print("matches", line)
        param_name = param_value_match.group('name')
        param_value = param_value_match.group('value')
        sep_width = (
          content_width 
          - len(param_name) 
          - len(param_value) 
          - 2
        )

        line = '%s %s %s' % (
          param_name,
          param_value_sep_char * sep_width,
          param_value,
        )
      else:
        print("no match", line)
    

    return frame_line(line)


  def frame_line(line=''):
    return [str.join('', (
      frame_char if frame_left else '',
      ' ' * padding_left,
      line + ' ' * (content_width - len(line)),
      ' ' * padding_right,
      frame_char if frame_right else '',
    ))]

  def horiz_frame():
    return frame_char * width

  banner_lines = []
  banner_lines += [horiz_frame()] if frame_top else []
  banner_lines += [frame_line()] * padding_top
  banner_lines += list(map(process_line, text_lines))
  banner_lines += [frame_line()] * padding_top
  banner_lines += [horiz_frame()] if frame_bottom else []

  return str.join('\n', flatten_line_lists(banner_lines))

# print(banner(width=45, align='center', text="ERROR!!!"))
# print(banner(width=45, align='right', frame_top=False, text='To jest tytuł\n\nA to jest bardzo, ale to bardzo długa \n -----   \n linia dłuzsza nawet niz 80 znaków i tak dalej\n a to jest juz krotsza linia'))

import time


def t(s):
  start = time.time()
  m = re.match('^(?P<name>.*(?!\.{3,}))\s+\.{3,}\s+(?P<value>.*(?!\.{3,}))$', s)
  took = time.time() - start

  if m:
    print('[MATCH]', "[%.2fs]" % took, s, ' | ', m.group('name'), '=', m.group('value'))
  else:
    print('[NO]',"[%.2fs]" % took, s)

t(' this...is.a complicated   param-name ...    and its value!  ')
t('simple.param.name ... 34')
t('spaced param  name ... 56')
t('  spaced .. param . name ...... 56')
t('  spaced.. name ... 56')
t('  spaced.. name ...56')
t('  spaced.. name ...56 ......elo')
t('param ....... elo value ..... another one')
t('                           To jest tytuł')