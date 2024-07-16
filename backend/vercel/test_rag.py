import os
from flask import Flask, request, jsonify
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
from datasets import load_dataset

# Initialize Flask app
app = Flask(__name__)

# Load the dataset from Hugging Face
dataset = load_dataset("wiki_dpr", "psgs_w100.nq.exact", split="train[:1%]")

# Save the dataset to disk (if needed)
dataset_path = 'dataset'
dataset.save_to_disk(dataset_path)

# Load RAG model components
model_name = "facebook/rag-token-base"
tokenizer = RagTokenizer.from_pretrained(model_name)

# Use the dataset for the retriever
retriever = RagRetriever.from_pretrained(
    model_name, 
    index_name="exact", 
    passages_path=dataset_path
)

model = RagSequenceForGeneration.from_pretrained(model_name, retriever=retriever)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Generate summary using RAG model
        summary_ids = model.generate(**inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        
        # Decode the generated summary
        summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)[0]
        
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
