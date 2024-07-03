import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
signal = 32
GPIO.setup(signal, GPIO.OUT)
frequency = 50
pwm = GPIO.PWM(signal, frequency)
def get_duty(direction):
     duty = (direction/18 +2)
     print('duty:',duty)
     return duty
if __name__=='__main__':
    try:
        pwm.start(0)
        while True:
            direction = float(input("请输入一个1～180之间的角度"))
            duty = get_duty(direction)
            pwm.ChangeDutyCycle(duty)
            time.sleep(1)
    except Exception as e:
        print('An exception happen', e)
    finally:
        print("exit")
        pwm.stop()
        GPIO.cleanup()
