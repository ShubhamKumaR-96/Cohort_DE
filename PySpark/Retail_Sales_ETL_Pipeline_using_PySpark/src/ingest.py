from pyspark.sql import SparkSession

def create_spark_session(app_name="Retail ETL Pipeline"):
    spark = SparkSession.builder\
            .appName(app_name)\
            .getOrCreate()
    return spark


def load_path(spark,file_path,file_type="csv"):
    """
    Load raw data from csv or excel
    """
    if file_type=="csv":
        df = spark.read.option("header",True).option("inferSchema",True).csv(file_path)
    elif file_type == "xlsx":
        df = spark.read.format("com.crealytics.spark.excel")\
            .option("header",True).option("inferSchema",True).csv(file_path)   

    else:
        raise ValueError("Unsupported file type")

    return df     