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
    
    CLIENT_ID=os.getenv("CLIENT_ID")
    CLIENT_SECRET=os.getenv("CLIENT_SECRET")
    print(os.getenv("SPARK_CONF_DIR"))
    #openssl_path = spark.conf.get("org.wildfly.openssl.path")
    #print("OpenSSL path is: {0}".format(openssl_path))
    spark.conf.set("fs.azure.account.auth.type.sparkstor.dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type.sparkstor.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id.sparkstor.dfs.core.windows.net", CLIENT_ID)
    spark.conf.set("fs.azure.account.oauth2.client.secret.sparkstor.dfs.core.windows.net", CLIENT_SECRET)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint.sparkstor.dfs.core.windows.net", "https://login.microsoftonline.com/6c51c659-9d52-41af-81f7-dde16380e813/oauth2/token")
    
    
    n = spark.read.csv("abfss://sparkdata@sparkstor.dfs.core.windows.net/files", header=True).count()
    print("Lines number is %s" % n)

    spark.stop()