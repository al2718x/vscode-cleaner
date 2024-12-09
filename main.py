#!/usr/bin/python3
import os
import re
import shutil

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

    dry_run = True

    # dir_config = '/home/al/.config/Code'
    dir_config = '/home/al/.config/VSCodium'
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
