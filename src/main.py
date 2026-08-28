import os
from pyspark.sql import SparkSession
from extract import extract_cotacao_dolar, salvar_dados
import sys
from transform import transformar_cotacao
from load import load_cotacao

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"

def main():
    spark = SparkSession.builder.appName("bacen-cambio-pipeline").getOrCreate()
    dados = extract_cotacao_dolar(dias_atras=30)
    salvar_dados(dados)
    df = transformar_cotacao(spark, dados)
    load_cotacao(df)

    print("Pipeline criado com sucesso!")
    spark.stop()

if __name__=="__main__":
    main()