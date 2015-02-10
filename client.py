"""Tornado TCP echo client demo."""

import logging
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpclient import TCPClient

@gen.coroutine
def main():
    client = TCPClient()
    stream = yield client.connect('127.0.0.1', '8080')

    while True:
        data = raw_input('>>> ')
        logging.debug(data)
        stream.write(data)
        reply = yield stream.read_until('\n')
        logging.info('Reply: ' + reply)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting...")
    IOLoop.instance().run_sync(main)