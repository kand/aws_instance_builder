import os
from root import create_publisher

from quixote.server.simple_server import run
port = 8080
host = "localhost"
print("current working directory: %s" % os.getcwd())
print("listening on %s:%i" % (host,port))
run(create_publisher,host=host,port=port)
