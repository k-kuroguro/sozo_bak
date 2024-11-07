#!/bin/bash

PYTHON_OUT="."
PROTO_FILE="src/ipc/msg_types/monitor_msg.proto"

cd "$(dirname "$0")/.."

protoc --python_out=$PYTHON_OUT --pyi_out=$PYTHON_OUT $PROTO_FILE
