import time

import zmq
from monitor_msg_pb2 import MonitorMsg, StudyState

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind("ipc:///tmp/pubsub")

print("Starting loop...")
topic = "kitty cats"

i = 1
time.sleep(0.1)
while True:
    msg = StudyState(concentration_score=float(i)).SerializeToString()
    sock.send_multipart([topic.encode(), msg])
    print("Sent string: %s ..." % msg)
    i += 1
    time.sleep(1)

sock.close()
ctx.term()
