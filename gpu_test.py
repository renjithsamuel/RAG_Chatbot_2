from llama_cpp import Llama

llm = Llama(
    model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_gpu_layers=-1,  # Use all GPU layers
    n_ctx=2048,
)

print(llm.create_chat_completion([{"role": "user", "content": "Hello"}]))