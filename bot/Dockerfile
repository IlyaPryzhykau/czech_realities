FROM python:3.12

WORKDIR /app

COPY ./bot /app/bot
COPY ./bot/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["python", "-m", "bot.bot_main"]
