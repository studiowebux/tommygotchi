# Setup llama-cpp-python

**Setup on MacOS M1**

```bash
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh -o Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```

```bash
conda create -n llama python=3.9.16
conda activate llama

pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U llama-cpp-python --no-cache-dir
python3 -m pip install 'llama-cpp-python[server]'

curl -L https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf?download=true -o llama-2-13b-chat.Q4_0.gguf


# export MODEL=./llama-2-13b-chat.Q4_0.gguf

# https://huggingface.co/TheBloke/Samantha-1.11-13B-GGUF/blob/main/samantha-1.11-13b.Q4_0.gguf
export MODEL=./samantha-1.11-13b.Q4_0.gguf
python3 -m llama_cpp.server --model $MODEL  --n_gpu_layers 1
```

## Sources

- https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF
- https://llama-cpp-python.readthedocs.io/en/latest/install/macos/

---

# Llama CPP Python with openai API

## Streaming

```bash
pip install openai

python3 src/streaming.py
```

### Sources

- https://platform.openai.com/docs/api-reference/
- https://github.com/openai/openai-python

---

# llama index

## Sources

- https://docs.llamaindex.ai/en/stable/examples/llm/llama_2_llama_cpp.html

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt


python3 src/llamaidx.py
```