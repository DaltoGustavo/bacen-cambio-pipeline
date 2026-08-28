from pyspark.sql import functions as F
from pyspark.sql.window import Window

def transformar_cotacao(spark, dados_brutos):
    """
    Recebe os dados de uma API como lista de dicionarios e retorno um DataFrame limpo, com data convertida e variação percentual calculada.
    """
    df = spark.createDataFrame(dados_brutos)

    df = df.withColumn("data_cotacao", F.to_date(F.col("dataHoraCotacao")))

    window_spec = Window.orderBy("data_cotacao")
    df = df.withColumn("cotacao_venda_anterior", F.lag("cotacaoVenda", 1).over(window_spec))

    variacao = F.round(((df["cotacaoVenda"] - df["cotacao_venda_anterior"])/ df["cotacao_venda_anterior"]*100), 2)

    df = df.withColumn("variacao_percentual", variacao)

    return df



if __name__=="__main__":
    import os
    from pyspark.sql import SparkSession
    from extract import extract_cotacao_dolar
    import sys
    
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    os.environ["HADOOP_HOME"] = "C:\\hadoop"
    os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"

    spark = SparkSession.builder.appName("teste-transform").getOrCreate()

    dados = extract_cotacao_dolar(dias_atras=30)
    df= transformar_cotacao(spark, dados)
    df.printSchema()
    df.show(5)
