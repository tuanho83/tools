


ptGuiFile = open("O:\\WT_GP\\01_opt.pts","r")
imagecount = 0
for line in ptGuiFile.readlines():
	if '#-imgfile'in line:
		imagecount += 1
		ptguiImageLine = line.replace('\n','').split(' ')
		ptguiImageX = ptguiImageLine[1]
		ptguiImageY = ptguiImageLine[2]  
		ptguiImagePath = ptguiImageLine[3]  
		print ptguiImageLine
	#print 'QB ', values[0], values[1], 'had a rating of ', values[10]
	# print values

ptGuiFile.close()

print imagecount