#!/bin/bash

set -e  # Encerra o script se algum comando falhar
set -o pipefail

echo "🟡 Atualizando pacotes do sistema..."
sudo apt update

echo "🟡 Instalando dependências do sistema (libpq-dev)..."
sudo apt install -y libpq-dev

echo "🟡 Criando ambiente virtual com uv..."
uv venv
uv add --requirements requirements.txt

echo "🟡 Ativando ambiente virtual..."
source .venv/bin/activate

echo "🟡 Instalando bibliotecas Python..."
uv pip install psycopg2-binary pandas

echo "🟡 Subindo containers Docker..."
sudo docker compose up -d

echo "🟡 Aguardando bancos de dados subirem..."
sleep 10  # Dá tempo para os bancos iniciarem

echo "🟢 Executando importador de CSVs..."
python import_csv_to_postgres.py

echo "✅ Tudo pronto! As tabelas foram criadas a partir dos CSVs."
