#!/bin/bash
echo "Starting server.py..."
python3 server.py &

echo "Starting dashboard/app.py..."
python3 dashboard/app.py