import pandas as pd
from pathlib import Path
import json
import logging
# Configura o logging para exibir mensagens de informação com um formato específico, incluindo a data e hora, o nível de log e a mensagem.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define o caminho para o arquivo JSON contendo os dados meteorológicos, utilizando a biblioteca Path para construir o caminho de forma portátil e segura.
# O caminho é construído a partir do diretório do arquivo atual (__file__), subindo um nível (parent), e depois navegando para a pasta 'data' e o arquivo 'weather_data.json'.
path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'

columns_name_to_drop = ['weather','weather_icon','sys.type']
columns_name_to_rename = {
    "base" : "base",
    "visibility" : "visibility",
    "dt" : "datetime",
    "timezone" : "timezone",    
    "id" : "city_id",
    "name" : "city_name",
    "code" : "code",
    "coord.lon" : "longitude",
    "coord.lat" : "latitude",
    "main.temp" : "temperature",
    "main.feels_like" : "feels_like",
    "main.temp_min" : "temp_min",
    "main.temp_max" : "temp_max",
    "main.pressure" : "pressure",
    "main.humidity" : "humidity",
    "main.sea_level" : "sea_level",
    "main.grnd_level" : "grnd_level",
    "wind.speed" : "wind_speed",
    "wind.deg" : "wind_deg",
    "wind.gust" : "wind_gust",
    "clouds.all" : "clouds",
    "sys.type" : "sys_type",
    "sys.id" : "sys_id",
    "sys.country" : "country",
    "sys.sunrise" : "sunrise",
    "sys.sunset" : "sunset"
}

columns_to_normalize_datetime = ['datetime','sunrise','sunset']

def create_dataframe(path_name: str) -> pd.DataFrame:
    """Cria um DataFrame a partir de um arquivo JSON.
        Args:
            path (str): O caminho para o arquivo JSON.

        Returns:
            pd.DataFrame: Um DataFrame contendo os dados do arquivo JSON.
        """
    logging.info(f"Criando DataFRame do arquivo JSON...")
    path = Path(path_name)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    
    with open(path) as f:
        data = json.load(f)
    
    df = pd.json_normalize(data)
    logging.info(f"DataFrame criado com sucesso. Número de linhas: {len(df)}, Número de colunas: {len(df.columns)}")
    return df

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza os nomes das colunas do DataFrame de dados meteorológicos.
        Args:
            df (pd.DataFrame): O DataFrame a ser normalizado.

        Returns:
            pd.DataFrame: Um DataFrame com os nomes das colunas normalizados.
        """
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0])) # Normaliza a coluna 'weather' do DataFrame, aplicando uma função lambda para extrair o primeiro elemento de cada lista na coluna 'weather' e criando um novo DataFrame com os dados normalizados.
    
    df_weather = df_weather.rename(columns={
        'id' : 'weather_id',
        'main' : 'weather_main',
        'description' : 'weather_description',
        'icon' : 'weather_icon'
    }
    )

    df = pd.concat([df, df_weather], axis=1) # Concatena o DataFrame original com o DataFrame normalizado 'df_weather' ao longo do eixo das colunas (axis=1), resultando em um DataFrame combinado que inclui as colunas originais e as novas colunas normalizadas.

    logging.info(f"\n/ Coluna 'weather' normalizada com sucesso. Número de colunas após normalização: {len(df.columns)}")
    return df

def drop_weather_column(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f"Removendo coluna {columns_name}")
    df = df.drop(columns=columns_name)
    logging.info(f"Colunas {columns_name} removidas com sucesso.")
    return df

def rename_columns(df: pd.DataFrame, columns_name: dict[str, str]) -> pd.DataFrame:
    logging.info(f"Renomeando colunas {columns_name}")
    df = df.rename(columns=columns_name)
    logging.info(f"Colunas {list(columns_name.values())} renomeadas com sucesso.")
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:

    for name in columns_name:
        logging.info(f"Normalizando coluna de data/hora: {name}")
        df[name] = pd.to_datetime(df[name], unit='s',utc=True).dt.tz_convert('America/Sao_Paulo')# Converte a coluna de data/hora para o formato datetime do pandas, especificando que os valores estão em segundos (unit='s') e que estão em UTC (utc=True), e depois converte para o fuso horário 'America/Sao_Paulo' usando dt.tz_convert().
        logging.info(f"Coluna {name} normalizada com sucesso.")
    return df

def data_transformations():
    print("Iniciando transformação dos dados...")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_weather_column(df, columns_name_to_drop)
    df = rename_columns(df, columns_name_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    print("Transformação dos dados concluída.")
    return df
