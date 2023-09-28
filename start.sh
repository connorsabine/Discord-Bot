#!/usr/bin/env bash

echo "Starting web server"
python web.py &

echo "Starting hikari bot"
python src/main.py
