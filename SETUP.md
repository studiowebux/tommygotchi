# Infrastructure

```text
Compute:
    - AMD Ryzen 9 5900X 12-Core Processor
    - 78GB DDR4 3200

Client:
    - Raspberry PI 4B 8GB
```

## Compute

1. Install llama-gpt
2. Expose Port 3000

## Client

1. Install Raspberry Lite OS (Bookworm)
2. Setup SSH
3. Install/Configure Python3
4. Setup whisper
5. Setup Piper
6. Setup Project
7. Create Linux Service (systemd)

---

# Setup

## Install llama-gpt on Linux

```bash
mkdir ~/tommygotchi && cd ~/tommygotchi
git clone https://github.com/getumbrel/llama-gpt.git
cd llama-gpt

# Update Container ports if needed.
sed -i 's/- 3000:/- 30000:/' docker-compose.yml

./run.sh --model 7b
```

## Install Python3 on Debian Bookworm

By default it has python 3.11 installed.

## Setup whisper on Debien Bookworm

```bash
mkdir ~/tommygotchi && cd ~/tommygotchi

sudo apt update \
    && sudo apt install -y \
        ffmpeg \
        python3-setuptools-rust
```

## Setup Piper on Debian Bookworm

Nothing Special to do

## Setup Project

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/studiowebux/tommygotchi app
cd app

sudo apt install -y \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Configure

This is only a POC, nothing has been done to configure the project.  
*You might have to edit the `main.py` and set the values for the classes.*  

## Start Project

```bash
python3 /src/client/main.py
```

## Create Linux Service

```bash
cat <<EOF > tommygotchi.service
[Unit]
Description=tommygotchi service

[Service]
User=$USER
WorkingDirectory=$HOME/tommygotchi/app
ExecStart=$HOME/tommygotchi/app/.venv/bin/python3 src/client/main.py
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target
EOF

sudo chown root:root tommygotchi.service
sudo chmod 755 tommygotchi.service
sudo mv tommygotchi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start tommygotchi.service
sudo systemctl status tommygotchi.service
sudo systemctl enable tommygotchi.service

journalctl -u tommygotchi.service -f
```

# Hardware for raspberry PI 4B 8GB

```bash
sudo apt-get install -y alsa-tools alsa-utils
```

- Microphone (USB ReSpeaker Mic Array v2.0)
- Speaker (JBL Jack 3.5mm GO 2)

# Remote voice to text (whisper) server using docker

Listens on port **4242**

*First time it takes a while to boot correctly*

```bash
docker build -t tommygotchi-server .
docker run -d --name tommygotchi-server --restart=always -p 4242:4242 tommygotchi-server:latest
```


