import argparse
from http.server import HTTPServer
from .base_service import BaseAgentHandler
from .wechat_service import *

parser = argparse.ArgumentParser(description="Start server script for agent")
parser.add_argument(
    "--host", type=str, default="localhost", help="The host name of the server"
)
parser.add_argument("--port", type=int, default=8080, help="The port of the server")
args = parser.parse_args()


def start_agent():
    server = HTTPServer((args.host, args.port), BaseAgentHandler)
    print("Server created @ http://{}:{}".format(args.host, args.port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server closed")


if __name__ == "__main__":
    start_agent()
