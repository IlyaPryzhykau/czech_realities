FROM python:3.12

WORKDIR /app

COPY ./parser ./parser
COPY ./scrapy.cfg ./scrapy.cfg
COPY ./db_models ./db_models
COPY ./parser/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["sh", "-c", "cd parser && scrapy crawl czech_realities"]
