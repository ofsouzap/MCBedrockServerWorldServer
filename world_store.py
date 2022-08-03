from typing import Tuple as tTuple;
from typing import List as tList;
from datetime import datetime;
from pathlib import Path;

from globals import *;

def get_world_name_from_file(filepath: Path) -> str:

    with filepath.open("r") as file:
        name = file.read().strip();
    
    return name;

def get_world_name_from_dir(dir: Path) -> str:

    filepath = dir / WORLD_LEVELNAME_FILENAME;
    return get_world_name_from_file(filepath);

def get_world_names(worlds_dir: Path) -> tTuple[tList[Path], tList[str]]:

    sub_dirs = [s.absolute() for s in worlds_dir.iterdir() if s.is_dir()];

    names = [get_world_name_from_dir(s) for s in sub_dirs];

    return (sub_dirs, names);

def get_backup_timestamp() -> str:
    now = datetime.now();
    return now.strftime("%y-%m-%d_%H-%M-%S");

def get_next_backup_path(backups_dir: Path,
    base_name: str) -> Path:

    base_ts = base_name + ' ' + get_backup_timestamp();

    i = 0;
    while True:
        
        suffix = base_ts if i == 0 else base_ts + str(i);
        new = backups_dir / suffix;
        if not new.is_dir():
            return new;

        i += 1;

def move_dir_contents(src_dir: Path,
    dst_dir: Path) -> None:

    # Use absolute paths

    src_dir = src_dir.absolute();
    dst_dir = dst_dir.absolute();

    # Check directory paths

    if not src_dir.is_dir():
        raise Exception("Source directory provided doesn't exist.");

    if dst_dir.is_dir():
        raise Exception("Destination directory provided already exists.");

    # Create destination directory

    dst_dir.mkdir(parents = False, exist_ok = False);

    # Copy items from source to destination

    for item in src_dir.iterdir():

        if item.is_file():
            item.rename(dst_dir / item.name);

        elif item.is_dir():
            new_dir = dst_dir / item.name;
            move_dir_contents(item, new_dir);

        else:
            raise Exception(f"Directory item found that isn't file or directory at: {item.absolute()}");

    # Once directory is emptied, remove original

    src_dir.rmdir();

def move_world_to_backup(world_dir: Path) -> None:

    """Moves the copy of a world in the worlds directory to the backups directory removing the original in the process."""

    new_dir = get_next_backup_path(Path(SERVER_BACKUPS_DIR), world_dir.name);

    move_dir_contents(world_dir, new_dir);
