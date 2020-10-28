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
    spark.conf.set("fs.azure.account.key.sparkstor.dfs.core.windows.net", "l9QpO1pw2Qsb+7Cxi+I/j5rflDDqB6aJs2yXDIdh8k6m7XVD+UJnqQ/6+A9BQyt8pDNeS8jwmVdK2SyYMP7PTw==")
    n = spark.read.csv("abfss://sparkdata@sparkstor.dfs.core.windows.net/files", header=True).count()
    print("Lines number is %s" % n)

    spark.stop()