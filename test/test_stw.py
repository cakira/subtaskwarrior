"""
This file runs unit tests over stw.py.

Execute it from the repository root folder with:
`python -m unittest` or `pytest`
You can add the argument '-v' to both commands above to have a verbose output.

pytest have a colored output, but it's necessary to install the tool first
with the command `pip3 install -U pytest`
"""

import unittest

from stw import get_args


class TestSubtaskwarrior(unittest.TestCase):
    """
    Unit tests for the stw.py file.
    """

    def test_get_args_tree_simple(self):
        command_line = 'bin/stw tree 10'
        args = vars(get_args(command_line.split()))
        args_expected = {'filter': 10, 'command': 'tree'}
        self.assertEqual(args_expected, args)

    def test_get_args_tree_with_rc_file(self):
        command_line = 'bin/stw rc:test/data/.taskrc tree 3'
        args = vars(get_args(command_line.split()))
        args_expected = {
            'rc': 'test/data/.taskrc',
            'filter': 3,
            'command': 'tree'
        }
        self.assertEqual(args_expected, args)
