import time
import board
import adafruit_dht

def read_dht11():

    dht_device = adafruit_dht.DHT11(board.D4)
    while True:
        try:
            tem_c = dht_device.temperature
            tem_f = tem_c * (9 / 5) + 32
            hum = dht_device.humidity
            return("温度{:.1f}华氏度{:.1f}摄氏度湿度百分之{}".format(tem_f, tem_c, hum))
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)

read_dht11()