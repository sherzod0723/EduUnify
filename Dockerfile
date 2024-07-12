FROM python:latest

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get install -y wkhtmltopdf
RUN pip install -r req.txt

EXPOSE 8888

#ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8888"]
