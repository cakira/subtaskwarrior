"""
This file runs unit tests over stw.py.

Execute it from the repository root folder with:
`python -m unittest` or `pytest`
You can add the argument '-v' to both commands above to have a verbose output.

pytest have a colored output, but it's necessary to install the tool first
with the command `pip3 install -U pytest`
"""

import json
import subprocess
import unittest
from unittest import mock

from stw import get_args, get_tasks

EXAMPLE_TASKS = [{
    "id": 1,
    "description": "Task 1",
    "entry": "20220515T044432Z",
    "modified": "20220515T044432Z",
    "status": "pending",
    "uuid": "d40c36ae-855f-4e12-b785-fc7b445863e5",
    "urgency": 0.0547945
}, {
    "id": 2,
    "description": "Task 2",
    "entry": "20220515T044437Z",
    "modified": "20220515T044437Z",
    "status": "pending",
    "uuid": "7e9b7fcb-12d0-4574-a36a-b58d2cd98d29",
    "urgency": 0.0547945
}, {
    "id": 3,
    "description": "Parent task",
    "entry": "20220515T044458Z",
    "modified": "20220515T050552Z",
    "status": "pending",
    "subtasks":
    "61508f-8d22-498b-90b0-b116a42dfb7a,09a2a6-54d6-48cc-b3ca-54bbea599423",
    "uuid": "3f000090-6e51-4ab2-811e-dadc49e4c68c",
    "urgency": 0.0547945
}, {
    "id": 4,
    "description": "subtask 1",
    "entry": "20220515T044521Z",
    "modified": "20220515T044521Z",
    "status": "pending",
    "uuid": "d961508f-8d22-498b-90b0-b116a42dfb7a",
    "urgency": 0.0547945
}, {
    "id": 5,
    "description": "subtask 2",
    "entry": "20220515T044528Z",
    "modified": "20220515T044528Z",
    "status": "pending",
    "uuid": "a309a2a6-54d6-48cc-b3ca-54bbea599423",
    "urgency": 0.0547945
}]


class TestSubtaskwarrior(unittest.TestCase):
    """
    Unit tests for the stw.py file.
    """

    def test_get_args_tree_simple(self):
        command_line = 'bin/stw tree 10'
        args = get_args(command_line.split())
        args_expected = {'filter': 10, 'command': 'tree'}
        self.assertEqual(args_expected, args)

    def test_get_args_tree_with_rc_file(self):
        command_line = 'bin/stw rc:test/data/.taskrc tree 3'
        args = get_args(command_line.split())
        args_expected = {
            'rc': 'test/data/.taskrc',
            'filter': 3,
            'command': 'tree'
        }
        self.assertEqual(args_expected, args)

    @mock.patch('stw.subprocess')
    def test_get_tasks_simple(self, mock_subprocess):
        tasks_data = EXAMPLE_TASKS
        json_mock = json.dumps(tasks_data).encode('UTF-8')
        mock_subprocess.run.return_value = subprocess.CompletedProcess(
            args='', returncode=0, stdout=json_mock)
        tasks = get_tasks({})
        subprocess_mock_method_calls_expected = [
            mock.call.run(['task', 'export'], check=True, capture_output=True)
        ]
        self.assertEqual(subprocess_mock_method_calls_expected,
                         mock_subprocess.method_calls)
        self.assertEqual(tasks_data, tasks)

    @mock.patch('stw.subprocess')
    def test_get_tasks_with_rc_file(self, mock_subprocess):
        tasks_data = EXAMPLE_TASKS
        args = {'rc': 'test/data/.taskrc', 'filter': 3, 'command': 'tree'}
        json_mock = json.dumps(tasks_data).encode('UTF-8')
        mock_subprocess.run.return_value = subprocess.CompletedProcess(
            args='', returncode=0, stdout=json_mock)
        tasks = get_tasks(args)
        subprocess_mock_method_calls_expected = [
            mock.call.run(['task', 'rc:test/data/.taskrc', 'export'],
                          check=True,
                          capture_output=True)
        ]
        self.assertEqual(subprocess_mock_method_calls_expected,
                         mock_subprocess.method_calls)
        self.assertEqual(tasks_data, tasks)
