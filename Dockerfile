# Use a imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo pyproject.toml e poetry.lock para o diretório de trabalho
COPY pyproject.toml poetry.lock /app/

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copia o restante do código da aplicação
COPY . /app

# Expõe a porta que a aplicação irá rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["poetry", "run", "python", "app.py"]
