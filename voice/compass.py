import time
import math
#导入I2C SMBus 模块 
import smbus     

# 配置寄存器A的地址
Register_A = 0
# 配置寄存器B的地址
Register_B = 0x01
# 模式寄存器地址
Register_mode = 0x02
# X、Z和Y轴 MSB数据寄存器的地址
X_axis_H = 0x03
Z_axis_H = 0x05
Y_axis_H = 0x07
# 定义测量位置的偏角
declination = -0.00669
# 圆周率
pai = 3.14159265359
# 初始化一个bus对象
bus = smbus.SMBus(1)
# bus = smbus.SMBus(0)
# HMC5883L设备地址
HMC5883L_Address = 0x1e    
def init():
    """初始化寄存器"""
    # 设置配置寄存器A
    bus.write_byte_data(HMC5883L_Address, Register_A, 0x70)
    # 设置配置寄存器B，设置增益
    bus.write_byte_data(HMC5883L_Address, Register_B, 0xa0)
    # 设置操作模式
    bus.write_byte_data(HMC5883L_Address, Register_mode, 0)
def get_value(addr):
    """从传感器读取数据"""
    # 读取初始16位值
    high = bus.read_byte_data(HMC5883L_Address, addr)
    low = bus.read_byte_data(HMC5883L_Address, addr + 1)
    # 位运算，连接高位与低位的值
    value = ((high << 8) | low)
    # 从模块获取带符号的值
    if value > 32768:
        value = value - 65536
    return value
def main_loop():
    """主循环，打印读取到的数据"""
    # 初始化
    init()
    # 读取原始值
    x = get_value(X_axis_H)
    z = get_value(Z_axis_H)
    y = get_value(Y_axis_H)
    # 计算弧度
    heading = math.atan2(y, x) + declination
    # 检查是否大于360度
    if heading > 2 * pai:
        heading = heading - 2 * pai
    # 检查符号
    if heading < 0:
        heading = heading + 2 * pai
    # 转换成角度
    heading_angle = int(heading * 180 / pai)
    return heading_angle

data=main_loop()
print(data)


