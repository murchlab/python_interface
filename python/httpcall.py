import os
import sys
import threading
import subprocess
from subprocess import Popen
import zmq
import json
import time


def http_call_pyhost(module, function):
    zmq_port = 27183

    try:
        process = Popen(['nohup', 'python', '\"/Users/simplex/OneDrive - Washington University in St. Louis/Library/Murch Lab/Projects/python_interface/python/pyhost.py\"'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # process = Popen(['nohup', 'python', 'pyhost.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print(123)
        pass

    #  Socket to talk to the pyhost.py
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:" + str(zmq_port))

    # host_init()
    method = 'HTTP'
    call_dict = {'method': method, 'module': module, 'function': function}
    call_json = json.dumps(call_dict)

    socket.send(call_json.encode('utf-8'))

    #  Get the reply.
    message = socket.recv()
    print(message)


if __name__ == "__main__":
    module = r"/Users/simplex/OneDrive - Washington University in St. Louis/Library/Murch Lab/Projects/python_interface/python/test_module.py"
    function = r"rand(500, 1000)"
    http_call_pyhost(module, function)
