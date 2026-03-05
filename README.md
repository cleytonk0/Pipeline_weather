# Pipeline Weather - EMT (Extract, Transform, Load)

## 📋 Visão Geral

**Pipeline Weather** é um sistema de orquestração e processamento de dados climáticos.O projeto implementa uma pipeline ETL automatizada que extrai dados meteorológicos da API OpenWeatherMap, realiza transformações estruturadas e carrega os dados em um banco de dados PostgreSQL.

Este projeto foi desenvolvido incluindo:
- **Orquestração de workflows** com Apache Airflow
- **Processamento de dados** com Pandas
- **Containerização** com Docker
- **Integração com APIs** RESTful

---

### Componentes Principais

| Componente | Responsabilidade | Localização |
|------------|-----------------|-------------|
| **Extract** | Coleta de dados brutos de API externa | `src/extract_data.py` |
| **Transform** | Normalização, limpeza e estruturação de dados | `src/transformer_data.py` |
| **Load** | Persistência em banco de dados relacional, no PostgreSQL | `src/load_data.py` |
| **Orquestração** | Agendamento automático com Airflow | `dags/weather_dag.py` |

---

## 🛠️ Tecnologias e Dependências

### Stack Tecnológico

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | ≥3.12 | Linguagem principal |
| **Apache Airflow** | ≥2.10.0 | Orquestração de workflows DAG |
| **Pandas** | ≥3.0.1 | Processamento e análise de dados |
| **PostgreSQL** | 16 | Data warehouse relacional |
| **SQLAlchemy** | ≥2.0.47 | ORM e abstração de BD |
| **Redis** | Latest | Message broker para Celery |
| **Docker** | Latest | Containerização e orquestração |

### Dependências Python

```toml
apache-airflow>=2.10.0        # Orquestração de pipelines
pandas>=3.0.1                 # Manipulação de dados
psycopg2-binary>=2.9.11       # Driver PostgreSQL
python-dotenv>=1.2.1          # Gerenciamento de variáveis de ambiente
requests>=2.32.5              # Cliente HTTP para APIs
sqlalchemy>=2.0.47            # ORM e SQL toolkit
```

---


## 📊 Estrutura do Projeto

```
pipeline_weather/
├── config/
│   ├── airflow.cfg           # Configurações do Airflow
│   └── .env                  # Variáveis de ambiente (não versionado)
├── dags/
│   └── weather_dag.py        # DAG principal do Airflow
├── data/
│   └── weather_data.json     # Dados brutos extraídos
├── logs/
│   └── [Logs do Airflow]     # Logs de execução
├── notebooks/
│   └── analysis_data.ipynb   # Análise exploratória de dados
├── plugins/
│   └── [Plugins Airflow]     # Extensões Airflow
├── src/
│   ├── extract_data.py       # Módulo de extração
│   ├── transformer_data.py   # Módulo de transformação
│   └── load_data.py          # Módulo de persistência
├── docker-compose.yaml       # Orquestração de containers
├── main.py                   # Script de execução local (standalone)
├── pyproject.toml            # Configuração do projeto
└── README.md                 # Esta documentação
```

---

## 📚 Referências e Recursos

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Melhorias a fazer

- [ ] Implementar data quality checks (Great Expectations)
- [ ] Adicionar monitoring com Prometheus/Grafana
- [ ] Criar testes unitários (pytest)
- [ ] Configurar CI/CD com GitHub Actions
- [ ] Documentar múltiplas cidades simultaneamente

---
