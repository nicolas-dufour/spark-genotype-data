##Took 374 sec to create a 1.1Go
import sys
import time
time1=time.time()
from random import randint
NewFile=open('testFile.csv','w+')
for i in range(int(sys.argv[1])):
	for j in range(int(sys.argv[2])):
		NewFile.write(str(randint(0,100))+',')
	NewFile.write(str(randint(0,100))+'\n')
print('The file took '+str(time.time()-time1)+'s to be created')