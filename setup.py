from pathlib import Path;

from globals import *;

server_dirs_to_make = [SERVER_WORLDS_DIR, SERVER_BACKUPS_DIR];
server_files_to_make = [SERVER_ACCESS_LOG_FILE];

def set_up_server():

    global server_dirs_to_make, server_files_to_make;

    # Create directories before files so the files have their directories made if needed

    for dir in server_dirs_to_make:

        dir_p = Path(dir);

        if not dir_p.is_dir():
            dir_p.mkdir(parents = True, exist_ok = False);

    for file in server_files_to_make:

        file_p = Path(file);

        if not file_p.is_file():
            file_p.touch(exist_ok = False);
