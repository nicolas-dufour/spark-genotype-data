import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession

sc=SparkContext()
sqlContext=SQLContext(sc);
spark = SparkSession.builder.getOrCreate()

def loadDataBase(dbPath):
	df=sqlContext.read.parquet(dbPath)
	df.createTempView('db')
def getNucleotideStats(nucleotide):
	total= spark.sql("SELECT COUNT("+nucleotide+") as total FROM db").collect()[0].total
	print spark.sql("SELECT "+nucleotide+" , COUNT("+nucleotide+")/"+str(total)+" AS fq FROM db GROUP BY "+nucleotide).collect()
if __name__ == '__main__':
	loadDataBase(sys.argv[1])
	getNucleotideStats(sys.argv[2])
