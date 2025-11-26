#usa uma imagem base Python leve
FROM python:3.11-slim

#define o diretório de trabalho
WORKDIR /app

#instala as dependências Flask e requests
RUN pip install Flask requests

#copia o código da aplicação para o container
COPY app.py .

#expõe a porta que o serviço vai usar
EXPOSE 5001

#comando para rodar a aplicação
CMD ["python", "app.py"]