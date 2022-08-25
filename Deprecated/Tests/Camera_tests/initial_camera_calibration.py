#Cam Calibration

class cam:

	def __init__(self):
		self.focal = 0

	def findFocal(self, pxWid, dist, wid):
		self.focal = (pxWid*dist)/wid

	def getFoc(self):
		return self.focal


camJ = cam()
camJ.findFocal(58, .9218, .087)
foc = camJ.getFoc()
print(foc)

print((51*1.016)/foc)



