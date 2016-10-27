#!/bin/sh
python3 server.py 8080 & python3 client.py 8070 8080 & python3 client.py 8060 8080
