#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  
PORT = 65431

def send(s, cmd):
    s.sendall(cmd.encode("utf-8"))
    data = s.recv(1024)
    print("Received", repr(data))

def get_val(s, key):
    cmd = "get {}".format(key)
    s.sendall(cmd.encode("utf-8"))
    data = s.recv(1024)
    print("Received", repr(data))    

def set_val(s, key, value):
    cmd = "set {} {}\r\n{}".format(key, len(value), value)
    s.sendall(cmd.encode("utf-8"))
    data = s.recv(1024)
    print("Received", repr(data))    
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    send(s, "set k1 7\r\n123557")
    send(s, "get k1")
    send(s, "set k2 15\r\nthis is second value")
    send(s, "get k2")
    send(s, "set k3 7\r\nI am third")
    send(s, "get k3")
    send(s, "set k1 7\r\nover written first")
    send(s, "get k1")
    set_val(s, "big_input_key", "The ParaPro Assessment is a general aptitude test that is required in many states for paraprofessional certification. It also offers school districts an objective assessment of your foundation of knowledge and skills. Start now and take the necessary steps to become a paraprofessional.")
    get_val(s, "big_input_key")
    # key that doesn't exist
    get_val(s, "get k6")

