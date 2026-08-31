# BACEN Câmbio Pipeline

Pipeline de dados que consome a API pública do Banco Central do Brasil (PTAX),
transforma a cotação diária do dólar com PySpark, e carrega o resultado em um
banco de dados PostgreSQL na nuvem.

## Contexto

Este projeto foi construído como evolução do [voltmart-orders-pipeline], com o
objetivo de praticar três habilidades complementares: consumo de APIs externas,
persistência em banco de dados relacional, e boas práticas de segurança no
uso de credenciais.

## Arquitetura

O pipeline segue o padrão Extract, Transform, Load (ETL):

- **Extract** (`extract.py`): consome a API PTAX do Banco Central, retornando
  a cotação diária do dólar dos últimos N dias.
- **Transform** (`transform.py`): limpa e enriquece os dados com PySpark,
  conversão de tipos e cálculo de variação percentual dia a dia (Window Function).
- **Load** (`load.py`): escreve o resultado em uma tabela PostgreSQL (Neon).

O dado bruto da API também é salvo localmente (`data/raw/cotacao_dolar.json`)
, para fins de auditoria e possibilidade de
reprocessamento, mesmo com volume pequeno, é um princípio importante de
pipelines de dados: nunca depender só da disponibilidade futura da fonte externa.

## Decisões técnicas importantes

- Optei por converter o resultado final para Pandas (`.toPandas()`) antes de
  escrever no banco, já que o volume de dados (cotação diária) é pequeno o
  suficiente para não representar risco de memória.
- A variação percentual é calculada com uma Window Function (`lag()`) sem
  `partitionBy`, já que os dados representam uma única série temporal contínua.
- Credenciais de conexão com o banco são mantidas em variável de ambiente
  (arquivo `.env`, não versionado), nunca diretamente no código.
- Este projeto não inclui testes automatizados de qualidade de dados, dado o
  volume pequeno e a simplicidade das transformações. Para um exemplo 
  de testes com PySpark, veja o [voltmart-orders-pipeline].

## Estrutura do projeto
```
bacen-cambio-pipeline/
├── .env # credenciais (não versionado)
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│ └── raw/ # dado bruto da API, salvo antes da transformação
└── src/
├── main.py # orquestra o pipeline completo
├── extract.py
├── transform.py
└── load.py
```
## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env na raiz, com sua connection string do PostgreSQL:
# DATABASE_URL=postgresql://usuario:senha@host/banco?sslmode=require

# Rodar o pipeline completo (a partir da raiz do projeto)
python src/main.py
```

## Requisitos de ambiente (Windows)

- Python 3.11 (PySpark 3.5.8 não é compatível com versões muito recentes do Python)
- Java 17
- winutils.exe + hadoop.dll (Hadoop 3.3.6), configurados via `HADOOP_HOME`
- O caminho do projeto não deve conter espaços, para evitar falhas na
  comunicação entre o Spark e os workers Python no Windows

## Fonte de dados

API PTAX do Banco Central do Brasil:
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/

## Exemplos de resultado

### Extração da API (dado bruto)

![Dados brutos da API](imagens/dados_brutos_api.png)

### Pipeline completo em execução

![Pipeline executado](imagens/main_pipeline_sucesso.png)

### Dados carregados no PostgreSQL

Cotação diária do dólar, com variação percentual calculada via Window Function:

![Cotação no PostgreSQL](imagens/PostgreSQL_cotacao_dolar.png)

## Próximos passos (evolução futura)

- Adicionar testes de qualidade de dados
- Agendar execução periódica (ex: Airflow)
- Persistir histórico incremental no banco, em vez de substituir a
  tabela inteira a cada execução