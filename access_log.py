from pathlib import Path;
from datetime import datetime;

from globals import *;

log_path = Path(SERVER_ACCESS_LOG_FILE);

def get_log_timestamp() -> str:
    now = datetime.now();
    return now.strftime("[%y-%m-%d %H:%M:%S]");

def write_log_line(s: str) -> None:
    with log_path.open("a") as file:
        file.write(get_log_timestamp() + ' ' + s + "\n");

def write_unknown_request_type(caddr: str, req: int) -> None:
    write_log_line(f"Unknown request from {caddr}: {str(req)}");

def write_worlds_listed(caddr: str) -> None:
    write_log_line(f"Worlds listed by {caddr}");

def write_world_taken(wname: str, caddr: str) -> None:
    write_log_line(f"World \"{wname}\" taken by {caddr}");

def write_world_couldnt_take(wname: str, caddr: str) -> None:
    write_log_line(f"Client {caddr} tried but couldn't take world {wname}");

def write_world_returned(wname: str, caddr: str) -> None:
    write_log_line(f"World \"{wname}\" returned by {caddr}");