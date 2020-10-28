from __future__ import print_function

import sys
from random import random
from operator import add
import os

from pyspark.sql import SparkSession


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    spark = SparkSession\
        .builder\
        .appName("ADLSTest")\
        .getOrCreate()
    
    print("SPARK DIST CLASSPATH IS: ", os.getenv('SPARK_DIST_CLASSPATH'))
    print("HADOOP HOME IS: ", os.getenv('HADOOP_HOME'))
    n = spark.read.csv("abfss://sparkdata@sparkstor.dfs.core.windows.net/files", header=True).count()
    print("Lines number is %s" % n)

    spark.stop()