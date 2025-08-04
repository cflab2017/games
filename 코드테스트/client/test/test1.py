import random

com = random.randint(1,100)

print(com)

while True:
	
	a = input('입력하세요')
	a = int(a)
	
	if a > com:
		print('down')
	if a < com:
		print('up')
	if a == com:
		print('정답')
		break


class std:
	def __init__(self, name):
		self.name = name

	def show_info(self):
		print(f'이름 : {self.name}')



s = std('홍길동')
s.show_info()