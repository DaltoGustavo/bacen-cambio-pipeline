import requests
from datetime import datetime, timedelta
import json

def extract_cotacao_dolar(dias_atras=30):
    """
    Consome a API do Banco Central e retorna os dados da cotação do dólar dos últimos N dias em um dicionario.
    """

    data_final = datetime.today()
    data_inicial = data_final - timedelta(days=dias_atras)

    data_inicial_str = data_inicial.strftime("%m-%d-%Y")
    data_final_str = data_final.strftime("%m-%d-%Y")
    url = (f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{data_inicial_str}'&@dataFinalCotacao='{data_final_str}'&$format=json")

    response = requests.get(url)
    response.raise_for_status()
    
    dados = response.json()
    return dados["value"]

def salvar_dados(dados_brutos, output_path="data/raw/cotacao_dolar_json"):
    """
    Salva os dados brutos da API para fins de auditoria e reprocessamento.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dados_brutos, f, indent=2)



if __name__=="__main__":
    resultado = extract_cotacao_dolar(dias_atras=30)
    print(f"Registros recebidos: {len(resultado)}")
    print(resultado[:2])
