"""Tornado TCP echo server/client demo."""

from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer

define('port', default=8080, help="TCP port to use")
define('server', default=False, help="Run as the echo server")
define('encoding', default='utf-8', help="String encoding")

# Server
# -----------------------------------------------------------------------------

class EchoServer(TCPServer):
    """Tornado asynchronous echo TCP server."""
    clients = set()
    
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
        data = yield stream.read_until('\n'.encode(options.encoding))
        print('Echoing data: ' + repr(data))
        yield stream.write(data)

def start_server():
    server = EchoServer()
    server.listen(options.port)
    print("Starting server on tcp://localhost:" + str(options.port))
    IOLoop.instance().start()

# Client
# -----------------------------------------------------------------------------

@gen.coroutine
def echo(stream, text):
    """Send the text to the server and print the reply."""
    if text[-1] != '\n':
        text = text + '\n'
    yield stream.write(text.encode(options.encoding))
    reply = yield stream.read_until('\n'.encode(options.encoding))
    print(reply.decode(options.encoding).strip())

@gen.coroutine
def run_client():
    """Setup the connection to the echo server and wait for user
    input.

    """
    stream = yield TCPClient().connect('127.0.0.1', options.port)
    try:
        while True:
            data = input('(echo) ')
            yield echo(stream, data)
    except KeyboardInterrupt:
        stream.close()

if __name__ == "__main__":
    options.parse_command_line()
    if options.server:
        start_server()
    else:
        print("Starting client...")
        IOLoop.instance().run_sync(run_client)
