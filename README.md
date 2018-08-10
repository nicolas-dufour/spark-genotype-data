#### Improving storage of genotypic data

## This is the readme of the code Nicolas DUFOUR produce during 2018 summer internship at BTI in Mueller's lab

#memeff_csv_transpo.py

This script is used to transpose matrices that don't fit in RAM. It only takes as arguments the path to the file

##convertCSVToParquet.py

This script is used with spark to convert genotypic CSV to parquet. You give him the path in hdfs for your csv and the path where you want your parquet file in hdfs.

##queryNucleotides.py

Can be used as a script or as a module. if script the argument can be given as a text file or a string for single arguments. If module you can also pass him arrays. The arguments are the db path in HDFS, markers you want to retrieve, the plants you want to filter and some condition you want to add. The query is the following:  SELECT nucleotides FROM file WHERE plant=plant1 OR plant=plant2 etc... AND condition1 AND condition2

##queryPlants.py

Can be used as a script or as a module. if script the argument can be given as a text file or a string for single arguments. If module you can also pass him arrays. The arguments are the db Path, plants you want to retrieve, the markers you want to filter and some condition you want to add. The query is the following:  SELECT plants FROM file WHERE pos=pos1 OR pos=pos2 etc... AND condition1 AND condition2

##queryCSV.py

This script is used to query on a  csv. Same usage as queryNucleotides

##frequencies.py

This script is used to determine the frequencies of a given marker. Arguments: dbPath and string of the marker name

##server.py

Launch the server with spark
RequestObject:
{
	"QueryType":"M"//M for markers
	"dbId":"10",
	"nucleotidesRetrieve":["nucleotideA","nucleotideB"], //["ALL"] fo all
	"plantFilter":["plantA","plantB"], //["ALL"] fo all
	"nucleotideCondition":["NucleotideC='A'"] //["NONE"] for no conditioning
}
Response 200
{
	"metadata":{
		"datafiles":[],
		"pagination":{
			"currentPage":0,
			"pageSize":1,
			"totalCount":2,
			"totalPages":1
		},
		"status":[]
	},
	"result":{
		"data":[
			{
				"nucleotide":"nucleotideX",
				"plantA":"A",
				"plantB":"B",
				"plantC":"C"
			},
			{
				"nucleotide":"nucleotideY",
				"plantA":"A",
				"plantB":"B",
				"plantC":"C"
			}
		],
		"plantDbId":123,
	}
}
