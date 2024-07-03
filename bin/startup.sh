# #!/bin/bash
cd $WEBSITE
./startup.sh
cd $PY
python3 motor.py 1> log/motor.log &
python3 servo.py 1> log/servo.log &
python3 camera.py 1> log/camera.log &
