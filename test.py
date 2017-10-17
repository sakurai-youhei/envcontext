'''
Created on 2017/10/16

@author: sakurai
'''
from itertools import islice
from os import environ
from os import getenv as os_getenv
from os import name as osname
from random import choice
from random import randint
from random import sample
from string import ascii_letters
from string import digits
from string import punctuation
from subprocess import check_output
from sys import version_info
from unittest import main
from unittest import TestCase
from unittest import skipIf
from uuid import uuid4

from envcontext import EnvironmentContext as EnvContext


WINSHELL_UNREWRITABLE_ENVS = (
    "COMMONPROGRAMFILES",
    "PROGRAMFILES",
    "PROMPT",
    "PATHEXT",
)


def quickfuzzer(MAX_LENGTH=16):
    printable_wo_space = ascii_letters + digits + punctuation
    while True:
        yield "".join(sample(printable_wo_space, randint(0, MAX_LENGTH)))


def is_invalid_key(key):
    return key == "" or "=" in key


def subshell_getenv(key, default=None):
    key_bin = key.encode("ascii", errors="ignore")
    if osname == "nt":
        key_bin = key_bin.upper()
        output = check_output("set", shell=True)
    else:
        output = check_output("printenv", shell=True)

    for line in output.splitlines():
        k, _, v = line.partition(b"=")
        if k == key_bin:
            return v.decode("ascii", errors="ignore")
    else:
        return default


class EnvContextFuzzingTest(TestCase):
    def setUp(self):
        self.fuzzer = quickfuzzer()
        self.num_keys = len(environ)

    def tearDown(self):
        self.assertEqual(len(environ), self.num_keys)

    def assertEnvContext(self, k_add, v_add, k_update, v_update, func_getenv):
        if func_getenv(k_add):
            # k_add exists accidentally
            return
        elif is_invalid_key(k_add):
            # k_add is invalid accidentally
            return

        v_original = func_getenv(k_update)

        params = {k_add: v_add, k_update: v_update}
        with EnvContext(**params):
            self.assertEqual(v_add, func_getenv(k_add),
                             "%r is not added, %r" % (k_add, params))
            self.assertEqual(v_update, func_getenv(k_update),
                             "%r is not updated, %r" % (k_update, params))

        self.assertIsNone(func_getenv(k_add),
                          "%r still exists, %r" % (k_add, params))
        self.assertEqual(v_original, func_getenv(k_update),
                         "%r is not reverted, %r" % (k_update, params))

    def test_environ(self, N=10000):
        keys = tuple(environ)
        for _ in range(N):
            key_add, value_add = islice(self.fuzzer, 2)
            key_update, value_update = choice(keys), next(self.fuzzer)

            self.assertEnvContext(key_add, value_add,
                                  key_update, value_update,
                                  environ.get)

    def test_getenv(self, N=10000):
        keys = tuple(environ)
        for _ in range(N):
            key_add, value_add = islice(self.fuzzer, 2)
            key_update, value_update = choice(keys), next(self.fuzzer)

            self.assertEnvContext(key_add, value_add,
                                  key_update, value_update,
                                  os_getenv)

    @skipIf(version_info[0] == 2, "Test won't pass due to no replication of "
            "environmental variables to child process by subprocess module.")
    def test_subshell(self, N=100):
        keys = tuple(environ)
        for _ in range(N):
            key_add, value_add = islice(self.fuzzer, 2)
            key_update, value_update = choice(keys), next(self.fuzzer)

            if key_update in WINSHELL_UNREWRITABLE_ENVS + ("COMSPEC", ):
                # Windows-specific corner cases making test fail.
                continue
            elif "" in (value_add, value_update):
                # Empty environmental variable becomes invisible in subprocess.
                continue

            self.assertEnvContext(key_add, value_add,
                                  key_update, value_update,
                                  subshell_getenv)


class EnvContextUseCasesTest(TestCase):
    """TODO(YSA): Rewrite to smarter code"""
    def test_multiple_usage(self, N=10):
        original = os_getenv("MYVAR")
        envcontext = EnvContext(MYVAR="multiple_usage")
        for _ in range(N):
            with envcontext:
                self.assertNotEqual(original, os_getenv("MYVAR"))
            self.assertEqual(original, os_getenv("MYVAR"))

    def test_nested_usage(self, N=10):
        original = os_getenv("MYVAR")
        envcontext = EnvContext(MYVAR="nested_usage")

        def f(N):
            if N == 0:
                self.assertNotEqual(original, os_getenv("MYVAR"))
            else:
                with envcontext:
                    f(N-1)
                self.assertEqual(original, os_getenv("MYVAR"))
        f(N)

    def test_combined_usage(self, N=10):
        original = os_getenv("MYVAR")
        with EnvContext(MYVAR="usage1"):
            with EnvContext(MYVAR="usage2"):
                self.assertEqual("usage2", os_getenv("MYVAR"))
            self.assertEqual("usage1", os_getenv("MYVAR"))
        self.assertEqual(original, os_getenv("MYVAR"))

    def test_add_empty_variable(self):
        original = os_getenv("MYVAR")
        envcontext = EnvContext(MYVAR="")
        with envcontext:
            self.assertNotEqual(original, os_getenv("MYVAR"))
        self.assertEqual(original, os_getenv("MYVAR"))

    def test_add_new_variable(self):
        uniqvar = ""
        while not uniqvar:
            candidate = str(uuid4()).upper()
            if candidate not in environ:
                uniqvar = candidate
                break

        params = {uniqvar: uniqvar}
        with EnvContext(**params):
            self.assertEqual(uniqvar, os_getenv(uniqvar))
        self.assertIsNone(os_getenv(uniqvar))


if __name__ == "__main__":
    main(verbosity=2)
