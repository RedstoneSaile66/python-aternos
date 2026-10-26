#!/usr/bin/env python3

import unittest
import sys

from python_aternos import atjsparse
from tests import files


class TestJsNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if isinstance(atjsparse.js, atjsparse.NodeInterpreter):
            cls.js = atjsparse.js
        else:
            try:
                cls.js = atjsparse.NodeInterpreter()
            except (OSError, RuntimeError) as err:
                raise unittest.SkipTest(
                    f'Unable to start NodeJS interpreter: {err}'
                ) from err

    def test_default_interpreter(self) -> None:
        expected = (
            atjsparse.NodeInterpreter
            if sys.version_info >= (3, 12)
            else atjsparse.Js2PyInterpreter
        )
        self.assertIs(atjsparse.default_interpreter(), expected)

    def test_exec(self) -> None:
        self.tests = files.read_sample('token_input.txt')
        self.results = files.read_sample('token_output.txt')

        for func, exp in zip(self.tests, self.results):
            self.__class__.js.exec_js(func)
            res = self.__class__.js['AJAX_TOKEN']
            self.assertEqual(res, exp)


if __name__ == '__main__':
    unittest.main()
