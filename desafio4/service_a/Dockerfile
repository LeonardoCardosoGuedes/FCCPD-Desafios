#usa uma imagem base python leve
FROM python:3.11-slim

#define o diretório de trabalho
WORKDIR /app

#instala a dependência flask
RUN pip install Flask

#copia o código da aplicação para o container
COPY app.py .

#expõe a porta que o serviço vai usar
EXPOSE 5000

#comando para rodar a aplicação
CMD ["python", "app.py"]