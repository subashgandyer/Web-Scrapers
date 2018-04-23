import os
for filename in os.listdir('.'):
	if filename.startswith("D:\subash"):
		print 'Yes'
		os.rename(filename, filename[25:])


