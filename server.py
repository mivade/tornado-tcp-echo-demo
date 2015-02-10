"""Tornado TCP echo server demo."""

import logging
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpserver import TCPServer

logger = logging.getLogger('server')

class EchoServer(TCPServer):
    """Tornado asynchronous echo TCP server."""
    def handle_stream(self, stream, address):
        self.stream = stream
        self.address = address
        self.echo()

    @gen.coroutine
    def echo(self):
        request = yield self.stream.read_until('\n')
        logging.debug('Incoming request: ' + request)
        self.stream.write(request)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = EchoServer()
    server.listen(8080)
    logging.info("Starting server on tcp://localhost:8080")
    IOLoop.instance().start()
