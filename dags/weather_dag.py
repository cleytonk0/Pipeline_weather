import sys
import os
from pathlib import Path

AIRFLOW_HOME = Path("/opt/airflow")
SRC_PATH = AIRFLOW_HOME / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
if str(AIRFLOW_HOME) not in sys.path:
    sys.path.insert(0, str(AIRFLOW_HOME))

from datetime import datetime, timedelta
from airflow.decorators import dag, task
import extract_data
import load_data
import transformer_data
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("API_KEY")
url = f"https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}"

@dag(
    dag_id="weather_dag",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5)
    },
    description="DAG para extrair, transformar e carregar dados de clima de Sao Paulo",
    schedule="0 */1 * * *",
    start_date=datetime(2026, 2, 7),
    catchup=False,
    tags=["weather", "etl"]
)
def weather_pipeline():

    @task()
    def extract():
        extract_data.extract_weather_data(url)

    @task()
    def transform():
        import pandas as pd
        df = transformer_data.data_transformations()
        df.to_parquet("/opt/airflow/data/temp_data.parquet", index=False)

    @task()
    def load():
        import pandas as pd
        df = pd.read_parquet("/opt/airflow/data/temp_data.parquet")
        load_data.load_weather_data("sp_weather", df)

    extract() >> transform() >> load()

weather_pipeline()
