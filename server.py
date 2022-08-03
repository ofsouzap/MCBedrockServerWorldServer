#!/usr/bin/env python3

from socket import socket as Socket;
from pathlib import Path;
import socket;
from struct import unpack, pack;

import file_exchange;
import world_store;
import access_log as log;
from setup import set_up_server;
from settings import *;
from globals import *;

def create_server_socket(port: int = SERVER_PORT) -> Socket:

    s = Socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP);

    s.bind(("", port));
    s.listen(SERVER_BACKLOG);

    return s;

def handle_client(cli: Socket,
    caddr: str) -> None:

    code = unpack(NET_INT8_FMT, cli.recv(INT8_SIZE))[0];

    if code == REQUEST_WORLDS_LIST:
        handle_client_worlds_list(cli, caddr);

    elif code == REQUEST_TAKE_WORLD:
        handle_client_take_world(cli, caddr);

    elif code == REQUEST_RETURN_WORLD:
        handle_client_return_world(cli, caddr);

    else:
        log.write_unknown_request_type(caddr, code);

def handle_client_worlds_list(cli: Socket,
    caddr: str) -> None:

    world_dirs, world_names = world_store.get_world_names(Path(SERVER_WORLDS_DIR));

    # Send number of worlds

    cli.send(pack(NET_INT32_FMT, len(world_dirs)));

    # Send world names and directory names

    for i in range(len(world_names)):

        file_exchange.send_str(cli, world_dirs[i].name);
        file_exchange.send_str(cli, world_names[i]);

    # Write to access log

    log.write_worlds_listed(caddr);

def handle_client_take_world(cli: Socket,
    caddr: str) -> None:

    # Receive intended world directory name

    wdir_name = file_exchange.recv_str(cli);

    # Load worlds

    world_dir_paths, world_names = world_store.get_world_names(Path(SERVER_WORLDS_DIR));

    wdir_name_matches = [d.name == wdir_name for d in world_dir_paths];

    if any(wdir_name_matches):

        # If matching world found

        windex = wdir_name_matches.index(True);

        cli.send(pack(NET_INT8_FMT, RESPONSE_YES));

        file_exchange.send_dir(cli, world_dir_paths[windex]);

        # TODO - once world locking implemented, lock world here

        # Write to access log
        
        log.write_world_taken(wdir_name, caddr);

    else:

        # If matching world not found

        cli.send(pack(NET_INT8_FMT, RESPONSE_NO));
        
        # Write to access log

        log.write_world_couldnt_take(wdir_name, caddr);

def handle_client_return_world(cli: Socket,
    caddr: str) -> None:

    # Receive intended world name

    wdir_name = file_exchange.recv_str(cli);

    # Load current worlds

    world_dir_paths, world_names = world_store.get_world_names(Path(SERVER_WORLDS_DIR));

    wpath = None;

    # Determine name for world directory

    wdir_name_matches = [d.name == wdir_name for d in world_dir_paths];

    if any(wdir_name_matches):

        windex = wdir_name_matches.index(True);

        wpath = world_dir_paths[windex];

        world_store.move_world_to_backup(wpath); # Backup the current version of the world

        # TODO - once world locking implemented, unlock world here

    else:

        # Find next available name

        i = 0;

        while True:

            wpath = SERVER_WORLDS_DIR / ((wdir_name + str(i)) if i != 0 else wdir_name);

            if not wpath.is_dir():
                break;
            
            i += 1;

    # Receive and save world directory from client

    file_exchange.recv_dir(cli, wpath.parent);

    # Write to access log

    log.write_world_returned(wdir_name, caddr);

def main() -> None:

    set_up_server(); # In case set up is needed

    sock = create_server_socket();

    while True:

        cli, caddr = sock.accept();

        caddr = str(caddr);

        handle_client(cli, caddr);

        cli.close();

if __name__ == "__main__":
    main();
