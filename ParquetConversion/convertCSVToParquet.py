import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc=SparkContext()
sqlContext=SQLContext(sc);
def formatFile(path): #Allow us to convert it to parquet. Parquet doesn't handle some characthers
	start=time.time()
	import shutil
	from_file = open(path)
	line = from_file.readline()
	line=line.replace('(','-').replace(')','-')
	to_file = open(path,mode="w")
	to_file.write(line)
	shutil.copyfileobj(from_file, to_file)
	print("The programm took "+str(time.time()-start)+" secondes to run")

def convertToParquet(pathin,pathout):
	if(pathin.split('.')[-1]=='csv'):
		formatFile(pathin)
		df=sqlContext.read.csv(pathin,header='true')
		df.withColumnRenamed('pos','plant')
	else:
		print("error: format not supported")
		exit()
	# formatFile(pathin)
	df.write.parquet(pathout)
if __name__ == '__main__':
	convertToParquet(sys.argv[1],sys.argv[2])
