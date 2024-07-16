import os
from flask import Flask, request, jsonify
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

# Initialize Flask app
app = Flask(__name__)

# Load BART model components
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Tokenize the input text
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

        # Generate summary using BART model
        summary_ids = model.generate(inputs, max_length=15000, min_length=3, length_penalty=2.0, num_beams=4, early_stopping=True)
        
        # Decode the generated summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ensure this line is only run during local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
