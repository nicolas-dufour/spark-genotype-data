import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import time
import csv

sc=SparkContext()
sqlContext=SQLContext(sc);
spark = SparkSession.builder.getOrCreate()

### Don't forget to escape the characters when entering them

def listEntries(nucleotide,plant,condition):
	if('.txt' in nucleotide):
		with open(nucleotide, 'rb') as f:
		    reader = csv.reader(f)
		    nucleotides = list(reader)
		    nucleotides=[y for x in nucleotides for y in x]
	else:
		nucleotides=[nucleotide]
	if('.txt' in plant):
		with open(plant, 'rb') as f:
		    reader = csv.reader(f)
		    plants = list(reader)
		    plants=[y for x in plants for y in x]
	else:
		plants=[plant]
	if('.txt' in condition):
		with open(condition, 'rb') as f:
		    reader = csv.reader(f)
		    conditions = list(reader)
		    conditions=[y for x in conditions for y in x]
	else:
		conditions=[condition]
	return(nucleotides,plants,conditions)
def prepareQuery(nucleotides,plants,conditions): # SELECT nucleotides FROM file WHERE plant=plant1 OR plant=plant2 etc... AND condition1 AND condition2
	if(nucleotides!=['ALL']):
		selectstring="plant"
		for i in range(len(nucleotides)):
			selectstring+=', '+str(nucleotides[i])
	else:
		selectstring="*"
	if(plants!=['ALL']):
		wherestring=""
		for i in range(len(plants)-1):
			wherestring+="plant='"+str(plants[i])+ "' or "
		wherestring+="plant='"+str(plants[-1])+"'"
		if(conditions!=['NONE']):
			for i in range(len(conditions)):
				wherestring+=" AND "+str(conditions[i])
		return("SELECT "+selectstring+" FROM db WHERE "+wherestring)
	else:
		if(conditions!=['NONE']):
			wherestring=""
			for i in range(len(conditions)-1):
				wherestring+=str(conditions[i])+ " AND "
			wherestring+=str(conditions[-1])
			return("SELECT "+selectstring+" FROM db WHERE "+wherestring)
		else:
			return("SELECT "+selectstring+" FROM db")

def dbQuery(dbPath,nucleotide,plant,condition):
	df=sqlContext.read.parquet(dbPath)
	df.createTempView('db')
	nucleotides,plants,conditions=listEntries(nucleotide,plant,condition)
	query=prepareQuery(nucleotides,plants,conditions)
	print("Query: "+query)
	spark.sql(query).show()

if __name__ == '__main__':
	start=time.time()
	dbQuery(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	print("The programm took "+str(time.time()-start)+" secondes to run")
