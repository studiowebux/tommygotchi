from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)

from llama_index import set_global_tokenizer
from transformers import AutoTokenizer
from llama_index.embeddings import HuggingFaceEmbedding



llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url=None,
    # optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path="./llama-2-13b-chat.Q4_0.gguf",
    # model_path="../../models/mistral-7b-v0.1.Q4_0.gguf",
    temperature=0.1,
    # max_new_tokens=256,
    max_new_tokens=2048,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    # context_window=4096,
    context_window=4000,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": 1},
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)

# response = llm.complete("Hello! Can you tell me a poem about cats and dogs?")
# print(response.text)

# response_iter = llm.stream_complete("Can you write me a poem about fast cars?")
# for response in response_iter:
#     print(response.delta, end="", flush=True)
    
set_global_tokenizer(
    AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode
)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
)

documents = SimpleDirectoryReader(
    input_dir="./data/test", recursive=True, required_exts=[".md", ".txt"]
).load_data()

index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

# query_engine = index.as_query_engine(response_mode="tree_summarize")
# print(response)
# response = query_engine.query("Summarize the article")

query_engine = index.as_query_engine()
response = query_engine.query("What is the article about?")
print(response)