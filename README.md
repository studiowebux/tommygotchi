# Notes

# Install Whisper on MacOS

```bash
sudo port install portaudio
sudo port install pkgconfig
CFLAGS="-I/opt/local/include -L/opt/local/lib" python3 -m pip install pyaudio
pip3 install git+https://github.com/openai/whisper.git
pip3 install -r requirements.txt
```

# Piper Installation on MacOS

Source: https://github.com/rhasspy/piper-phonemize/issues/14#issuecomment-1837289540

```bash
git clone https://github.com/rhasspy/piper-phonemize.git
cd piper-phonemize
git checkout fccd4f335aa68ac0b72600822f34d84363daa2bf -b my
make

export DYLD_LIBRARY_PATH=`pwd`/install/lib/
echo "testing one two three" | ./install/bin/piper_phonemize -l en-us --espeak-data ./install/share/espeak-ng-data/

patch -p1 <<EOF
--- a/setup.py
+++ b/setup.py
@@ -9 +9 @@ _DIR = Path(__file__).parent
-_ESPEAK_DIR = _DIR / "espeak-ng" / "build"
+_ESPEAK_DIR = _DIR / "install"
@@ -13 +13 @@ _ONNXRUNTIME_DIR = _LIB_DIR / "onnxruntime"
-__version__ = "1.2.0"
+__version__ = "1.1.0"
EOF

pip3 install .

cp -rp ./install/share/espeak-ng-data /Users/tgingras/miniforge3/lib/python3.10/site-packages/piper_phonemize/espeak-ng-data

echo 'Welcome to the world of speech synthesis!' | piper --model en_US-lessac-medium --output_file welcome.wav
afplay welcome.wav
```

# Generate wav using Piper

```bash
echo 'Yes !' | \
  piper --model ./piper-voices/en_US-amy-medium.onnx --output_file yes.wav
echo 'Ok !' | \
  piper --model ./piper-voices/en_US-amy-medium.onnx --output_file ok.wav
```

# Llama GPT Installation

https://github.com/getumbrel/llama-gpt

API: `POST http://localhost:3000/api/chat`

See data : [Data JSON](./data.json)

```bash
git clone https://github.com/getumbrel/llama-gpt.git
cd llama-gpt
./run-mac.sh --model 7b
./run-mac.sh --model 13b

./run.sh --model 7b
./run.sh --model 7b --with-cuda
./run.sh --model 13b --with-cuda
```

---

# Start

On MacOS:

```bash
export DYLD_LIBRARY_PATH="$PWD/piper-phonemize/install/lib/"
```

```bash
python3 src/client/main.py
```

# Server to run whisper on remote machine

```bash
python3 src/server/main.py
```

```text
POST http://localhost:4242/api
form-data: key=file
```

Returns `application/json`

```json
{
  "status": "OK", // "ERR"
  "result": "transcribed text" // "Failed to transcribe..."
}
```

# Sounds

- https://freesound.org/people/GameAudio/sounds/220175/
- https://freesound.org/people/harrisonlace/sounds/611503/

