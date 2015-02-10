"""Tornado TCP echo server demo."""

import logging
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpserver import TCPServer

logger = logging.getLogger('server')

class EchoConnection(object):
    def __init__(self, stream, address):
        self.stream = stream
        self.address = address
        self.echo()

    def echo(self):
        self.stream.read_until('\n', self._read)

    def _read(self, data):
        logging.debug('Got data: ' + repr(data))
        self.stream.write(data)

class EchoServer(TCPServer):
    """Tornado asynchronous echo TCP server."""
    def handle_stream(self, stream, address):
        logging.info("Incoming connction from " + str(address))
        print stream
        self.stream = stream
        self.address = address
        EchoConnection(self.stream, self.address)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = EchoServer()
    server.listen(8080)
    logging.info("Starting server on tcp://localhost:8080")
    IOLoop.instance().start()
