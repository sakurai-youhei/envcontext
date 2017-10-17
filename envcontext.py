"""
Usage:
    os.environ['MYVAR'] = 'oldvalue'

    with EnvironmentContex(MYVAR='myvalue', MYVAR2='myvalue2'):
        print(os.getenv('MYVAR'))  # Should print myvalue.
        print(os.getenv('MYVAR2'))  # Should print myvalue2.

    print(os.getenv('MYVAR'))  # Should print oldvalue.
    print(os.getenv('MYVAR2'))  # Should print None.
"""

from os import environ


class EnvironmentContext(object):
    """Context manager to update environment variables with preservation"""
    def __init__(self, **kwargs):
        self.envs = kwargs
        self.preservation = {}

    def __enter__(self):
        for k in self.envs:
            if k not in self.preservation:
                self.preservation[k] = environ.get(k)
            environ[k] = self.envs[k]

    def __exit__(self, *_):
        for k in self.preservation:
            if self.preservation[k]:
                environ[k] = self.preservation[k]
            else:
                environ.pop(k, None)
