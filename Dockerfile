FROM python:3.11-bookworm

WORKDIR /app

RUN apt update && apt install -y \
    ffmpeg \
    python3-setuptools-rust \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0

COPY ./requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY src/ ./src

CMD ["python3", "src/server/main.py"]