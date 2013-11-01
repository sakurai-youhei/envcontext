from contextlib import contextmanager

@contextmanager
def env_var(key, value):
    os.environ[key] = value
    yield
    del os.environ[key]