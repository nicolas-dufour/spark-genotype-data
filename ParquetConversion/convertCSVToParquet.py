import sys
import codecs
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc=SparkContext()
sqlContext=SQLContext(sc);
def formatFile(path): #Allow us to convert it to parquet. Parquet doesn't handle some characthers
	lec=codecs.open(path,'r').read()
	s=codecs.open(path,'w')
	lec=lec.replace('(','-').replace(')','-')
	s.write(lec)
	s.close()
def convertToParquet(pathin,pathout):
	if(pathin.split('.')[-1]=='csv'):
		df=sqlContext.read.csv(pathin,header='true')
		df.withColumnRenamed('pos','plant')
	else:
		print("error: format not supported")
		exit()
	# formatFile(pathin)
	df.write.parquet(pathout)
if __name__ == '__main__':
	convertToParquet(sys.argv[1],sys.argv[2])
