from typing import List as tList;
from pathlib import Path;

from globals import *;

server_dirs_to_make = [SERVER_WORLDS_DIR, SERVER_BACKUPS_DIR];
server_files_to_make = [SERVER_ACCESS_LOG_FILE];

client_dirs_to_make = [CLIENT_WORLDS_DIR, CLIENT_BACKUPS_DIR];
client_files_to_make = [];

def make_dirs(dirs: tList[str]):

    for dir in dirs:

        dir_p = Path(dir);

        if not dir_p.is_dir():
            dir_p.mkdir(parents = True, exist_ok = False);

def make_files(files: tList[str]):

    for file in files:

        file_p = Path(file);

        if not file_p.is_file():
            file_p.touch(exist_ok = False);

def set_up_server():

    global server_dirs_to_make, server_files_to_make;

    # Create directories before files so the files have their directories made if needed

    make_dirs(server_dirs_to_make);
    make_files(server_files_to_make);

def set_up_client():

    global client_dirs_to_make, client_files_to_make;

    make_dirs(client_dirs_to_make);
    make_files(client_files_to_make);
