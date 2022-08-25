class queue_(object):

	class Node:

		def __init__(self, dat):
			self.data = dat
			self.next = None

		def setNext(self, n):
			self.next = n

		def getDat(self):
			return self.data

	def __init__(self):
		self.length = 0
		self.head = None
		self.tail = None

	def push(self, dat):
		y = queue_.Node(dat)
		if self.length >= 1:
			self.tail.setNext(y)
			self.tail = y
		else:
			self.head = y
			self.tail = y
		self.length += 1

	def pop(self):
		out = self.head
		self.head = self.head.next
		self.length -= 1
		return out

	def peek(self):
		out = self.head
		return out

	def __len__(self):
		return self.length
