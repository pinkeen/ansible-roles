from pinkeen import text

class TextFilterModule(AbstractFilterModule):
    FILTER_NAME_PREFIX = 'text_'
    FILTER_FUNC_PREFIX = 'do_'
    LINE_WIDTH = 80

    @staticmethod
    def do_wrap(text, width=TextFilterModule.LINE_WIDTH):
        return text.wrapped(
          text=text,
          indicate_breaks=False,
          break_on_hyphens=True,
          width=width
        )

    @staticmethod
    def do_wrap_markup(text, width=TextFilterModule.LINE_WIDTH):
      return text.wrapped(
        text=text, 
        indicate_breaks=True,
        break_on_hyphens=False, 
        width=width
      )

    @staticmethod
    def do_align(text, align=None, width_max=TextFilterModule.LINE_WIDTH, width=None):
        return text.aligned(text, align=align, width=width, width_max=width_max)

    @staticmethod
    def do_align_center(text, width=TextFilterModule.LINE_WIDTH):
        return TextFilterModule.do_align(text, 'center', width)

    @staticmethod
    def do_align_left(text, width=TextFilterModule.LINE_WIDTH):
        return TextFilterModule.do_align(text, 'left', width)

    @staticmethod
    def do_align_right(text, width=TextFilterModule.LINE_WIDTH):
        return TextFilterModule.do_align(text, 'right', width)

    @staticmethod
    def do_trim(text, leading=True, trailing=True):
      return text.trimmed(
        text=text, 
        leading=True,
        trailing=True
      )

    @staticmethod
    def do_justify(text, width=TextFilterModule.LINE_WIDTH):
        return text.justified(text=text, width=width)

    @staticmethod
    def do_render_ruler(*args, **kwargs):
        return text.ruler(*args, **kwargs)

    @staticmethod
    def do_render_banner(*args, **kwargs):
        return text.banner(*args, **kwargs)