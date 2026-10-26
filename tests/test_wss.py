#!/usr/bin/env python3

import unittest
from typing import Any

from python_aternos.atwss import _headers_argument


def legacy_connect(*, extra_headers: Any) -> None:
    pass


def current_connect(*, additional_headers: Any) -> None:
    pass


class TestWebsocketCompatibility(unittest.TestCase):

    def test_legacy_header_keyword(self) -> None:
        self.assertEqual(_headers_argument(legacy_connect), 'extra_headers')

    def test_current_header_keyword(self) -> None:
        self.assertEqual(
            _headers_argument(current_connect),
            'additional_headers',
        )


if __name__ == '__main__':
    unittest.main()
