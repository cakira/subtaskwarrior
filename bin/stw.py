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
    args = get_args()
    tasks = get_tasks(args)
    parent_task = next((task for task in tasks if task['id'] == args.filter),
                       None)
    if parent_task:
        if 'subtasks' in parent_task:
            subtasks = get_subtasks(parent_task, tasks)
            print_subtasks(subtasks, args)


def get_args():
    transform_rc_argument_in_optional_argv_argument()
    parser = argparse.ArgumentParser(
        description='Subtask processing for taskwarrior.')
    parser.add_argument('-rc')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_tree = subparsers.add_parser('tree', help='Generate tree view')
    parser_tree.set_defaults(command='tree')
    parser_tree.add_argument('filter', type=int, help='filter help')
    args = parser.parse_args()
    return args


def transform_rc_argument_in_optional_argv_argument():
    rc_elements = [arg for arg in sys.argv if arg.startswith('rc:')]
    if len(rc_elements) > 0:
        i = sys.argv.index(rc_elements[0])
        sys.argv[i:i + 1] = '-rc', rc_elements[0][3:]


def get_tasks(args):
    rc_argument = f'rc:{args.rc}' if args.rc else ''
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
    rc_argument = f'rc:{args.rc}' if args.rc else ''

    command = f'task {rc_argument} {subtasks_as_string}'
    if has_script_command():
        full_command = f'script -q -c "{command}"'
    else:
        full_command = command
    process = secure_subprocess_run(full_command, capture_output=True)
    print(process.stdout.decode('UTF-8'))


def has_script_command():
    try:
        secure_subprocess_run('script --version', stdout=subprocess.PIPE)
        script_command_exists = True
    except FileNotFoundError:
        script_command_exists = False
    return script_command_exists


def secure_subprocess_run(command, *args, **kwargs):
    command_list = shlex.split(command)
    return subprocess.run(  # nosec (skip bandit's security check)
        command_list,
        check=True,
        *args,
        **kwargs)


if __name__ == "__main__":
    main()
