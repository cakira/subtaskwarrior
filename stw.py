#!/bin/env python3
"""
Subtaskwarrior - Subtasks in Taskwarrior

This Python code accepts commands to deal with subtasks, then generates
commands to taskwarrior.
"""

import argparse
import json
import shlex
import subprocess  # nosec (skip bandit's the security check)
import sys


def main():
    args = get_args(sys.argv)
    tasks = get_tasks(args)
    parent_task = next(
        (task for task in tasks if task['id'] == args['filter']), None)
    if parent_task:
        if 'subtasks' in parent_task:
            subtasks = get_subtasks(parent_task, tasks)
            print_subtasks(subtasks, args)


def get_args(argv):
    transform_rc_argument_in_optional_argv_argument(argv)
    parser = argparse.ArgumentParser(
        description='Subtask processing for taskwarrior.',
        argument_default=argparse.SUPPRESS)
    parser.add_argument('-rc')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_tree = subparsers.add_parser('tree', help='Generate tree view')
    parser_tree.set_defaults(command='tree')
    parser_tree.add_argument('filter', type=int, help='filter help')
    args = vars(parser.parse_args(argv[1:]))
    return args


def transform_rc_argument_in_optional_argv_argument(argv):
    rc_elements = [arg for arg in argv if arg.startswith('rc:')]
    if len(rc_elements) > 0:
        i = argv.index(rc_elements[0])
        argv[i:i + 1] = '-rc', rc_elements[0][3:]


def get_tasks(args):
    rc_argument = f'rc:{args["rc"]}' if 'rc' in args else ''
    command = f'task {rc_argument} export'
    process = secure_subprocess_run(command, capture_output=True)
    json_exported_data = process.stdout.decode('UTF-8')
    tasks = json.loads(json_exported_data)
    return tasks


def get_subtasks(parent_task, all_tasks):
    subtasks_uuid = parent_task['subtasks'].split(',')
    subtasks_sub_uuid = [
        '-'.join(uuid.split('-')[1:]) for uuid in subtasks_uuid
    ]
    subtasks = [
        task for task in all_tasks
        if '-'.join(task['uuid'].split('-')[1:]) in subtasks_sub_uuid
    ]
    return subtasks


def print_subtasks(subtasks, args):
    subtasks_id = [task['id'] for task in subtasks]
    subtasks_as_string = ','.join([str(id) for id in subtasks_id])
    rc_argument = f'rc:{args["rc"]}' if 'rc' in args else ''

    command = f'task {rc_argument} {subtasks_as_string}'
    secure_subprocess_run(command, capture_output=False)


def secure_subprocess_run(command, *args, **kwargs):
    command_list = shlex.split(command)
    return subprocess.run(  # nosec (skip bandit's security check)
        command_list,
        check=True,
        *args,
        **kwargs)


if __name__ == "__main__":
    main()
