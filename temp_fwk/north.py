from compass import main_loop
import time

result = main_loop()
while (not(result>=100 and result<=120)):
    print("在转了")
    time.sleep(0.5)
    result = main_loop()
