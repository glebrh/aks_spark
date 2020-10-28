from __future__ import print_function

import sys
from random import random
from operator import add
import time
import os

from pyspark.sql import SparkSession


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    spark = SparkSession\
        .builder\
        .appName("PythonPi")\
        .getOrCreate()

    print("CLIEND_ID: ", os.getenv('CLIEND_ID'))
    print("CLIEND_SECRET: ", os.getenv('CLIEND_SECRET'))
    print("Start 60 seconds sleep")
    time.sleep(60)
    print("Ended sleep")
    
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))

    spark.stop()