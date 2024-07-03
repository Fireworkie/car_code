# #!/bin/bash
cd $WEBSITE
./shutdown.sh
pkill -f "python3 motor.py"
pkill -f "python3 servo.py"
pkill -f "python3 camera.py"