# Server

Server mode is for the device storing the worlds and distributing them when they are being run.

To run the server, run the server.py script with the other scripts it needs in the same directory with it.

The server device only needs the following scripts:

- access_log.py
- file_exchange.py
- globals.py
- server.py
- settings.py
- setup.py
- world_store.py

# Client

Client mode is for the device that will be hosting the server itself and must request the worlds when it needs them.

To run the client, run the client.py script in the MC Bedrock server folder with the other scripts it needs in the same directory with it.

The client device only needs the following scripts:

- client.py
- file_exchange.py
- globals.py
- settings.py
- setup.py
- world_store.py
