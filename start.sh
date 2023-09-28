#!/usr/bin/env bash

echo "Starting web server"
python web.py &

echo "Starting hikari bot"
python main.py
