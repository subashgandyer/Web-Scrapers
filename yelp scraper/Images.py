import shutil
import os
 
# copy all the files in the subfolders to main folder
 
# The current working directory
dest_dir = os.getcwd()
# The generator that walks over the folder tree
walker = os.walk(dest_dir)
 
# the first walk would be the same main directory
# which if processed, is
# redundant
# and raises shutil.Error
# as the file already exists
 
rem_dirs = walker.next()[1]
 
for data in walker:
	for files in data[2]:
		try:
			shutil.move(data[0] + os.sep + files, dest_dir)
		except shutil.Error:
		# still to be on the safe side
			continue
 
# clearing the directories
# from whom we have just removed the files
for dirs in rem_dirs:
	shutil.rmtree(dest_dir + os.sep + dirs)
