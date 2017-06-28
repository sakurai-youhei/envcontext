"""
Context manager for environment variables

Usage:
    os.environ['MYVAR'] = 'oldvalue'

    with EnvironmentContex(MYVAR='myvalue', MYVAR2='myvalue2'):
        print os.getenv('MYVAR')    # Should print myvalue.
        print os.getenv('MYVAR2')    # Should print myvalue2.

    print os.getenv('MYVAR')        # Should print oldvalue.
    print os.getenv('MYVAR2')        # Should print None.
"""

import os


class EnvironmentContext(object):
    def __init__(self, **kwargs):
        self.envs = kwargs

    def __enter__(self):
        self.old_envs = {}
        for k, v in self.envs.items():
            self.old_envs[k] = os.environ.get(k)
            os.environ[k] = v

    def __exit__(self, *args):
        for k, v in self.old_envs.items():
            if v:
                os.environ[k] = v
            else:
                del os.environ[k]