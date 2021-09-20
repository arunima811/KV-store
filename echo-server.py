import socket
import os
import json
from threading import Lock
import threading
import time

HOST = "127.0.0.1"  
PORT = 65431
FILE = "store.json"

def ensure_store_exists():
    if not os.path.exists(FILE):
        with open(FILE, 'w'): pass

class KeyValueCache(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.lock = Lock()

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            
    def _get(self, key):
        print("GET ", key)
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
                
                if key in data:
                    return data[key]
                else:
                    return "NO-KEY"
        except Exception as e:
            print("Unable to be open JSON file")

    def _set(self, key, value):
        print("SET ", key)
        self.lock.acquire()

        try:
            data = None
            with open(FILE, "r") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    data = dict()
            data[key] = value
            with open(FILE, "w") as f:
                json.dump(data, f)
            return "STORED"
        except Exception as e:
            print(e)
            return "NOT-STORED"
        finally:
            self.lock.release()
        
    def listenToClient(self, client, address):
        while True:
            try:
                byte_data = client.recv(2048)
                byte_data = byte_data.decode("utf-8")
                byte_data = byte_data.split("\r\n")
                
                header = byte_data[0]
                tokens = header.split(" ")
                cmd = tokens[0]
                
                if cmd == "set":
                    key = tokens[1]
                    size = tokens[2]
                    value = byte_data[1]
                    client.sendall(self._set(key, value).encode("utf-8"))
                elif cmd == "get":
                    key = tokens[1]
                    value = self._get(key)
                    
                    resp = "VALUE {} {}\r\n{}".format(key, len(value), value)
                    client.sendall(resp.encode("utf-8"))
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

ensure_store_exists()
KeyValueCache('127.0.0.1', PORT).listen()

# ===========

def find_char(f, start, char):
    f.seek(start)
    while f.read(1) != char:
        continue
    return f.tell()

def _get_old(key, size):
    with open("store", "r") as store:
        pos = 0
        current_key = None
        while file.tell() < f.size():
            pos_s = find_char(f, pos, ' ')
            f.seek(pos)
            current_key = f.read(pos_s - pos + 1)
            if current_key == key:
                f.read(1)
                pos = f.tell()
                pos_s = find_char(f, pos, ' ')
                f.seek(pos)
                current_size = f.read(pos_s - pos + 1)
                f.read(1)
                return f.read(current_size)
            else:
                f.read(1)
                pos = f.tell()
                pos_s = find_char(f, pos, ' ')
                f.seek(pos)
                current_size = f.read(pos_s - pos + 1)
                pos = f.tell() + current_size + 1