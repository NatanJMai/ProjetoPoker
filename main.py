import os
import time
from sys import argv

def run():
    os.system("python3 server.py 8080 &")
    time.sleep(1)
    os.system("python3 client.py 8010 8080 &")
    time.sleep(1)
    os.system("python3 client.py 8020 8080 &")
    time.sleep(1)
    os.system("python3 client.py 8030 8080 &")
    time.sleep(1)
    os.system("python3 client.py 8040 8080 &")


def stop():
    os.system("pkill -f server.py &")
    os.system("pkill -f client.py &")


if argv[1] == 'r':
    run()
    
if argv[1] == 's':
    stop()