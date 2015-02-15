"""Tornado TCP echo server/client demo."""

from __future__ import print_function
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer

# Server
# -----------------------------------------------------------------------------

class EchoServer(TCPServer):
    """Tornado asynchronous echo TCP server."""
    clients = set()

    @classmethod
    def show_clients(cls):
        print("Connected clients: ")
        for client in EchoServer.clients:
            print(client)
    
    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, fileno = address
        print("Incoming connection from " + ip)
        EchoServer.clients.add(address)
        while True:
            try:
                yield self.echo(stream)
            except StreamClosedError:
                print("Client " + str(address) + " left.")
                EchoServer.clients.remove(address)
                break

    @gen.coroutine
    def echo(self, stream):
        data = yield stream.read_until('\n')
        print('Echoing data: ' + repr(data))
        yield stream.write(data)

def start_server():
    server = EchoServer()
    server.listen(8080)
    print("Starting server on tcp://localhost:8080")
    show_clients = PeriodicCallback(lambda: server.show_clients(), 5000)
    show_clients.start()
    IOLoop.instance().start()

# Client
# -----------------------------------------------------------------------------

@gen.coroutine
def client():
    stream = yield TCPClient().connect('127.0.0.1', 8080)
    while True:
        data = raw_input('>>> ') + '\n'
        yield stream.write(data)
        reply = yield stream.read_until('\n')
        print(reply)
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