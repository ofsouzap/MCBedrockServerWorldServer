from socket import socket as Socket;
from struct import pack, unpack;
from pathlib import Path;

from globals import *;

# File code and directory code are of int8
END_CONTENT_CODE = 0x00;
FILE_CONTENT_CODE = 0x01;
DIR_CONTENT_CODE = 0x02;

def recv_bytes(cli: Socket,
    size: int) -> bytearray:

    out = bytearray(size);
    i = 0;

    while True:

        if i == size:
            break;

        recv = cli.recv(size - i);

        if not recv:
            break;

        for b in recv:
            out[i] = b;
            i += 1;

    return out;

def recv_str(cli: Socket) -> str:

    size = unpack(NET_INT32_FMT, cli.recv(INT32_SIZE))[0];

    out_bytes = recv_bytes(cli, size);
    out = out_bytes.decode();

    return out;

def recv_file(cli: Socket,
    out_parent_path: Path) -> None:

    # Receive filename

    filename = recv_str(cli);

    # Receive length

    size = unpack(NET_INT32_FMT, cli.recv(INT32_SIZE))[0];

    # Receive contents

    out = recv_bytes(cli, size);

    # Write output to out file

    out_file_path = out_parent_path / filename;

    with out_file_path.open("wb") as file:
        file.write(out);

def recv_dir(cli: Socket,
    parent_path: Path) -> None:

    if not parent_path.is_dir():
        raise Exception("Parent path provided isn't directory.");

    # Receive name

    dir_name = recv_str(cli);

    # Create directory

    dir_path = parent_path / dir_name;
    dir_path.mkdir(parents = False, exist_ok = True);

    # Receive directory contents

    while True:

        type_code = unpack(NET_INT8_FMT, cli.recv(INT8_SIZE))[0];

        if type_code == END_CONTENT_CODE:
            break;

        elif type_code == FILE_CONTENT_CODE:
            recv_file(cli, dir_path);

        elif type_code == DIR_CONTENT_CODE:
            recv_dir(cli, dir_path);

        else:
            raise Exception(f"Unknown content code received: {type_code}");

def send_str(sock: Socket,
    s: str) -> None:

    bs = s.encode();

    sock.send(pack(NET_INT32_FMT, len(bs)));

    sock.send(bs);

def send_file(sock: Socket,
    file_path: Path) -> None:

    if not file_path.is_file():
        raise Exception("File provided doesn't exist.");

    # Send filename

    send_str(sock, file_path.name);

    # Get file data

    with file_path.open("rb") as file:
        data = file.read();

    # Send length

    size = len(data);

    sock.send(pack(NET_INT32_FMT, size));

    # Send contents

    sock.send(data);

def send_dir(sock: Socket,
    dir_path: Path) -> None:

    if not dir_path.is_dir():
        raise Exception("Directory provided doesn't exist");

    # Send name

    send_str(sock, dir_path.name);

    # Send directory contents

    for item in dir_path.iterdir():

        if item.is_file():

            sock.send(pack(NET_INT8_FMT, FILE_CONTENT_CODE));
            send_file(sock, item);

        elif item.is_dir():

            sock.send(pack(NET_INT8_FMT, DIR_CONTENT_CODE));
            send_dir(sock, item);

        else:
            raise Exception(f"Directory item found that isn't file or directory at: {item.absolute()}");

    sock.send(pack(NET_INT8_FMT, END_CONTENT_CODE));
