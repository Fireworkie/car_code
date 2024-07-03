import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT11(board.D4)
while True:
    try:
        tem_c = dht_device.temperature
        tem_f = tem_c * (9 / 5) + 32
        hum = dht_device.humidity

        print(
            "温度: {:.1f} °F / {:.1f} °C    湿度: {}% ".format(tem_f, tem_c, hum)
        )
    except RuntimeError as error:

          print(error.args[0])
    time.sleep(2.0)