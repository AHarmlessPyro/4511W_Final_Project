
import time
file_m = 'transferM.txt'
file_mi = 'transferMi.txt'

def GetMoveM():
	file = (open(file_m,'r'))
	file1 = file.read()
	booMi = (file1[0])
	move = int(file1[1])
	while(not (booMi == 'T')):
		file = (open(file_m,'r'))
		file1 = file.read()
		booMi = (file1[0])
		move = int(file1[1])
		time.sleep(1)

	file.close()
	file1 = open(file_m,'w')
	file1.write("F"+str(move))
	return move
		
	
def SetMoveM(n):
	move = n
	file1 = open(file_m,'w')
	file1.write("T"+str(move))
	print(move)
	file1.close()


def GetMoveMi():
	file = (open(file_mi,'r'))
	file1 = file.read()
	booMi = (file1[0])
	move = int(file1[1])
	while(not (booMi == 'T')):
		file = (open(file_mi,'r'))
		file1 = file.read()
		booMi = (file1[0])
		move = int(file1[1])
		time.sleep(1)

	file.close()
	file1 = open(file_mi,'w')
	file1.write("F"+str(move))
	file1.close()
	
	return move
		

def SetMoveMi(n):
	move = n
	file1 = open(file_mi,'w')
	file1.write("T"+str(move))
	file1.close()
	



	
   