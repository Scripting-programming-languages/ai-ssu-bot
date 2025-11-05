FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1

COPY ./backend ./backend
RUN apt-get update && apt-get install -y dos2unix \
    && dos2unix /backend/start.sh
WORKDIR /backend
ENV PYTHONPATH=/backend/

# Установка зависимостей напрямую через pip
RUN pip install --upgrade pip
RUN pip install .

RUN chmod +x ./start.sh
EXPOSE 8000
CMD ["bash", "./start.sh"]
