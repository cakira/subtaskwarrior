"""
This file runs unit tests over stw.py.

Execute it from the repository root folder with:
`python -m unittest` or `pytest`
You can add the argument '-v' to both commands above to have a verbose output.

pytest have a colored output, but it's necessary to install the tool first
with the command `pip3 install -U pytest`
"""

import unittest


class TestSubtaskwarrior(unittest.TestCase):
    """
    Unit tests for the stw.py file.
    """
