import numpy as np
uu = np.load('disparitttty.npy')
print(uu.shape)

fi = open("sureThing.txt", 'w')
for i in uu:
	stri = ""
	for j in i:
		stri += str(j) + "\t"
	fi.write(stri)
	
print("Completed")
