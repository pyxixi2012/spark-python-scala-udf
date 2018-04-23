import sys
#from pyspark.sql import SparkSession,SQLContext

def square(s):
  return s * s

#def process(argv):
  #spark = SparkSession.builder.appName("PythonUDF").getOrCreate()
  #sc = spark.sparkContext
  #sqlContext = SQLContext(spark.sparkContext)
  #sqlContext.range(1, 4).registerTempTable("test")
  #do_sql(spark,sqlContext)
  #do_df(spark,sqlContext)
  #do_sql_scala(spark,sqlContext)

def do_sql(spark,sqlContext):
  print "Calling Python UDF with SQL"
  sqlContext.udf.register("squareWithPython", square)
  spark.sql("select id, squareWithPython(id) as id_square_sql from test").show()

def do_sql_scala(spark,sqlContext):
  print "Calling Scala UDF with SQL"
  spark._jvm.org.andre.udf.Functions.registerFunc(sqlContext._jsqlContext,"cube")
  spark.sql("select id, cube(id) as id_cube_scala from test").show()

def do_df(spark,sqlContext):
  from pyspark.sql.functions import udf
  from pyspark.sql.types import LongType
  print "Calling Python UDF with DataFrame"
  square_udf = udf(square, LongType())
  df = sqlContext.table("test")
  df.select("id", square_udf("id").alias("id_square_df")).show()
