from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(path_name) 
user = os.getenv('user') 
password = os.getenv('password')
database = os.getenv('database')
host = 'host.docker.internal' # Define o host do banco de dados como 'host.docker.internal', que é um endereço especial usado para acessar serviços em execução no host a partir de um contêiner Docker.
def get_engine():
    """Cria uma conexão com o banco de dados usando SQLAlchemy.
        Returns:
            engine: Um objeto de conexão com o banco de dados.
        """
    logging.info(f"-> Conectando em {host} com o banco de dados {database}...")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine() 
def load_weather_data(table_name: str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    ) 
    '''Define a função load_data que recebe o nome da tabela e um DataFrame como argumentos. A função usa o método to_sql do DataFrame para inserir os 
    dados na tabela especificada no banco de dados. O parâmetro if_exists='append' indica que os dados devem ser adicionados à tabela existente, e index=False i
    ndica que o índice do DataFrame não deve ser incluído como uma coluna na tabela do banco de dados. '''

    logging.info(f"-> Dados carregados com sucesso na tabela {table_name}!")
    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine) # Executa uma consulta SQL para selecionar todos os dados da tabela especificada e armazena o resultado em um DataFrame chamado df_check.
    
    logging.info(f'Total de registros na tabela {table_name}: {len(df_check)}') 