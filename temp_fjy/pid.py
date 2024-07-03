#-*- coding: UTF-8 -*-
# 调用必需库
import time

class PID:
	def __init__(self, kP, kI, kD):
		# 初始化参数
		self.kP = kP
		self.kI = kI
		self.kD = kD
		print("PID参数初始化完成", kP, kI, kD)

	def initialize(self):
		# 初始化当前时间和上一次计算的时间
		self.currTime = time.time()
		self.prevTime = self.currTime

		# 初始化上一次计算的误差
		self.prevError = 0

		# 初始化误差的比例值，积分值和微分值
		self.cP = 0
		self.cI = 0
		self.cD = 0

	def update(self, error):
		# 暂停
		time.sleep(0.2)

		# 获取当前时间并计算时间差
		self.currTime = time.time()
		deltaTime = self.currTime - self.prevTime

		# 计算误差的微分
		deltaError = error - self.prevError

		# 比例项
		self.cP = error

		# 积分项
		self.cI += error * deltaTime

		# 微分项
		self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

		# 保存时间和误差为下次更新做准备
		self.prevTime = self.currTime
		self.prevError = error
		#print("p是：",self.kP * self.cP,"I是：",
		#	self.kI * self.cI,"D是：",
		#	self.kD * self.cD)

		# 返回输出值
		#print("输出值pid是： {} + {} + {}".format(self.kP * self.cP, self.kI * self.cI, self.kD * self.cD))
		return sum([
			self.kP * self.cP,
			self.kI * self.cI,
			self.kD * self.cD])