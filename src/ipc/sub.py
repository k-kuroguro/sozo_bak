import asyncio
import time
from selectors import EVENT_READ, DefaultSelector

import zmq
from zmq.asyncio import Context

ctx = Context()
sock = ctx.socket(zmq.SUB)


def interrupt_polling():
    """Fix CTRL-C on Windows using "self pipe trick"."""
    # ctx.send_multipart(['', 'quit'])
    sock.close()
    ctx.term()


selector = DefaultSelector()

from monitor_msg_pb2 import StudyState


def c(f):
    data = f.recv_multipart()[1]
    msg = StudyState()
    msg.ParseFromString(data)
    print(msg)


sock.connect("ipc:///tmp/pubsub")
sock.subscribe(b"kitty cats")


async def main():
    while 1:
        data = await sock.recv_multipart()
        msg = StudyState()
        msg.ParseFromString(data[1])
        print(msg)


asyncio.run(main())

print(1)

sock.close()
ctx.term()
