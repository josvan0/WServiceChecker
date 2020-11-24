class Message:
    INFORMATION = 1
    WARNING = 2
    ERROR = 3

    @staticmethod
    def create(content, type):
        symbol = '?'
        if type == Message.INFORMATION:
            symbol = '#'
        elif type == Message.WARNING:
            symbol = '!'
        elif type == Message.ERROR:
            symbol = '*'
        print(f'[{symbol}] {content}', end='\n\n')


class WServiceCheckerException(Exception):
    def __init__(self, message):
        super().__init__(message)
