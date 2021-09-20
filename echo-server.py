import socket
import json
from threading import Lock

HOST = "127.0.0.1"  
PORT = 65431
FILE = "store.json"

lock = Lock()

def find_char(f, start, char):
    f.seek(start)
    while f.read(1) != char:
        continue
    return f.tell()

def _get(key):
    with open(FILE, "r") as f:
        data = json.load(f)
        return data[key]

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

def _set(key, value):
    lock.acquire()
    
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
        return "NOT STORED"
    finally:
        lock.release()
    
    

def handler(data):
    data = data.decode("utf-8")
    tokens = data.split(" ")
    method_keyword = tokens[0]
    if method_keyword == "get":
        return _get(tokens[1])
    if method_keyword == "set":
        return _set(tokens[1], " ".join(tokens[2:]))
    

 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            conn.sendall(handler(data).encode("utf-8"))
