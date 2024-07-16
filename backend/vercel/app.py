import os

# Set the environment variable to allow multiple OpenMP runtimes
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, RagTokenizer, RagRetriever, RagSequenceForGeneration
import torch
from datasets import load_dataset
import faiss  # Ensure faiss is imported

app = Flask(__name__)

print("Loading dataset...")

# Load the summarization dataset
dataset = load_dataset('cnn_dailymail', '3.0.0', split='train')

print("Dataset loaded. Saving to disk...")

# Save the dataset to disk
dataset_path = 'dataset'
dataset.save_to_disk(dataset_path)

print("Dataset saved to disk. Loading RAG model and tokenizer...")

# Load the RAG model and tokenizer
try:
    rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
    print("RAG Tokenizer loaded.")
    
    rag_retriever = RagRetriever.from_pretrained(
        "facebook/rag-token-base",
        index_name="exact",
        use_dummy_dataset=True,
        passages_path=dataset_path  # Load dataset from disk path
    )
    print("RAG Retriever loaded.")

    rag_model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-base", retriever=rag_retriever)
    print("RAG Model loaded.")
except Exception as e:
    print(f"Error loading RAG components: {e}")

# Load the LLaMA model and tokenizer for generation
try:
    llama_model_name = 'meta-llama/llama-7b'  # Adjust the model name as necessary
    llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_name)
    print("LLaMA Tokenizer loaded.")
    
    llama_model = AutoModelForSeq2SeqLM.from_pretrained(llama_model_name)
    print("LLaMA Model loaded.")
except Exception as e:
    print(f"Error loading LLaMA components: {e}")

print("Models loaded. Setting up input parameters...")

MAX_INPUT_LENGTH = 512  # Maximum length the model can handle
MAX_OUTPUT_LENGTH = 150

def chunk_text(text, max_length):
    """Split the text into chunks of max_length."""
    words = text.split()
    chunks = [' '.join(words[i:i + max_length]) for i in range(0, len(words), max_length)]
    return chunks

print("Server setup complete. Starting Flask app...")

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get('text', '')

    print("Received text for summarization...")

    # Split the text into chunks
    chunks = chunk_text(text, MAX_INPUT_LENGTH)

    summaries = []
    for chunk in chunks:
        try:
            # Tokenize the input text using the RAG tokenizer
            inputs = rag_tokenizer(chunk, return_tensors='pt', truncation=True, max_length=MAX_INPUT_LENGTH)
            print(f"Tokenized input: {inputs}")

            # Retrieve relevant documents and generate a summary using RAG
            rag_outputs = rag_model.generate(
                inputs['input_ids'], 
                max_length=MAX_OUTPUT_LENGTH,  # Adjust this if you need a longer summary
                min_length=30, 
                length_penalty=2.0, 
                num_beams=4, 
                early_stopping=True
            )
            print(f"RAG Outputs: {rag_outputs}")

            # Decode the RAG output
            rag_summary = rag_tokenizer.batch_decode(rag_outputs, skip_special_tokens=True)[0]
            print(f"RAG Summary: {rag_summary}")

            # Further process the summary using LLaMA (if necessary)
            llama_inputs = llama_tokenizer(rag_summary, return_tensors='pt', padding=True, truncation=True, max_length=MAX_INPUT_LENGTH)
            llama_outputs = llama_model.generate(
                llama_inputs['input_ids'], 
                max_length=MAX_OUTPUT_LENGTH,  # Adjust this if you need a longer final output
                min_length=30, 
                length_penalty=2.0, 
                num_beams=4, 
                early_stopping=True
            )
            print(f"LLaMA Outputs: {llama_outputs}")

            # Decode the LLaMA output
            llama_summary = llama_tokenizer.batch_decode(llama_outputs, skip_special_tokens=True)[0]
            print(f"LLaMA Summary: {llama_summary}")

            summaries.append(llama_summary)
        except Exception as e:
            print(f"Error during summarization process: {e}")

    # Combine the partial summaries
    final_summary = ' '.join(summaries)

    print("Summarization complete. Returning response...")

    return jsonify(summary=final_summary)

if __name__ == '__main__':
    print("Running app...")
    app.run(host='0.0.0.0', port=5000)
