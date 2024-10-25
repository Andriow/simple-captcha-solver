FROM python:3.11.3-slim AS build

COPY . /captcha/
WORKDIR /captcha
ENV PYTHONPATH /captcha

ENV TZ=America/Fortaleza

RUN apt update && \
    apt install -y apt-utils && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt install -y gcc g++ python3-dev curl apt-transport-https gnupg2 openssl nano && \
    apt install -y ffmpeg libsm6 libxext6 && \
    apt install -y python3-pil tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-script-latn && \
    apt upgrade -y && \
    pip install --disable-pip-version-check -r requirements.txt && \
    apt autoremove -y && apt clean && rm -rf ~/.cache/pip/ && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone 

FROM build

ENV PYTHONUNBUFFERED=True
