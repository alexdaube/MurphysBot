class MessageFormatter(object):
    @staticmethod
    def get_message(message):
        if not isinstance(message, tuple):
            message = ('default', message)
        return '<span style=\" color:{0};\" > {1} </span>'.format(
            MessageFormatter._configure_color(message[0].lower()), message[1])

    @staticmethod
    def _configure_color(color):
        color_hex = "#"
        if color == 'info':
            color_hex += '21c521'  # green
        elif color == 'warning':
            color_hex += 'bcc701'  # yellow
        elif color == 'debug':
            color_hex += '00abff'  # light blue
        elif color == 'error':
            color_hex += 'f91f1f'  # red
        elif color == 'critical':
            color_hex += '8d0b0b'  # dark red
        else:
            color_hex += '0a0b02'  # black
        return color_hex
