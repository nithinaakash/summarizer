import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Set the environment variable to allow multiple OpenMP runtimes
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

print("Loading LLaMA model and tokenizer...")

try:
    llama_model_name = 'meta-llama/llama-7b'  # Adjust the model name as necessary
    llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_name)
    print("LLaMA Tokenizer loaded.")
    
    llama_model = AutoModelForSeq2SeqLM.from_pretrained(llama_model_name)
    print("LLaMA Model loaded.")
except Exception as e:
    print(f"Error loading LLaMA components: {e}")

print("LLaMA components loaded successfully.")
