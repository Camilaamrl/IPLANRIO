# Usa uma versão do Python pronta para uso
FROM python:3.10-slim

# Define onde os arquivos vão ficar dentro da bolha
WORKDIR /app

# Copia a lista de ferramentas e as instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos seus arquivos para dentro da bolha
COPY . .

# Comando para manter o container vivo
CMD ["sleep", "infinity"]