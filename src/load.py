import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def load_cotacao(df_spark, table_name="cotacao_dolar"):
    """
    Recebe um DataFrame Spark, converte para Pandas e escreve na tabela especificada do banco PostgreSQL.

    """
    database_url = os.environ["DATABASE_URL"]

    df_pandas = df_spark.toPandas()
    engine = create_engine(database_url)
    df_pandas.to_sql(table_name, engine, if_exists="replace", index=False)

    print(f"{len(df_pandas)} registros escritos na tabela '{table_name}'.")

if __name__=="__main__":
    import os
    from pyspark.sql import SparkSession
    from extract import extract_cotacao_dolar
    import sys
    from transform import transformar_cotacao
    
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    os.environ["HADOOP_HOME"] = "C:\\hadoop"
    os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"

    spark = SparkSession.builder.appName("teste-load").getOrCreate()
    dados = extract_cotacao_dolar(dias_atras=30)
    df= transformar_cotacao(spark, dados)
    load_cotacao(df)