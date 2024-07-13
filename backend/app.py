from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, RagTokenizer, RagRetriever, RagSequenceForGeneration
import torch

app = Flask(__name__)

# Load the RAG model and tokenizer
rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
rag_retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index_name="exact", use_dummy_dataset=True)
rag_model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-base", retriever=rag_retriever)

# Load the LLaMA model and tokenizer for generation
llama_model_name = 'meta-llama/llama-7b'  # Adjust the model name as necessary
llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_name)
llama_model = AutoModelForSeq2SeqLM.from_pretrained(llama_model_name)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get('text', '')

    # Tokenize the input text using the RAG tokenizer
    inputs = rag_tokenizer(text, return_tensors='pt')

    # Retrieve relevant documents and generate a summary using RAG
    rag_outputs = rag_model.generate(inputs['input_ids'], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode the RAG output
    rag_summary = rag_tokenizer.batch_decode(rag_outputs, skip_special_tokens=True)

    # Further process the summary using LLaMA (if necessary)
    llama_inputs = llama_tokenizer(rag_summary, return_tensors='pt', padding=True, truncation=True)
    llama_outputs = llama_model.generate(llama_inputs['input_ids'], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode the LLaMA output
    llama_summary = llama_tokenizer.batch_decode(llama_outputs, skip_special_tokens=True)

    return jsonify(summary=llama_summary[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
