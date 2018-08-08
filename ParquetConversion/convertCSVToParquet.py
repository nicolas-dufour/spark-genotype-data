import sys
import codecs
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc=SparkContext()
sqlContext=SQLContext(sc);
def formatFile(path): #Allow us to convert it to parquet. Parquet doesn't handle some characthers. Apply this function when the conversion don't work becquse of some characters in the header
	with open(path, 'r+') as f:
	    line = next(f) # grab first line
	    f.seek(0) # move file pointer to beginning of file
	    f.write(line.replace('(','-').replace(')','-'))
def convertToParquet(pathin,pathout):#Function to convert our CSV into Parquet
	if(pathin.split('.')[-1]=='csv'):
		df=sqlContext.read.csv(pathin,header='true')
		df.withColumnRenamed('pos','plant') #We use this when we want to go from sample oriented to marker oriented
	else:
		print("error: format not supported")
		exit()
	df.write.parquet(pathout)
if __name__ == '__main__':
	convertToParquet(sys.argv[1],sys.argv[2])
