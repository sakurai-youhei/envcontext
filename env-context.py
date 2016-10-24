"""Context manager for environment variables.

Usage:
    os.environ['MYVAR'] = 'oldvalue'

    with EnvironmentVariable('MYVAR', 'myvalue'):
        print os.getenv('MYVAR')    # Should print myvalue.

    print os.getenv('MYVAR')        # Should print oldvalue.
"""

import os

class EnvironmentVariable(object):
    """Context manager for creating a temporary environment variable.
    """
    def __init__(self, key, value):
        """Contructor.

        Args:
            key - Environment variable name.
            value - Value to set in environment variable.
        """
        self.key = key
        self.newValue = value

    def __enter__(self):
        """Sets the environment variable and saves the old value.
        """
        self.oldValue = os.environ.get(self.key)
        os.environ[self.key] = self.newValue

    def __exit__(self, *args):
        """Sets the environment variable back to the way it was before.
        """
        if self.oldValue:
            os.environ[self.key] = self.oldValue
        else:
            del os.environ[self.key]