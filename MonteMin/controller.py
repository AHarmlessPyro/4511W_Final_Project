import time

def Get(fileName):
	file = (open(fileName,'r'))
	file1 = file.read()
	booMi = (file1[0])
	move = int(file1[1])
	while(not (booMi == 'T')):
		file = (open(fileName,'r'))
		file1 = file.read()
		booMi = (file1[0])
		move = int(file1[1])
		time.sleep(1)

	file.close()
	file1 = open(fileName,'w')
	file1.write("F"+str(move))
	return move
		
	
def Set(col,fileName):
	move = col
	file1 = open(fileName,'w')
	file1.write("T"+str(move))
	print(move)
	file1.close()
