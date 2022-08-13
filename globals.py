# Confirmation

INP_YES_OPTIONS = ["y", "yes", "1"];
INP_NO_OPTIONS = ["n", "no", "0"];

# MC Server files

MC_PROPERTIES_FILE = "server.properties";
MC_PROPERTIES_FILE_WORLD_DIR_KEY = "level-name"; # The name of the property that describes the name of the directory that the MC server's world is in
MC_SERVER_EXE = "bedrock_server.exe";

# Level names

WORLD_LEVELNAME_FILENAME = "levelname.txt";

# Directories and files

SERVER_WORLDS_DIR = "worlds_store";
SERVER_BACKUPS_DIR = "backups";

CLIENT_WORLDS_DIR = "worlds";
CLIENT_BACKUPS_DIR = "world-backups";

SERVER_ACCESS_LOG_FILE = "access-log.txt";

# Networked numerical types

NET_INT32_FMT = "!i";
INT32_SIZE = 4;

NET_INT8_FMT = "!b";
INT8_SIZE = 1;

# Response codes (all of int8)

RESPONSE_YES = 0x00
RESPONSE_NO = 0x01

# Request codes (all of int8)

REQUEST_WORLDS_LIST = 0x00
REQUEST_TAKE_WORLD = 0x01
REQUEST_RETURN_WORLD = 0x02