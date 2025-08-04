
class std:
	def __init__(self, name):
		self.name = name

	def show_info(self):
		print(f'이름 : {self.name}')



s = std('홍길동')
s.show_info()