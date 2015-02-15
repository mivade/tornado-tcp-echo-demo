"""Tornado TCP echo server/client demo."""

from __future__ import print_function
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer

# Server
# -----------------------------------------------------------------------------

class EchoServer(TCPServer):
    """Tornado asynchronous echo TCP server."""
    def handle_stream(self, stream, address):
        print("Incoming connction from " + str(address))
        self.echo(stream, address)

    @gen.coroutine
    def echo(self, stream, address):
        data = yield stream.read_until('\n')
        print('Echoing data: ' + repr(data))
        yield stream.write(data)

def start_server():
    server = EchoServer()
    server.listen(8080)
    print("Starting server on tcp://localhost:8080")
    IOLoop.instance().start()

# Client
# -----------------------------------------------------------------------------

@gen.coroutine
def echo(stream):
    data = raw_input('>>> ') + '\n'
    yield stream.write(data)
    reply = yield stream.read_until('\n')
    print(reply.strip())
    raise gen.Return(reply)

@gen.coroutine
def client():
    stream = yield TCPClient().connect('127.0.0.1', 8080)
    while True:
        reply = yield echo(stream)
        if reply.strip() == 'quit':
            stream.close()
            break

if __name__ == "__main__":
    import sys
    if sys.argv[1] == 'client':
        print("Starting client...")
        IOLoop.instance().run_sync(client)
    elif sys.argv[1] == 'server':
        start_server()