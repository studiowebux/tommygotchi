FROM python:3.11-bookworm

WORKDIR /app

COPY ./requirements.txt ./
COPY src/ ./src

RUN apt update && apt install -y \
    ffmpeg \
    python3-setuptools-rust \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "src/server/main.py"]