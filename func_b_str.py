import re

class proc():
	
	desc = ''
	is_completed = False
	step = 0
	

	def __init__(self, func):
		
		self.desc = '[' + func + ']'
		self.is_completed = False	# 計算完了フラグ
		self.step = 0				# 計算ステップ数記録
		self.step_rec = 0			# 
		self.max_len = 0			# 数式の最大長
	
	def solve(self):
		'''
			計算完了するまで update_desc() を繰り返し実行
		'''
		while self.is_completed == False:
			
			self.update_desc()
		
		
	def show(self):
		'''
			数式の表示

		'''
		desc_show = 1
		info_show = 1
		
		if self.step == self.step_rec:
			return
		

		# _desc = re.sub('[\[\]]', '',  self.desc)
		_desc = re.sub('\[(.+)\]', '\033[41m\\1\033[0m',  self.desc)
		
		if self.step % desc_show == 0:
			print('step:{:>3d} len:{:>2d} = {} '.format(self.step, len(_desc), _desc))
			
		elif self.step % info_show == 0:
			print('step:{} max_len:{} len{}'.format(self.step, self.max_len, len(_desc)))
		
		if self.is_completed == True:
			print('step:{} max_len:{}\n  = {}'.format(self.step, self.max_len, _desc))
		
		self.step_rec = self.step
		#print('step:{} | = {}'.format(self.step, _desc))
		
			
			
	def update_desc(self):
		'''

		'''
		self.get_active_func()
		self.expand_active()
		self.replace_active()
		
		self.is_completed = \
			re.fullmatch('\[[0-9]+\]', self.desc) != None
		
		if self.max_len < len(self.desc):
			self.max_len = len(self.desc)
			
		self.show()
		
	
	def replace_active(self):
		'''
			式の計算前後の内容置換
		'''
		# print('update {} -> {}'.format(self.active_part, self.calced))
		
		before = self.active_part
		after = self.calced
		if after != '' and before != after:
			self.desc = self.desc.replace(before, after)
			# print(self.desc)
			self.step += 1
			
		
	def get_active_func(self):
		'''
			式中の活性部分の要素を抽出
		'''
		
		self.active_part = \
			re.findall('(\[.+\])', self.desc)[0]
		
		# print('active:', end='')
		# print(self.active_part)
		
	
	def expand_active(self):
		'''
		式中の活性部分を展開した結果を取得
		- f(n) = n+1
		- B(0,n) = f(n)
		- B(m+1,0) = B(m,1)
		- B(m+1,n+1) = B(m,B(m+1,n1))
		- g(x) = B(x,x)
		'''

		if self.active_part[1] == 'g':
			# g(x) = B(x, x)
			x = re.findall('g\(([0-9]+)\)', self.active_part)[0]
			
			#print('x:', end='')
			#print(x)
			
			self.calced = '[B({}, {})]'.format(x,x)
			
			#print('calced:' + self.calced)
			
		elif self.active_part[1] == 'B':
			# get arg B(m, n)
			m = int(re.findall('B\(([0-9]+), ([0-9]+)\)', self.desc)[0][0])
			n = int(re.findall('B\(([0-9]+), ([0-9]+)\)', self.desc)[0][1])
			
			if m == 0:
				# ルール1 B(0, n) = f(n)
				self.calced = '[f({})]'.format(n)
				
			elif 0 < m and n == 0:
				# ルール2 B(m, 0) = B(m-1, 1)
				self.calced = '[B({}, {})]'.format(m-1, 1)
				
				
			elif 0 < m and 0 < n:
				# ルール3 B(m, n) = B(m-1, B(m, n-1))
				self.calced = 'B({}, [B({}, {})])'.format(m-1, m, n-1)
				
				
		elif self.active_part[1] == 'f':
			# f(n) = n + 1
			
			# get arg f(n)
			n = int(re.findall('f\(([0-9]+)\)', self.desc)[0])
			
			self.calced = '[{}]'.format(n+1)
			
			
		elif '0' <= self.active_part[1] and \
		     self.active_part[1] <= '9':
		     	
		  # 
			#re.findall('(B\([0-9]+, \[[0-9]+\]\))', st)[0]
			self.desc = re.sub('B\(([0-9]+), \[([0-9]+)\]\)','[B(\\1, \\2)]', self.desc)
			
			self.calced = ''
		
		# print('calced:' + self.calced)
		
		
		
if __name__ == '__main__':
	
	g_proc = proc('g(3)')
	
	print('desc :{}'.format(re.sub('[\[\]]','',g_proc.desc)) )
	
	g_proc.solve()
	
	#for i in range(52):

	#	g_proc.update_desc()
	

	
