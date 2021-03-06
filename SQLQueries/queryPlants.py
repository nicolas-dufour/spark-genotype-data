import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import time
import csv

sc=SparkContext()
sqlContext=SQLContext(sc);
spark = SparkSession.builder.getOrCreate()

### Don't forget to escape the characters when entering them \( for ( for exemple

def listEntries(nucleotide,plant,condition): #This function transform the file, the array (for the api) or the single string into a standard array
	if('.txt' in nucleotide):
		with open(nucleotide, 'rb') as f:
		    reader = csv.reader(f)
		    nucleotides = list(reader)
		    nucleotides=[y for x in nucleotides for y in x]
	elif(isinstance(nucleotide,list)):
		nucleotides=nucleotide
	else:
		nucleotides=[nucleotide]
	if('.txt' in plant):
		with open(plant, 'rb') as f:
		    reader = csv.reader(f)
		    plants = list(reader)
		    plants=[y for x in plants for y in x]
	elif(isinstance(plant,list)):
		plants=plant
	else:
		plants=[plant]
	if('.txt' in condition):
		with open(condition, 'rb') as f:
		    reader = csv.reader(f)
		    conditions = list(reader)
		    conditions=[y for x in conditions for y in x]
	elif(isinstance(condition,list)):
		conditions=condition
	else:
		conditions=[condition]
	return(plants,nucleotides,condition)
def prepareQuery(plants,nucleotides,conditions): # SELECT nucleotides FROM file WHERE plant=plant1 OR plant=plant2 etc... AND condition1 AND condition2
	if(plants!=['ALL']):
		selectstring="pos"
		for i in range(len(plants)):
			selectstring+=', '+str(plants[i])
	else:
		selectstring="*"
	if(nucleotides!=['ALL']):
		wherestring=""
		for i in range(len(nucleotides)-1):
			wherestring+="pos='"+str(nucleotides[i])+ "' or "
		wherestring+="pos='"+str(nucleotides[-1])+"'"
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

def dbQuery(dbPath,nucleotide,plant,condition):#This function is the one to use to query on our Parquet file
	df=sqlContext.read.parquet(dbPath)
	df.createOrReplaceTempView('db')
	plants,nucleotides,conditions=listEntries(plant,nucleotide,condition)
	query=prepareQuery(plants,nucleotides,conditions)
	print("Query: "+query)
	return spark.sql(query).toJSON().collect()

if __name__ == '__main__':
	start=time.time()
	print(dbQuery(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
	print("The programm took "+str(time.time()-start)+" secondes to run")
