from socket import socket as Socket;
from pathlib import Path;
from subprocess import run;
from typing import Tuple as tTuple;
from typing import List as tList;
import socket;
from struct import unpack, pack;

import file_exchange;
from settings import *;
from globals import *;

def set_mc_server_world_name(wdir_name: str) -> None:

    sprops_path = Path(MC_PROPERTIES_FILE);

    if not sprops_path.is_file():
        raise Exception("MC server properties file doesn't exist.");

    # Read current lines

    lines = None;

    with sprops_path.open("r") as file:
        lines = list(file.readlines());

    # Find world dir name line

    wdir_index = -1;

    for i in range(len(lines)):

        l = lines[i];

        parts = l.split("=");

        if parts[0].strip() == MC_PROPERTIES_FILE_WORLD_DIR_KEY:
            wdir_index = i;

    if wdir_index < 0:
        raise Exception("World directory name entry couldn't be found in MC server properties file.");

    # Edit properties

    lines[wdir_index] = MC_PROPERTIES_FILE_WORLD_DIR_KEY + "=" + wdir_name + "\n";

    # Write edited properties

    with sprops_path.open("w") as file:
        file.writelines(lines);

def create_client_socket(saddr: tTuple[str, int]) -> Socket:

    s = Socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP);

    s.connect(saddr);

    return s;

def get_server_addr() -> tTuple[str, int]:

    ip = input("Server Address> ");

    return ip, SERVER_PORT;

def get_worlds(saddr: tTuple[str, int]) -> tTuple[tList[str], tList[str]]:

    # Create socket

    sock = create_client_socket(saddr);

    # Prepare names array

    wdir_names = [];
    wnames = [];

    # Send request type

    sock.send(pack(NET_INT8_FMT, REQUEST_WORLDS_LIST));

    # Get number of worlds

    n = unpack(NET_INT32_FMT, sock.recv(INT32_SIZE))[0];

    # Receive worlds

    for _ in range(n):

        wdir_names.append(file_exchange.recv_str(sock));
        wnames.append(file_exchange.recv_str(sock));

    # Close socket

    sock.close();

    # Return output

    return wdir_names, wnames;

def get_input_world_option(wdir_names: tList[str],
    wnames: tList[str]) -> str:

    while True:

        print("Choose world to run:");

        for i in range(len(wnames)):
            name = wnames[i];
            dir = wdir_names[i];
            print(f"{i}) {dir} ({name})");

        inp = input("World (case-sensitive)> ");

        if inp.isdigit() and (0 <= int(inp) < len(wnames)):
            return wdir_names[int(inp)];

        elif inp in wdir_names:
            return inp;

        elif inp in wnames:
            return wdir_names[wnames.index(inp)];

        else:
            print("Invalid choice.\n");

def delete_directory(dir: Path):

    for item in dir.iterdir():

        if item.is_file():
            item.unlink();
        
        elif item.is_dir():
            delete_directory(item.absolute());

        else:
            raise Exception(f"Directory item found that isn't file or directory at: {item.absolute()}");

    # Once contents removed, remove directory

    dir.rmdir();

def confirm_replace_dir(dir: Path) -> bool:

    while True:

        inp = input(f"Are you sure you want to overwrite the existing world {dir.name} (y/n)? ");

        if inp.lower() in INP_YES_OPTIONS:
            return True;

        elif inp.lower() in INP_NO_OPTIONS:
            return False;

        else:
            print("Invalid selection.\n");

def try_take_world_from_server(saddr: tTuple[str, int],
    wdir_name: str) -> bool:

    wdir_path = Path(CLIENT_WORLDS_DIR) / wdir_name;

    # If world exists, delete if user agress

    if wdir_path.is_dir():

        if confirm_replace_dir(wdir_path):
            delete_directory(wdir_path);

        else:
            return False;

    # Create socket

    sock = create_client_socket(saddr);

    # Send request type

    sock.send(pack(NET_INT8_FMT, REQUEST_TAKE_WORLD));

    # Send world name

    file_exchange.send_str(sock, wdir_name);

    # Receive response

    resp = unpack(NET_INT8_FMT, sock.recv(INT8_SIZE))[0];

    if resp == RESPONSE_NO:
        return False;

    elif resp != RESPONSE_YES:
        raise Exception("Unknown response to trying to take world");

    # Receive the world directory

    file_exchange.recv_dir(sock, Path(CLIENT_WORLDS_DIR));

    # Return success

    return True;

def run_server() -> None:

    run([MC_SERVER_EXE]);

def return_world_to_server(saddr: tTuple[str, int],
    wdir_name: str) -> None:

    sock = create_client_socket(saddr);

    wdir_path = Path(CLIENT_WORLDS_DIR) / wdir_name;

    if not wdir_path.is_dir():
        raise Exception("World specified doesn't exist.");

    # Send request type

    sock.send(pack(NET_INT8_FMT, REQUEST_RETURN_WORLD));

    # Send world name

    file_exchange.send_str(sock, wdir_name);

    # Send world directory

    file_exchange.send_dir(sock, wdir_path);

def main() -> None:

    saddr = get_server_addr();

    while True:

        wdir_names, wnames = get_worlds(saddr);

        if len(wnames) == 0:
            print("No worlds available, quitting program.");
            return;

        wdir_name = get_input_world_option(wdir_names, wnames);

        if try_take_world_from_server(saddr, wdir_name):
            break;

        else:
            print("Couldn't get that world");

    set_mc_server_world_name(wdir_name);

    try:
        run_server();

    except KeyboardInterrupt:
        print("MC Server halted with keyboard interrupt.");

    print("MC server halted, returning world to server.");

    return_world_to_server(saddr, wdir_name);

    print("World returned to server.");

if __name__ == "__main__":
    main();
