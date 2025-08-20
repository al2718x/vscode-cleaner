#!/usr/bin/python3
import appdirs
import argparse
import os
import re
import shutil
import json

if __name__ == '__main__':
    def rmrf(directory):
        if not os.path.isdir(directory):
            print(f'"{directory}" does not exist')
            return
        print(f' rm -rf {directory}', end=' ... ')
        if dry_run:
            print('dry run')
        else:
            shutil.rmtree(directory, ignore_errors=True)
            print('DONE')

    parser = argparse.ArgumentParser(description='Clean vscode cache')
    parser.add_argument('-d', '--dry', action='store_true', help='Dry run')
    parser.add_argument('-w', '--wet', action='store_true', help='Wet run (remove files)')
    parser.add_argument('-v', '--vscode', type=str, help='VSCode config directory')
    args = parser.parse_args()
    if not args.wet and not args.dry:
        parser.print_help()
        exit(0)
    dry_run = not args.wet

    dir_config = args.vscode if args.vscode else appdirs.user_config_dir('VSCodium')
    if not os.path.isdir(dir_config):
        print(f'"{dir_config}" does not exist')
        exit(1)

    rmrf(f'{dir_config}/Cache')
    rmrf(f'{dir_config}/CachedData')
    rmrf(f'{dir_config}/CachedExtensionVSIXs')

    dir_workspace_storage = f'{dir_config}/User/workspaceStorage'
    for file in os.listdir(dir_workspace_storage):
        filename = os.fsdecode(file)
        dir_inner = f'{dir_workspace_storage}/{filename}'
        file_workspace = f'{dir_inner}/workspace.json'
        if os.path.isfile(file_workspace):
            # print(file_workspace)
            f = open(file_workspace, 'r')
            for line in f:
                remove = False

                search_result = re.search(r'"workspace": "file://(.*?)"', line)
                if search_result is not None:
                    found_name = search_result.group(1)
                    is_exists = os.path.exists(found_name)
                    print('[w]', '[+]' if is_exists else '[ ]', found_name)
                    if not is_exists:
                        rmrf(dir_inner)

                search_result = re.search(r'"folder": "file://(.*?)"', line)
                if search_result is not None:
                    found_name = search_result.group(1)
                    is_exists = os.path.exists(found_name)
                    print('[f]', '[+]' if is_exists else '[ ]', found_name)
                    if not is_exists:
                        rmrf(dir_inner)

    dir_history = f'{dir_config}/User/History'
    for file in os.listdir(dir_history):
        filename = os.fsdecode(file)
        dir_inner = f'{dir_history}/{filename}'
        file_entries = f'{dir_inner}/entries.json'
        if os.path.isfile(file_entries):
            # print(file_entries)
            f = open(file_entries, 'r')
            entries_j = json.load(f)
            line = entries_j['resource'] if 'resource' in entries_j else ''
            match_result = re.match(r'file://(.*)', line)
            if match_result:
                found_name = match_result.group(1)
                is_exists = os.path.isfile(found_name)
                print('[h]', '[+]' if is_exists else '[ ]', found_name)
                if not is_exists:
                    rmrf(dir_inner)
